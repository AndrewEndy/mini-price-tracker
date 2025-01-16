import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class EvaParser(BaseParser):
    async def parse(self, html_content , url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_name = soup.find('h1', class_='sf-heading__title').text.strip()
        
        # Пошук статуса
        if soup.find('div', class_='a-product-stock'):
            status = soup.find('div', class_='a-product-stock').text.strip()
            
            if status == 'В наличии':
                status = 'В наявності'
            elif status == 'Нет в наличии':
                status = 'Немає в наявності'
        else:
            status = None
        
        # Якщо статус = "Немає в наявності" - на сторінці відсутні майже всі дані про товар
        if status != 'Немає в наявності':
    
            price_block = soup.find('div', class_='sf-price')
            
            discount = True if not price_block.find('span', class_='sf-price__regular') else False
            
            if discount:
                price_with_currency = price_block.find('ins', class_='sf-price__special').text.strip()
            else:
                price_with_currency = price_block.find('span', class_='sf-price__regular').text.strip()
            
            currency = 'грн' if price_with_currency.split()[-1] == '₴' else price_with_currency.split()[-1]
            price = float(''.join(price_with_currency.replace(',','.').split()[:-1]))
                  
        else:
            discount = False
            price = 0.0
            currency = None
        
        
        
        # print('--->' + product_name + '<---')
        # print('--->' + str(status) + '<---')
        # print('--->' + str(discount) + '<---')
        # print('--->' + str(price) + '<---')
        # print('--->' + str(currency) + '<---')
        
        
        
        price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=None)
        product_obj = Product(product_name=product_name, store_name='Eva', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_eva(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = EvaParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_eva(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = EvaParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = EvaParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://eva.ua/ua/pr451382/"))
    # asyncio.run(run_parsers("https://123"))
    
