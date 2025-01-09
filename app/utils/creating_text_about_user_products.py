import datetime
from typing import List
from app.models import Price, Product, User


async def get_text_for_all_products(products: List['Product']) -> str:
    '''Функція для створення тексту про всі товари користувача'''
    
    text = '<b>Ось вся інформація про ваші товари</b>🧐:\n'
    for product in products:
        
        text += await get_info_product(product)
        text += '\n\n'
        
    return text


async def get_text_for_one_product(product: Product) -> str:
    '''Функція для створення тексту про товар користувача'''
    
    text = '<b>Ось інформація про цей товар</b>🧐:\n'
    
    text += await get_info_product(product)
        
    text += f'\n🔗<b>Посилання: </b> {product.url}\n\n'
        
    return text


async def get_update_data_text(product: Product, last_price_obj: Price, min_price_obj: Price, max_price_obj: Price, new_price_obj: Price) -> str:
    '''Функція для створення тексту з оновленими даними'''
    
    text = '<b>Ось Оновлені дані товару</b>🙌:\n'
    
    currency = '' if not last_price_obj.currency else last_price_obj.currency
    
    text = f'''\n🛒<b>Магазин:</b> {product.store_name}\n📝<b>Назва товара:</b> {product.product_name}\n'''
    unit_of_measure = None if not new_price_obj.unit_of_measure or new_price_obj.unit_of_measure == 'шт.' else new_price_obj.unit_of_measure
    status = new_price_obj.status
    
    if unit_of_measure: text += f'<b>Об\'єм:</b> {unit_of_measure}\n'
    
    if last_price_obj.price != new_price_obj.price:
        text += f'''💸<b>Остання ціна:</b> <s>{last_price_obj.price} {currency}</s> ➡️ {new_price_obj.price} {currency}\n'''
        text += f'''🗓️<b>Остання дата змін:</b> {str(new_price_obj.date.date())}\n'''
    else:
        text += f'''💸<b>Остання ціна:</b> {last_price_obj.price} {currency}\n🗓️<b>Остання дата змін:</b> {str(last_price_obj.date.date())}\n'''
    
    if min_price_obj.price > new_price_obj.price:
        text += f'''\n📉<b>Мінімальна ціна:</b> <s>{min_price_obj.price} {currency}</s> ➡️ {new_price_obj.price} {currency}\n'''
        text += f'''🗓️<b>Остання дата змін:</b> {str(new_price_obj.date.date())}\n'''
    else:
        text+=f'\n📉<b>Мінімальна ціна:</b> {min_price_obj.price} {currency}\n🗓️<b>Остання дата змін:</b> {str(min_price_obj.date.date())}\n'
    
    if max_price_obj.price < new_price_obj.price:
        text += f'''\n📈<b>Максимальна ціна:</b> <s>{max_price_obj.price} {currency}</s> ➡️ {new_price_obj.price} {currency}\n'''
        text += f'''🗓️<b>Остання дата змін:</b> {str(new_price_obj.date.date())}\n'''
    else:
        text+=f'\n📈<b>Максимальна ціна:</b> {max_price_obj.price} {currency}\n🗓️<b>Остання дата змін:</b> {str(max_price_obj.date.date())}\n'
        
    if status:
        text += f'\n<b>📍Статус: </b>{status}\n'
        
    if new_price_obj.discount:
        text+=f'\n‼️<b>На товар діє знижка</b>‼️\n'
    
    text += f'\n🔗<b>Посилання: </b> {product.url}\n\n'
    
    return text


async def get_info_product(product: Product) -> str:
    # Остання ціна за датою
    last_price_obj = max(product.prices, key=lambda price: price.date)
    last_price = last_price_obj.price
    last_date = last_price_obj.date

    # Максимальна ціна
    max_price_obj = max(product.prices, key=lambda price: price.price)
    max_price = max_price_obj.price
    max_price_date = max_price_obj.date

    # Мінімальна ціна
    min_price_obj = min(product.prices, key=lambda price: price.price)
    min_price = min_price_obj.price
    min_price_date = min_price_obj.date
        
    currency = '' if not last_price_obj.currency else last_price_obj.currency
    unit_of_measure = None if not last_price_obj.unit_of_measure or last_price_obj.unit_of_measure == 'шт.' else last_price_obj.unit_of_measure
    status = last_price_obj.status
    
    text = f'''\n🛒<b>Магазин:</b> {product.store_name}\n📝<b>Назва товара:</b> {product.product_name}\n'''
    
    if unit_of_measure: text += f'<b>Об\'єм:</b> {unit_of_measure}\n'
    
    text += f'''\n💸<b>Остання ціна:</b> {last_price} {currency}\n🗓️<b>Остання дата змін:</b> {str(last_date.date())}\n'''
    
    if last_price != min_price:
            text+=f'\n📉<b>Мінімальна ціна:</b> {min_price} {currency}\n🗓️<b>Остання дата змін:</b> {str(min_price_date.date())}\n'
        
    if last_price != max_price:
        text+=f'\n📈<b>Максимальна ціна:</b> {max_price} {currency}\n🗓️<b>Остання дата змін:</b> {str(max_price_date.date())}\n'
        
    if status:
        text += f'\n<b>📍Статус: </b>{status}\n'
        
    if last_price_obj.discount:
        text+=f'\n‼️<b>На товар діє знижка</b>‼️\n'
    return text