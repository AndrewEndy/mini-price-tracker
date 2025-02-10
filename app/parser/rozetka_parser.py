import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class RozetkaParser(BaseParser):
    async def parse(self, html_content, url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_name = soup.find('h1', class_='title__font').text.strip()
        
        price_and_status_block = soup.find('div', class_='product-price__wrap')
    
        # Пошук статуса товара
        if price_and_status_block.find('p', class_='status-label status-label--green'):
            status = 'Є в наявності'
        elif price_and_status_block.find('p', class_='status-label status-label--orange'):
            status = 'Закінчується'
        elif price_and_status_block.find('p', class_='status-label status-label--gray'):
            status = 'Немає в наявності'
        else:
            status = None
            
        
        # Пошук акції
        discount = True if price_and_status_block.find('p', class_ = 'product-price__small') else False
        
        # Пошук тексту ціни та валюти з акцією і без
        if discount:
            price_with_currency_text = price_and_status_block.find('p', class_='product-price__big product-price__big-color-red').text.strip()
        else:
            price_with_currency_text = price_and_status_block.find('p', class_='product-price__big').text.strip()
            
        currency = 'грн' if price_with_currency_text[-1] == '₴' else price_with_currency_text[-1]
        
        price = float(''.join(price_with_currency_text[:-1].split()))
        
        
        # print('--->' + product_name + '<---')
        # print('--->' + str(status) + '<---')
        # print('--->' , discount , '<---')
        # print('--->' + str(currency) + '<---')
        # print('--->' , price , '<---')
        
        
        price_obj = Price(price=price, currency=currency, discount=discount, status=status)
        product_obj = Product(product_name=product_name, store_name='Rozetka', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_rozetka(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = RozetkaParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_rozetka(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = RozetkaParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = RozetkaParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        print(res)
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://rozetka.com.ua/ua/klub-simeynogo-dozvillya-9786171283510/p440639588/"))
    # asyncio.run(run_parsers("https://123"))
    
