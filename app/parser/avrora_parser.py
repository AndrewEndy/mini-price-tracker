import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class AvroraParser(BaseParser):
    async def parse(self, url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        html_content = await self.fetch_page(url)
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            product_name = soup.find('h1', class_='ty-product-block-title').text.strip()
            
            price_block = soup.find('div', class_='ty-product-prices')
            
            # Пошук акції
            discount = True if price_block.find('span', class_='ty-strike') else False
            
            # Пошук ціни та валюти 
            price_with_currency = price_block.find('div', class_='ty-product-block__price-actual').text.strip()
            
            currency = price_with_currency.split()[-1]
            price = float(''.join(price_with_currency.split()[:-1]))
            
            # Пошук статуса товара
            if soup.find('span', class_='ty-control-group__item'):
                status = soup.find('span', class_='ty-control-group__item').text.strip()
            else:
                status = None
            
            # print('--->' + product_name + '<---')
            # print('--->' + status + '<---')
            # print('--->' , discount , '<---')
            # print('--->' + currency + '<---')
            # print('--->' , price , '<---')
            
            
            price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=None)
            product_obj = Product(product_name=product_name, store_name='Аврора', url=url, tg_id=tg_id)
            
            # print(f'{product_obj}\n\n{price_obj}')
            
            # async with SessionLocal() as session:
            #     session.add(product)
            #     await session.commit()
                
            return product_obj, price_obj
        else:
            return None


async def get_parse_avrora(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = AvroraParser(session)
        res = await parser.parse(url, tg_id)
        return res


async def run_parsers(urls: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = AvroraParser(session)
        res = await parser.parse(urls, tg_id=123)
        print(res)
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://avrora.ua/multipich-liberton-laf-3202-hromovana-stal-z-chornim-1700-vt/"))
    # asyncio.run(run_parsers("https://123"))
    
