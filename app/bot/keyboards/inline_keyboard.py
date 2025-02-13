from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.models import Price, Product, User


def inline_kb_store() -> InlineKeyboardMarkup:
    '''Inline клавіатура з вибором різних інтернет магазинів'''
    inline_kb_list = [
        [InlineKeyboardButton(text='Rozetka', callback_data='store_rozetka'), InlineKeyboardButton(text='Сільпо', callback_data='store_silpo')],
        [InlineKeyboardButton(text='Willmax', callback_data='store_willmax'), InlineKeyboardButton(text='Аврора', callback_data='store_avrora')],
        [InlineKeyboardButton(text='Епіцентр', callback_data='store_epicentr'), InlineKeyboardButton(text='Ябко', callback_data='store_yabko')],
        [InlineKeyboardButton(text='Staff', callback_data='store_staff'), InlineKeyboardButton(text='Щодня', callback_data='store_shchodnya')],
        [InlineKeyboardButton(text='Eva', callback_data='store_eva'), InlineKeyboardButton(text='Фокстрот', callback_data='store_focstrot')],
        [InlineKeyboardButton(text='MOYO', callback_data='store_moyo'), InlineKeyboardButton(text='Алло', callback_data='store_allo')],
        [InlineKeyboardButton(text='Kasta', callback_data='store_kasta'), InlineKeyboardButton(text='Prom', callback_data='store_prom')],
        [InlineKeyboardButton(text='Shafa', callback_data='store_shafa'), InlineKeyboardButton(text='Jusk', callback_data='store_jusk')],
        [InlineKeyboardButton(text='Sinsay', callback_data='store_sinsay') ],
        [InlineKeyboardButton(text='«Назад', callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def back_home_inline_kb() -> InlineKeyboardMarkup: 
    '''Inline клавіатура з кнопкою яка переносить в головне меню'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='«На головну', callback_data='back_home')]])


def check_name_product_inline_kb(product_id: int) -> InlineKeyboardMarkup:
    '''Inline клавіатура для перевірки чи підходить назва товара'''
    return InlineKeyboardMarkup(inline_keyboard=
                                [[InlineKeyboardButton(text='Завершити', callback_data='end_add_product'), 
                                  InlineKeyboardButton(text='Змінити назву', callback_data=f'change_name_{product_id}')]]
                                )


def show_all_my_products_inl_kb(products: List['Product'], next_page=False, back_page=False) -> InlineKeyboardBuilder:
    '''Стоворення Inline клавіатури з усіма товарами користувача'''
    
    builder = InlineKeyboardBuilder()
    
    for product in products:
        builder.row(
            InlineKeyboardButton(
                text=product.product_name,
                callback_data=f'product_{product.product_id}'
            )
        )
        
    # Додаєм кнопку "Переглянути всі" 
    builder.row(
        InlineKeyboardButton(
            text='--- Переглянути всі ---',
            callback_data='show_all_products'
        )
    )
        
    # Додаєм кнопку "На головну"
    builder.row(
        InlineKeyboardButton(
            text='--- На головну ---',
            callback_data='back_home'
        )
    )
    
    
    # Додаєм кнопку "Наступна сторінка"
    if next_page:
        builder.row(
            InlineKeyboardButton(
                text='Наступна сторінка >>',
                callback_data='next_page'
            )
        )
        
        
    # Додаєм кнопку "Попередня сторінка"
    if back_page:
        builder.row(
            InlineKeyboardButton(
                text='<< Попередня сторінка',
                callback_data='back_page'
            )
        )
    
    # Налаштовуєм розмір клавіатури
    builder.adjust(1)
    return builder.as_markup()


def product_control_inline_kb(product_id: int) -> InlineKeyboardMarkup:
    '''Inline клавіатура для кнопок для керуванням конкретним товаром'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оновити дані', callback_data=f'update_status_{product_id}')],
                                                  [InlineKeyboardButton(text='Змінити назву', callback_data=f'change_name_{product_id}')],
                                                  [InlineKeyboardButton(text='Видалити товар', callback_data=f'delete_product_{product_id}')],
                                                  [InlineKeyboardButton(text='На головну', callback_data='back_home')],
                                                  [InlineKeyboardButton(text='Назад', callback_data='show_my_products')]
                                                  ])


def back_home_and_show_my_products_inline_kb() -> InlineKeyboardMarkup:
    '''Inline клавіатура з кнопками на головну і переглянути мої товари'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='На головну', callback_data='back_home')], 
                                                 [InlineKeyboardButton(text='Назад', callback_data='show_my_products')]
                                                 ])