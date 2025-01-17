import aiohttp
from typing import List, Tuple
from app.parser.silpo_parser import get_parse_silpo, get_parsed_changes_silpo
from app.parser.willmax_parser import get_parse_willmax, get_parsed_changes_willmax
from app.parser.rozetka_parser import get_parse_rozetka, get_parsed_changes_rozetka
from app.parser.avrora_parser import get_parse_avrora, get_parsed_changes_avrora
from app.parser.epicentr_parser import get_parse_epicentr, get_parsed_changes_epicentr
from app.parser.yabko_parser import get_parse_yabko, get_parsed_changes_yabko
from app.parser.staff_parser import get_parse_staff, get_parsed_changes_staff
from app.parser.shchodnya_parser import get_parse_shchodnya, get_parsed_changes_shchodnya
from app.parser.eva_parser import get_parse_eva, get_parsed_changes_eva
from app.parser.focstrot_parser import get_parse_focstrot, get_parsed_changes_focstrot
from app.models import Price, Product, User
from app.utils.work_with_database import add_new_product_to_db, get_all_products, delete_product_by_id, get_all_urls
from app.utils.work_with_aiohttp import get_gather
from app.utils.creating_text_about_user_products import get_update_data_text
from app.bot.create_bot import bot
from app.db import SessionLocal


async def add_new_product(url: str, store_name: str, tg_id: int) -> Tuple['int', 'str']:
    
    if store_name == 'rozetka': product, price = await get_parse_rozetka(url, tg_id)
    if store_name == 'willmax': product, price = await get_parse_willmax(url, tg_id)
    if store_name == 'silpo': product, price = await get_parse_silpo(url, tg_id)
    if store_name == 'avrora': product, price = await get_parse_avrora(url, tg_id)
    if store_name == 'epicentr': product, price = await get_parse_epicentr(url, tg_id)
    if store_name == 'yabko': product, price = await get_parse_yabko(url, tg_id)
    if store_name == 'staff': product, price = await get_parse_staff(url, tg_id)
    if store_name == 'shchodnya': product, price = await get_parse_shchodnya(url, tg_id)
    if store_name == 'focstrot': product, price = await get_parse_focstrot(url, tg_id)
    if store_name == 'eva': product, price = await get_parse_eva(url, tg_id)
    
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
        if store == 'Ябко': res = await get_parse_yabko(url, tg_id)
        if store == 'Staff': res = await get_parse_staff(url, tg_id)
        if store == 'Щодня': res = await get_parse_shchodnya(url, tg_id)
        if store == 'Фокстрот': res = await get_parse_focstrot(url, tg_id)
        if store == 'Eva': res = await get_parse_eva(url, tg_id)
            
    return res    


# dict{'store_name':(html_content, 'url',tg_id)}
async def get_update_product_data_with_content(data_for_parsing: dict) -> Tuple['Product','Price'] | None: 
    
    for store, content_url_tg_id in data_for_parsing.items():
        html_content, url, tg_id = content_url_tg_id
        
        if store == 'Rozetka': res = await get_parsed_changes_rozetka(html_content, url, tg_id)
        if store == 'Willmax': res = await get_parsed_changes_willmax(html_content, url, tg_id)
        if store == 'Сільпо': res = await get_parsed_changes_silpo(html_content, url, tg_id)
        if store == 'Аврора': res = await get_parsed_changes_avrora(html_content, url, tg_id)
        if store == 'Епіцентр': res = await get_parsed_changes_epicentr(html_content, url, tg_id)
        if store == 'Ябко': res = await get_parsed_changes_yabko(html_content, url, tg_id)
        if store == 'Staff': res = await get_parsed_changes_staff(html_content, url, tg_id)
        if store == 'Eva': res = await get_parsed_changes_eva(html_content, url, tg_id)
        if store == 'Щодня': res = await get_parsed_changes_shchodnya(html_content, url, tg_id)
        if store == 'Фокстрот': res = await get_parsed_changes_focstrot(html_content, url, tg_id)
            
    return res   
    

async def check_products_updates():
    
        print('\n<<< check_products_updates >>>\n')
        
        products = await get_all_products()
        all_urls = await get_all_urls()
        
        # Парсимо асинхроно всі сайти 
        urls_with_content = await get_gather(all_urls)
        
        for product in products:
            
            for url, html_content in urls_with_content:
            
                if url == product.url:
                    print('FIND')
                    # Якщо успішно спарсили
                    if html_content:
                        
                        last_price_obj = max(product.prices, key=lambda price: price.date)
                        max_price_obj = max(product.prices, key=lambda price: price.price)
                        min_price_obj = min(product.prices, key=lambda price: price.price)
                        

                        # Парсимо нову ціну з веб-сайту
                        _, new_price = await get_update_product_data_with_content({product.store_name: (html_content, product.url, product.tg_id)})
  
                        # _, new_price = res
                        
                        
                        # Якщо не можемо отримати всі дані | Наприклад коли в Епіцентрі товар закнчився, зникаються майже всі дані про нього
                        if new_price.price == 0.0 and new_price.discount == False and new_price.currency == None and new_price.unit_of_measure == None:
                            new_price.price = last_price_obj.price
                            new_price.currency = last_price_obj.currency
                            new_price.date = last_price_obj.date
                            new_price.unit_of_measure = last_price_obj.unit_of_measure
                            
                    
                        if (new_price.price != last_price_obj.price or new_price.price < min_price_obj.price 
                            or new_price.price > max_price_obj.price or new_price.discount != last_price_obj.discount
                            or new_price.status != last_price_obj.status):
                            
                            text = 'Дані про товар змінились‼️‼️\n'
                            print(f'---- Виявлено зміни: {product.product_name} ----\n')
                            
                            new_price.product = product
                            async with SessionLocal() as session:
                                session.add(new_price)
                                await session.commit()
                                
                            text += await get_update_data_text(product,last_price_obj, min_price_obj, max_price_obj, new_price) 
                            await bot.send_message(chat_id=product.tg_id, text=text)
                            
                    else: # Якщо отримали none, видаляємо товар з БД
                        await delete_product_by_id(product_id=product.product_id)
                        await bot.send_message(chat_id=product.tg_id, text=f'Товар: {product.product_name}, більше не доступний😢')
