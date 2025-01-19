import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class ShafaParser(BaseParser):
    async def parse(self, html_content , url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_name = soup.find('h1', class_='b-product__title').text.strip()
        
        # Блок з ціною, валютою
        price_block = soup.find('div', class_='b-product-price')
        
        # Якщо товар безкоштовний
        if price_block.find('span', class_='b-product-price__gift'):
            status = 'У подарунок'
            discount = False
            price = 0.0
            currency = None
            
        else:
            # Пошук ціни, знижки, валюти
            discount = True if price_block.find('span', class_='b-product-price__old') else False
            price_with_currency = price_block.find('span', class_='b-product-price__current').text.strip()
            
            currency = price_with_currency.split()[-1]
            price = float(''.join(price_with_currency.replace(',','.').split()[:-1]))
            
            status = None
        
        
        
        # print('--->' + product_name + '<---')
        # print('--->' + str(status) + '<---')
        # print('--->' + str(discount) + '<---')
        # print('--->' + str(price) + '<---')
        # print('--->' + str(currency) + '<---')
        
        
        
        price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=None)
        product_obj = Product(product_name=product_name, store_name='Shafa', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_shafa(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = ShafaParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_shafa(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = ShafaParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = ShafaParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://shafa.ua/uk/women/nizhnee-bele-i-kupalniki/portupei/100442029-portupeya-na-grudi-strepi-konturniy-lif"))
    # asyncio.run(run_parsers("https://123"))
    
