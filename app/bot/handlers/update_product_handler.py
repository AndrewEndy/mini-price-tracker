import asyncio
from aiogram import Router, F
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from app.db import SessionLocal
from app.models import Product, Price, User
from app.bot.create_bot import admins, bot
from app.bot.keyboards.reply_keyboard import main_rp_kb
from app.bot.keyboards.inline_keyboard import back_home_and_show_my_products_inline_kb, show_all_my_products_inl_kb, product_control_inline_kb
from app.bot.fsm.form_fsm import Change_name_form
from app.services import get_updated_product_data
from app.utils.creating_text_about_user_products import get_update_data_text
from app.utils.work_with_database import delete_product_by_id



update_product_data_router = Router()

# *** Оновити дані про товар ***
@update_product_data_router.callback_query(F.data.startswith('update_status_'))
async def update_product_data(data: CallbackQuery):
    '''Хендлер для оновлення даних про товар'''
    
    async with ChatActionSender.typing(bot=bot, chat_id=data.from_user.id):
        
        await asyncio.sleep(1)
        
        await data.answer()
        await data.message.delete()

        product_id = int(data.data.replace('update_status_', ''))
        
        async with SessionLocal() as session:
            query = ( # Отримати product з product_id
                select(Product)
                .join(User)
                .where(Product.product_id == product_id, User.tg_id == data.from_user.id)
                .options(joinedload(Product.prices))  # Опціонально підвантажуємо ціни
            )
            result = await session.execute(query)
            
        product = result.scalars().first() 
            
        last_price_obj = max(product.prices, key=lambda price: price.date)          
        max_price_obj = max(product.prices, key=lambda price: price.price)
        min_price_obj = min(product.prices, key=lambda price: price.price)
        
        res = await get_updated_product_data({product.store_name: (product.url, data.from_user.id)})
    
        if res:
            
            _, new_price = res
        
            if (new_price.price != last_price_obj.price or new_price.price < min_price_obj.price 
                or new_price.price > max_price_obj.price or new_price.discount != last_price_obj.discount):
                
                await data.message.answer(f'Виявлено нові дані🧐') 
                await asyncio.sleep(2)
            
                new_price.product = product
                
                async with SessionLocal() as session:
                    session.add(new_price)
                    await session.commit()
                    
                text = await get_update_data_text(product,last_price_obj, min_price_obj, max_price_obj, new_price)  
                await data.message.answer(text, reply_markup=back_home_and_show_my_products_inline_kb())
                
            else: await data.message.answer(f'Дані товару не змінились🙌', reply_markup=main_rp_kb(data.from_user.id))
            
        else: # Якщо отримали none, видаляємо товар з БД
            await delete_product_by_id(product_id=product.product_id)
            data.message.answer(f'Даний товар більше не доступний😢', reply_markup=main_rp_kb(data.from_user.id))



# *** Змінити назву товара ***  

@update_product_data_router.callback_query(F.data.startswith('change_name_'))
async def change_name(data: CallbackQuery, state: FSMContext):
    '''Хендлер для змінни назви товару'''
    await data.answer()
    await data.message.delete()
    
    product_id = int(data.data.replace('change_name_', ''))
    
    await data.message.answer(f'Введіть назву товара')
    
    await state.set_state(Change_name_form.change_name)
    await state.update_data(product_id = product_id)
    

@update_product_data_router.message(F.text, Change_name_form.change_name)
async def set_new_name(message: Message, state: FSMContext):
    '''Хендлер який змінює назву товару в БД'''
    
    if len(message.text) > 255: # Якщо назва занадто довга, просить ввести коротшу назву 
        await message.answer(f'Назва завелика!\nБудь ласка введіть іншу')
        await state.set_state(Change_name_form.change_name)
        
    else: # Інкаше змінює назву в БД і перекидає в головне меню
        data = await state.get_data()
        product_id = int(data.get('product_id'))
        print(f'---{product_id}---')
        print(f'---{message.text}---')
        
        async with SessionLocal() as session:
            # Оновлення назви продукту
            stmt = (
                update(Product)
                .where(Product.product_id == product_id)
                .values(product_name=message.text)
                .execution_options(synchronize_session="fetch")  # Для синхронізації сесії
            )
            await session.execute(stmt)
            await session.commit()
            
        await state.clear()
        await message.answer(f'Назву змінено!', reply_markup=main_rp_kb(message.from_user.id))


@update_product_data_router.message(Change_name_form.change_name)
async def foo(message: Message, state: FSMContext):
    '''Хендлер спрацьовує якщо користувач ввів щось не те'''
    await message.answer(f'Введіть назву товару!')
    await state.set_state(Change_name_form.change_name)
        
    
            