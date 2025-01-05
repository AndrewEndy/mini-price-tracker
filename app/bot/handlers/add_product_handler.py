import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from app.bot.fsm.form_fsm import Add_product_form
from app.bot.create_bot import admins, bot
from app.bot.keyboards.reply_keyboard import main_rp_kb
from app.bot.keyboards.inline_keyboard import inline_kb_store, back_home_inline_kb, check_name_product_inline_kb
from app.checks.check_url import check_connection_to_url, check_desired_site
from app.services import add_new_product
from app.utils.work_with_database import is_url_in_db


add_product_router = Router()


@add_product_router.callback_query(F.data.startswith('store_'))
async def add_product(data: CallbackQuery, state: FSMContext):
    '''Хендлер для отримання назви магазина та початку додання нового товару шляхом встановлення FSM стану'''
    await data.answer()
    await data.message.delete()
    await state.set_state(Add_product_form.waiting_for_url)
    
    store_name = data.data.replace('store_', '')
    await state.update_data(store_name=store_name) # Передаємо в FSM назву магазина
    
    await data.message.answer(f'Введіть силку на товар', reply_markup=back_home_inline_kb())
    
    
@add_product_router.message(F.text, Add_product_form.waiting_for_url)
async def add_product(message: Message, state: FSMContext):
    '''Хендлер для всіх перевірок та додання нового товару'''
    
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        
        connection_to_url = await check_connection_to_url(message.text) # Перевірка чи можливо підключитись по силці
        
        if connection_to_url:
            
            data = await state.get_data()
            store_name = data.get('store_name') # Отримання назви магазина з FSM стану
            
            flag = await check_desired_site(message.text, store_name) # Перевірка на коректність URL для конкретного магазина
            if flag:
                same_url = await is_url_in_db(message.text, message.from_user.id) # Перевірка чи такий URL уже є в user
                
                if same_url:
                    await state.clear()
                    await message.answer(f'Даний товар вже відстежується', reply_markup=main_rp_kb(message.from_user.id))
                else:
                    product_id, product_name = await add_new_product(message.text, store_name, message.from_user.id)
                    await message.answer(f'Товар успішно додано👏\n<b>Навза товару</b>: {product_name}', reply_markup=check_name_product_inline_kb(product_id))
            else:
                await state.clear()
                await message.answer(f'Ви ввели не вірну силку!', reply_markup=main_rp_kb(message.from_user.id))
             
        else:
            await state.clear()
            await message.answer(f'Неможливо підключитись по силці!', reply_markup=main_rp_kb(message.from_user.id))
            
            
@add_product_router.message(Add_product_form.waiting_for_url)
async def foo(message: Message, state: FSMContext):
    '''Хендлер який спрацьовує якщо ввели щось не те'''
    await message.answer(f'Ви ввели некоректну силку!')
    await state.set_state(Add_product_form.waiting_for_url)


@add_product_router.callback_query(F.data == 'end_add_product')
async def foo(data: CallbackQuery, state: FSMContext):
    '''Хендлер який спрацьовує якщо назва товару влаштовує користувача'''
    await data.answer()
    await data.message.delete()
    await data.message.answer('Товар успішно додано👏',reply_markup=main_rp_kb(data.from_user.id))
    await state.clear()