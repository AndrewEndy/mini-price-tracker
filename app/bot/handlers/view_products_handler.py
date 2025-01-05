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
from app.bot.create_bot import admins, bot
from app.bot.keyboards.reply_keyboard import main_rp_kb
from app.bot.keyboards.inline_keyboard import back_home_and_show_my_products_inline_kb, show_all_my_products_inl_kb, product_control_inline_kb
from app.bot.fsm.form_fsm import Change_name_form
from app.utils.creating_text_about_user_products import get_text_for_all_products, get_text_for_one_product, get_update_data_text



view_router = Router()


# -----Переглянути мої товари-----  

# *** Показати мої товари ***  

@view_router.message(F.text == '👀 Переглянути мої товари')
async def show_my_products(message: Message):
    '''Хендлер для перегляду товарів користувача'''
    
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
        products = result.unique().scalars().all()  
        
    if products:
        msg = await message.answer('Виберіть один з варіантів', reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(0.1)
        await msg.delete()

        await message.answer(f'Виберіть один з варіантів', reply_markup=show_all_my_products_inl_kb(products))
    else:
        await message.answer(f'У вас немає доданих товарів😔', reply_markup=main_rp_kb(message.from_user.id))
    
    
@view_router.callback_query(F.data == 'show_my_products')
async def show_my_products(data: CallbackQuery):
    '''Хендлер для перегляду товарів користувача'''
    
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
        
    if products:
        msg = await data.message.answer('Виберіть один з варіантів', reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(0.1)
        await msg.delete()

        await data.message.answer(f'Виберіть один з варіантів', reply_markup=show_all_my_products_inl_kb(products))
    else:
        await data.message.answer(f'У вас немає доданих товарів😔', reply_markup=main_rp_kb(data.from_user.id))


@view_router.callback_query(F.data == 'show_all_products')
async def show_all_products(data: CallbackQuery):
    '''Хендлер який виводить всю інформацію про всі товари користувача'''
    
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
        
    text = await get_text_for_all_products(products)
    
    await data.message.answer(text=text, reply_markup=main_rp_kb(data.from_user.id))
    

@view_router.callback_query(F.data.startswith('product_'))
async def show_user_product(data: CallbackQuery):
    '''Хендлер для виведення інформації про конкретний товар користувача'''
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


