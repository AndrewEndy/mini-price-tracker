import aiohttp
from typing import List, Tuple
from app.parser.silpo_parser import SilpoParser, get_parse_silpo 
from app.parser.willmax_parser import WillmaxParser
from app.models import Price, Product, User
from app.utils.work_with_database import add_new_product_to_db


async def add_new_product(url: str, store_name: str, tg_id: int) -> int:
    
    if store_name == 'silpo':
        product, price = await get_parse_silpo(url, tg_id)
        # product, price = product_and_price
        product.prices.append(price)
        await add_new_product_to_db(product)
        return product.product_id, product.product_name
        


async def update_product_data(data_for_parsing : dict) -> List[Tuple['Product','Price']]: # dict{'store_name':[('url',tg_id),]}
    
    products_and_prices = []
    
    for store, urls_with_tg_id in data_for_parsing.items():
        
        if store == 'Rozetka':
            pass
        
        if store == 'Willmax':
            for url, tg_id in urls_with_tg_id:
                async with aiohttp.ClientSession() as session:
                    parser = WillmaxParser(session)
                    res = await parser.parse(url, tg_id)
                
                products_and_prices.append(res)
        
        if store == 'Сільпо':
            for url, tg_id in urls_with_tg_id:
                res = await get_parse_silpo(url, tg_id)
                products_and_prices.append(res)
            
    return products_and_prices    
    


