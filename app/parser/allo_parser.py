import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class AlloParser(BaseParser):
    async def parse(self, html_content , url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_name = soup.find('h1', class_='p-view__header-title').text.strip()
        
        # Пошук статуса товара
        if soup.find('p', class_='p-trade__stock-label'):
            status = ' '.join(soup.find('p', class_='p-trade__stock-label').text.strip().split()[:])
            if status[0] == '✓': status = status[2:]
            
            if status == 'Товар в наличии': status = 'Товар в наявності'
            if status == 'Нет в наличии': status = 'Немає в наявності'
        else:
            status = None

        # Якщо немає price_block - немає достатньо інформації про товар
        if soup.find('div', class_='p-trade__price p-trade-price'):
            # Пошук ціни, знижки, валюти
            price_block = soup.find('div', class_='p-trade__price p-trade-price')
            
            discount = True if price_block.find('div', class_='p-trade-price__old') else False
            
            if discount:
                price_text = price_block.find('div', class_='p-trade-price__current p-trade-price__current--discount').text.strip()
                currency = price_block.find('div', class_='p-trade-price__current p-trade-price__current--discount').find('span', class_='currency').text.strip()
            else:
                price_text = price_block.find('div', class_='p-trade-price__current').text.strip()
                currency = price_block.find('div', class_='p-trade-price__current').find('span', class_='currency').text.strip()
                
            price = float(''.join(price_text.replace(',','.').split(currency)[0].split()[:]))
            currency = 'грн' if currency == '₴' else currency
            
        else:
            # Якщо немає даних
            discount = False
            price = 0.0
            currency = None
            unit_of_measure = None
        
        
        
        # print('--->' + product_name + '<---')
        # print('--->' + str(status) + '<---')
        # print('--->' + str(discount) + '<---')
        # print('--->' + str(price) + '<---')
        # print('--->' + str(currency) + '<---')
        
        
        
        price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=None)
        product_obj = Product(product_name=product_name, store_name='Алло', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_allo(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = AlloParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_allo(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = AlloParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = AlloParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://allo.ua/ua/products/mobile/apple-iphone-12-64gb-white-mgj63-4.html"))
    # asyncio.run(run_parsers("https://123"))
    
