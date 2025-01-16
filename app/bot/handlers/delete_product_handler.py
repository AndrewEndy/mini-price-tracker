import asyncio
from aiogram import Router, F
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from app.db import SessionLocal
from app.models import Product, Price, User
from app.bot.create_bot import admins, bot
from app.bot.keyboards.reply_keyboard import main_rp_kb
from app.bot.keyboards.inline_keyboard import back_home_and_show_my_products_inline_kb, show_all_my_products_inl_kb, product_control_inline_kb
from app.utils.creating_text_about_user_products import get_update_data_text
from app.utils.work_with_database import delete_product_by_id

delete_product_router = Router()


@delete_product_router.callback_query(F.data.startswith('delete_product_'))
async def update_product_data(data: CallbackQuery):
    '''Хендлер який видаляє товар'''
    
    async with ChatActionSender.typing(bot=bot, chat_id=data.from_user.id):
        
        await asyncio.sleep(1)
        
        await data.answer()
        await data.message.delete()

        product_id = int(data.data.replace('delete_product_', '')) # Отримання product_id з callback query 
        
        await delete_product_by_id(product_id=product_id)
        await data.message.answer('Товар видалено🗑️', reply_markup=main_rp_kb(data.from_user.id))