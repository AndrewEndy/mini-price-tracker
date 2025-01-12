import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal





class WillmaxParser(BaseParser):
    async def parse(self, url: str, tg_id: int) -> Product:
        html_content = await self.fetch_page(url)
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            discount = False
            
            product_name = soup.find('div', class_='title-product').text.strip()
            
            price_block = soup.find('div', class_='product_page_price price')
            
            # Отримання даних якщо товар акційний
            if(price_block.find('span', id = 'price-special')): 
                discount = True
                price_with_currency = price_block.find('span', id = 'price-special').text.strip().split(' ') 
                
                if(len(price_with_currency) == 3):
                    price = float(price_with_currency[0]+price_with_currency[1])
                else:
                    price = float(price_with_currency[0])
                    
                currency = price_with_currency[-1][:-1]
                
            else: # Отримання даних якщо товар НЕ акційний
                price_with_currency = price_block.find('span', id = 'price-old').text.strip().split(' ')
                
                if(len(price_with_currency) == 3):
                    price = float(price_with_currency[0]+price_with_currency[1])
                else:
                    price = float(price_with_currency[0])
                
                currency = price_with_currency[-1][:-1]
                    
                    
                    
            # print('--->' + product_name + '<---')
            # print('--->' + str(price) + '<---')
            # print('--->' + currency + '<---')
            # print('--->' , discount , '<---')
            
            
            price_obj = Price(price=price, currency=currency, discount=discount, status=None, unit_of_measure=None)
            product_obj = Product(product_name=product_name, store_name='Willmax', url=url, tg_id=tg_id)
            
            # async with SessionLocal() as session:
            #     session.add(product)
            #     await session.commit()
            
            return product_obj, price_obj
        else:
            return None


async def get_parse_willmax(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = WillmaxParser(session)
        res = await parser.parse(url, tg_id)
        return res


async def run_parsers(urls: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = WillmaxParser(session)
        res = await parser.parse(urls, tg_id=123)
        print(res)

if __name__ == "__main__":
    asyncio.run(run_parsers("https://www.willmax.com.ua/mass-gainer-2kg-shokolad"))
    