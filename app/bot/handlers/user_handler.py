import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from app.bot.create_bot import admins
from app.db import SessionLocal
from app.models import User, Price, Product
from app.bot.keyboards.reply_keyboard import main_rp_kb
from app.bot.keyboards.inline_keyboard import inline_kb_store




user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    
    async with SessionLocal() as session:
        # Перевіряємо, чи існує користувач у таблиці Users
        user_query = select(User).where(User.tg_id == message.from_user.id)
        result = await session.execute(user_query)
        user_exists = result.scalar()  # Отримуємо користувача або None

        if not user_exists:
            # Додаємо нового користувача до таблиці Users
            new_user = User(tg_id=message.from_user.id, user_name=message.from_user.username)
            session.add(new_user)

            await message.answer(
                'Привіт👋\nВ цьому боті ти можеш відслідковувати ціни на свої товари в різних онлайн магазинах🤑 \
                \nКоли вони будуть падати або підніматися бот тебе про це повідомить👌', 
                reply_markup=ReplyKeyboardRemove()
            )
            await session.commit()
    
    await message.answer(f'Ось головне меню!', reply_markup=main_rp_kb(message.from_user.id))
    
    
@user_router.message(F.text == '🛍 Додати новий товар')
async def cmd_add_new_product(message:Message):
    msg = await message.answer('Виберіть онлайн магази🛒', reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(0.1)
    await msg.delete()

    await message.answer(f'Виберіть онлайн магази🛒', reply_markup=inline_kb_store())
    

@user_router.message(F.text == '❓ Про нас')
async def cmd_about_us(message: Message):
    await message.answer(f'Бот створений для спостереженям за цінами в різних онлайн магазинах')
    await message.answer(f'Бот поки що знаходиться в стадії розробки, якщо ви знайшли якись баг повідомте мене про це будь ласка'
                         , reply_markup=main_rp_kb(message.from_user.id))
    
    
@user_router.message(Command(commands=['info']))
async def cmd_about_us(message: Message):
    await message.answer(f'Бот створений для спостереженям за цінами в різних онлайн магазинах')
    await message.answer(f'Бот поки що знаходиться в стадії розробки, якщо ви знайшли якись баг повідомте мене про це будь ласка'
                         , reply_markup=main_rp_kb(message.from_user.id))
    

@user_router.message(Command(commands=['menu']))
async def cmd_menu(message: Message, state: FSMContext):
    '''Повернення на головне меню'''
    await state.clear()
    await message.answer(f'Ось головне меню!', reply_markup=main_rp_kb(message.from_user.id))
    
    

@user_router.callback_query(F.data == 'back_home')
async def cmd_on_main(data: CallbackQuery, state: FSMContext):
    '''Повернення на головне меню'''
    await state.clear()
    await data.answer()
    await data.message.delete()
    await data.message.answer(f'Ось головне меню!', reply_markup=main_rp_kb(data.from_user.id))
    
