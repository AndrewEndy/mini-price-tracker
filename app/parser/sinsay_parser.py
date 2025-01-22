import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal
import json


class SinsayParser(BaseParser):
    async def parse(self, html_content, url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        script_tag = soup.find('script', type='application/ld+json')

        # print(script_tag)

        if script_tag:
    
            data = json.loads(script_tag.string)
            
            # Отримуємо потрібні дані
            product_name = data.get('name')
            currency = data.get('offers', {}).get('priceCurrency')
            price = float(data.get('offers', {}).get('price'))
            
            if product_name and price and currency:
                status = None
                discount = False
            else:
                discount = False
                price = 0.0
                currency = None

        else:
            discount = False
            price = 0.0
            currency = None
        
                
        
        
        # print('--->' + product_name + '<---')
        # print('--->' + str(status) + '<---')
        # print('--->' + str(discount) + '<---')
        # print('--->' + currency + '<---')
        # print('--->' + str(price) + '<---')
        
        
        price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=None)
        product_obj = Product(product_name=product_name, store_name='Sinsay', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_sinsay(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = SinsayParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_sinsay(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = SinsayParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = SinsayParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        print(res)
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://www.sinsay.com/ua/uk/chokhol-dlia-iphone-12-12-pro-5099z-09x"))
    # asyncio.run(run_parsers("https://123"))
    
