import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class RozetkaParser(BaseParser):
    async def parse(self, url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        html_content = await self.fetch_page(url)
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            product_name = soup.find('h1', class_='title__font ng-star-inserted').text.strip()
            
            price_and_status_block = soup.find('div', class_='product-price__wrap ng-star-inserted')
        
            # Пошук статуса товара
            if price_and_status_block.find('p', class_='status-label status-label--green ng-star-inserted'):
                status = 'Є в наявності'
            elif price_and_status_block.find('p', class_='status-label status-label--orange ng-star-inserted'):
                status = 'Закінчується'
            elif price_and_status_block.find('p', class_='status-label status-label--gray ng-star-inserted'):
                status = 'Немає в наявності'
            else:
                status = None
                
            
            # Пошук акції
            discount = True if price_and_status_block.find('p', class_ = 'product-price__small ng-star-inserted') else False
            
            # Пошук тексту ціни та валюти з акцією і без
            if discount:
                price_with_currency_text = price_and_status_block.find('p', class_='product-price__big product-price__big-color-red').text.strip()
            else:
                price_with_currency_text = price_and_status_block.find('p', class_='product-price__big').text.strip()
                
            currency = 'грн' if price_with_currency_text[-1] == '₴' else price_with_currency_text[-1]
            
            price = float(''.join(price_with_currency_text[:-1].split()))
            
            
            # print('--->' + product_name + '<---')
            # print('--->' + status + '<---')
            # print('--->' , discount , '<---')
            # print('--->' + currency + '<---')
            # print('--->' , price , '<---')
            
            
            price_obj = Price(price=price, currency=currency, discount=discount, status=status)
            product_obj = Product(product_name=product_name, store_name='Rozetka', url=url, tg_id=tg_id)
            
            # print(f'{product_obj}\n\n{price_obj}')
            
            # async with SessionLocal() as session:
            #     session.add(product)
            #     await session.commit()
                
            return product_obj, price_obj
        else:
            return None


async def get_parse_rozetka(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = RozetkaParser(session)
        res = await parser.parse(url, tg_id)
        return res


async def run_parsers(urls: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = RozetkaParser(session)
        res = await parser.parse(urls, tg_id=123)
        print(res)
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://hard.rozetka.com.ua/gigabyte-gv-n4060wf2oc-8gd/p385179081/"))
    # asyncio.run(run_parsers("https://123"))
    
