import aiohttp
from typing import List, Tuple
from app.parser.silpo_parser import get_parse_silpo 
from app.parser.willmax_parser import get_parse_willmax
from app.parser.rozetka_parser import get_parse_rozetka
from app.parser.avrora_parser import get_parse_avrora
from app.parser.epicentr_parser import get_parse_epicentr
from app.models import Price, Product, User
from app.utils.work_with_database import add_new_product_to_db, get_all_products, delete_product_by_id
from app.utils.creating_text_about_user_products import get_update_data_text
from app.bot.create_bot import bot
from app.db import SessionLocal


async def add_new_product(url: str, store_name: str, tg_id: int) -> Tuple['int', 'str']:
    
    if store_name == 'rozetka': product, price = await get_parse_rozetka(url, tg_id)
    if store_name == 'willmax': product, price = await get_parse_willmax(url, tg_id)
    if store_name == 'silpo': product, price = await get_parse_silpo(url, tg_id)
    if store_name == 'avrora': product, price = await get_parse_avrora(url, tg_id)
    if store_name == 'epicentr': product, price = await get_parse_epicentr(url, tg_id)
    
    # Якщо не можемо отримати всі дані | Наприклад коли в Епіцентрі товар закнчився, зникаються майже всі дані про нььго
    if price.price == 0.0 and price.discount == False and price.currency == None and price.unit_of_measure == None: return 0, ''

    print(product, price)
    product.prices.append(price)
    await add_new_product_to_db(product)
    return product.product_id, product.product_name
        


async def get_updated_product_data(data_for_parsing : dict) -> Tuple['Product','Price'] | None: # dict{'store_name':('url',tg_id)}
    
    for store, urls_with_tg_id in data_for_parsing.items():
        url, tg_id = urls_with_tg_id
        
        if store == 'Rozetka': res = await get_parse_rozetka(url, tg_id)
        if store == 'Willmax': res = await get_parse_willmax(url, tg_id)
        if store == 'Сільпо': res = await get_parse_silpo(url, tg_id)
        if store == 'Аврора': res = await get_parse_avrora(url, tg_id)
        if store == 'Епіцентр': res = await get_parse_epicentr(url, tg_id)
            
    return res    
    

async def check_products_updates():

        products = await get_all_products()

        print('\n<<< check_products_updates >>>\n')
        
        for product in products:
            
            last_price_obj = max(product.prices, key=lambda price: price.date)
            max_price_obj = max(product.prices, key=lambda price: price.price)
            min_price_obj = min(product.prices, key=lambda price: price.price)
            

            # Парсимо нову ціну з веб-сайту
            res = await get_updated_product_data({product.store_name: (product.url, product.tg_id)})
    
            if res:
                
                _, new_price = res
            
                if (new_price.price != last_price_obj.price or new_price.price < min_price_obj.price 
                    or new_price.price > max_price_obj.price or new_price.discount != last_price_obj.discount
                    or new_price.status != last_price_obj.status):
                    
                    text = 'Дані про товар змінились‼️‼️\n'
                    
                    new_price.product = product
                    async with SessionLocal() as session:
                        session.add(new_price)
                        await session.commit()
                        
                    text += await get_update_data_text(product,last_price_obj, min_price_obj, max_price_obj, new_price) 
                    await bot.send_message(chat_id=product.tg_id, text=text)
                
            else: # Якщо отримали none, видаляємо товар з БД
                await delete_product_by_id(product_id=product.product_id)
                await bot.send_message(chat_id=product.tg_id, text=f'Товар: {product.product_name}, більше не доступний😢')
