import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from sqlalchemy import update, text as sqltext
from sqlalchemy.orm import joinedload
from app.db import SessionLocal
from app.models import Product, Price, User
from app.bot.fsm.form_fsm import Product_review_form
from app.bot.create_bot import admins, bot
from app.bot.keyboards.reply_keyboard import main_rp_kb
from app.bot.keyboards.inline_keyboard import back_home_and_show_my_products_inline_kb, show_all_my_products_inl_kb, product_control_inline_kb
from app.utils.creating_text_about_user_products import get_text_for_one_product, get_info_product



view_router = Router()


# -----Переглянути мої товари-----  

# *** Показати мої товари ***  

@view_router.message(F.text == '👀 Переглянути мої товари')
async def show_my_products(message: Message, state: FSMContext):
    '''Хендлер для перегляду товарів користувача'''
    
    # Ставим FSM стан для можливих кнопое "вперед" і "назад"
    await state.set_state(Product_review_form.product_review)
    
    async with SessionLocal() as session:
    # Отримуємо список продуктів для користувача з tg_id
        tg_id = message.from_user.id
        query = (
            select(Product)
            .join(User)
            .where(User.tg_id == tg_id)
            .options(joinedload(Product.prices))  # Опціонально, щоб підвантажити пов'язані ціни
        )
        result = await session.execute(query)
        next_products = result.unique().scalars().all()  
        
    if next_products:
        msg = await message.answer('Виберіть один з варіантів', reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(0.1)
        await msg.delete()
        
        # 11 - максимум можливих товарів щоб не сталась помилка (макс кнопок - 15)
        if len(next_products) <= 11:
            await message.answer(f'Виберіть один з варіантів', reply_markup=show_all_my_products_inl_kb(next_products))
        else:
            # Створюєм додаткові списки, між якими будем переміщати товари
            previous_products = [] 
            current_products = next_products[:11]
            next_products = next_products[11:]
            
            # Поміщаємо ці списки в FSM пам'ять, щоб потім їх отримати
            await state.update_data(next_products=next_products, current_products=current_products, previous_products=previous_products)
            
            await message.answer(f'Виберіть один з варіантів', reply_markup=show_all_my_products_inl_kb(current_products, next_page=True)) 
        
    else:
        await message.answer(f'У вас немає доданих товарів😔', reply_markup=main_rp_kb(message.from_user.id))
   
    
    
@view_router.callback_query(F.data == 'show_my_products')
async def show_my_products(data: CallbackQuery, state: FSMContext):
    '''Хендлер для перегляду товарів користувача'''
    
     # Ставим FSM стан для можливих кнопое "вперед" і "назад"
    await state.set_state(Product_review_form.product_review)
    await data.answer()
    await data.message.delete()
    
    async with SessionLocal() as session:
    # Отримуємо список продуктів для користувача з tg_id
        tg_id = data.from_user.id
        query = (
            select(Product)
            .join(User)
            .where(User.tg_id == tg_id)
            .options(joinedload(Product.prices))  # Опціонально, щоб підвантажити пов'язані ціни
        )
        result = await session.execute(query)
        next_products = result.unique().scalars().all()
        
    if next_products:
        msg = await data.message.answer('Виберіть один з варіантів', reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(0.1)
        await msg.delete()
        
        # 11 - максимум можливих товарів щоб не сталась помилка (макс кнопок - 15)
        if len(next_products) <= 11:
            await data.message.answer(f'Виберіть один з варіантів', reply_markup=show_all_my_products_inl_kb(next_products))
        else:
            # Створюєм додаткові списки, між якими будем переміщати товари
            previous_products = [] 
            current_products = next_products[:11]
            next_products = next_products[11:]
            
            # Поміщаємо ці списки в FSM пам'ять, щоб потім їх отримати
            await state.update_data(next_products=next_products, current_products=current_products, previous_products=previous_products)
            
            await data.message.answer(f'Виберіть один з варіантів', reply_markup=show_all_my_products_inl_kb(current_products, next_page=True)) 
        
    else:
        await data.message.answer(f'У вас немає доданих товарів😔', reply_markup=main_rp_kb(data.from_user.id))
 
    
       
@view_router.callback_query(F.data == 'next_page', Product_review_form.product_review)
async def show_my_product(data: CallbackQuery, state: FSMContext):
    '''Хендлер для перегляду товарів на наступній сторінці'''
    await state.set_state(Product_review_form.product_review)
    await data.answer()
    
    # Отримуєм всі списки з пам'ять FSM
    state_data = await state.get_data()
    previous_products = state_data.get('previous_products')
    current_products = state_data.get('current_products')
    next_products = state_data.get('next_products')
    
    # Якщо <= 11 - значить це крайня сторінка
    if len(next_products) <= 11:
        
        previous_products = previous_products + current_products
        current_products = next_products[:]
        next_products = []
        
        await bot.edit_message_reply_markup(
            chat_id=data.message.chat.id,
            message_id=data.message.message_id,
            reply_markup=show_all_my_products_inl_kb(current_products, back_page=True))
        
    # Якщо > 11 значить є ще наступні сторінки
    else:
        previous_products = previous_products + current_products
        current_products = next_products[:11]
        next_products = next_products[11:]
        
        await bot.edit_message_reply_markup(
            chat_id=data.message.chat.id,
            message_id=data.message.message_id,
            reply_markup=show_all_my_products_inl_kb(current_products, next_page=True, back_page=True))
    
    # Оновлені списки додаєм до FSM пам'яті
    await state.update_data(next_products=next_products, current_products=current_products, previous_products=previous_products)



@view_router.callback_query(F.data == 'back_page', Product_review_form.product_review)
async def show_my_product(data: CallbackQuery, state: FSMContext):
    '''Хендлер для перегляду товарів на попередній сторінці'''
    await state.set_state(Product_review_form.product_review)
    await data.answer()
    
    # Отримуєм всі списки з пам'ять FSM
    state_data = await state.get_data()
    previous_products = state_data.get('previous_products')
    current_products = state_data.get('current_products')
    next_products = state_data.get('next_products')
    
    # Якщо <= 11 - значить це крайня сторінка
    if len(previous_products) <= 11:
        next_products = current_products + next_products
        current_products = previous_products[:]
        previous_products = []
        
        await bot.edit_message_reply_markup(
            chat_id=data.message.chat.id,
            message_id=data.message.message_id,
            reply_markup=show_all_my_products_inl_kb(current_products, next_page=True))
        
    # Якщо > 11 значить є ще попередні сторінки
    else:
        next_products = current_products + next_products
        current_products = previous_products[-11:]
        previous_products = previous_products[:-11]
        
        await bot.edit_message_reply_markup(
            chat_id=data.message.chat.id,
            message_id=data.message.message_id,
            reply_markup=show_all_my_products_inl_kb(current_products, next_page=True, back_page=True))
    
    # Оновлені списки додаєм до FSM пам'яті
    await state.update_data(next_products=next_products, current_products=current_products, previous_products=previous_products)
        
    

@view_router.callback_query(F.data == 'show_all_products')
async def show_all_products(data: CallbackQuery, state: FSMContext):
    '''Хендлер який виводить всю інформацію про всі товари користувача'''
    await state.clear()
    await data.answer()
    await data.message.delete()
    
    async with SessionLocal() as session:
    # Отримуємо список продуктів для користувача з tg_id
        tg_id = data.from_user.id
        query = (
            select(Product)
            .join(User)
            .where(User.tg_id == tg_id)
            .options(joinedload(Product.prices))  # Опціонально, щоб підвантажити пов'язані ціни
        )

        result = await session.execute(query)
        products = result.unique().scalars().all()
    
    text = '<b>Ось вся інформація про ваші товари</b>🧐:\n'
    
    for product in products:
        
        temp = await get_info_product(product)
        temp += '\n\n'
        
        if len(text + temp) >= 4096:
            await bot.send_message(chat_id=data.from_user.id, text=text)
            text = temp
        else:
            text += temp
    
    await bot.send_message(chat_id=data.from_user.id, text=text, reply_markup=main_rp_kb(data.from_user.id))
    


@view_router.callback_query(F.data.startswith('product_'))
async def show_user_product(data: CallbackQuery, state: FSMContext):
    '''Хендлер для виведення інформації про конкретний товар користувача'''
    
    await state.clear()
    await data.answer()
    await data.message.delete()
    
    product_id = int(data.data.replace('product_', ''))
    
    async with SessionLocal() as session:
        query = (
            select(Product)
            .join(User)
            .where(Product.product_id == product_id, User.tg_id == data.from_user.id)
            .options(joinedload(Product.prices))  # Опціонально підвантажуємо ціни
        )
        result = await session.execute(query)
        product = result.scalars().first()
        
    text = await get_text_for_one_product(product)
    
    await data.message.answer(text=text, reply_markup=product_control_inline_kb(product_id))


