from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from app.bot.create_bot import admins


def main_rp_kb(user_telegram_id: int): 
    kb_list = [
        [KeyboardButton(text='🛍 Додати новий товар')],
        [KeyboardButton(text='👀 Переглянути мої товари')],
        [KeyboardButton(text='❓ Про нас')]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
        
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
