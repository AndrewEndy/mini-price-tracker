import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class MoyoParser(BaseParser):
    async def parse(self, html_content , url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_name = soup.find('h1', class_='product_name').text.strip()
        
        # Пошук статуса товара
        # Пошук "В наявності" або "Закінчується"
        if soup.find('div', class_='product_availability_status instock-status'):
            status = soup.find('div', class_='product_availability_status instock-status').text.strip()
            if status == 'Есть в наличии': status = 'Є в наявності' 
            if status == 'Заканчивается': status = 'Закінчується'
        # Пошук "Немає в наявності"
        elif soup.find('div', class_='product_availability_status noinstock-status'):
            status = soup.find('div', class_='product_availability_status noinstock-status').text.strip()
            if status == 'Товар закончился': status = 'Товар закінчився'
        else:
            status = None
       
        # Пошук ціни, знижки, валюти
        price_block = soup.find('div', class_='product_price')
        
        discount = True if price_block.find('div', class_='product_price_oldprice js-old-price') else False
        if discount:
            price_with_currency = price_block.find('div', class_='product_price_current sale js-current-price').text.strip()
        else:
            price_with_currency = price_block.find('div', class_='product_price_current js-current-price').text.strip()
            
        currency = price_with_currency.split()[-1]
        price = float(''.join(price_with_currency.replace(',', '.').split()[:-1]))
        
        
        
        # print('--->' + product_name + '<---')
        # print('--->' + str(status) + '<---')
        # print('--->' + str(discount) + '<---')
        # print('--->' + str(price) + '<---')
        # print('--->' + str(currency) + '<---')
        
        
        
        price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=None)
        product_obj = Product(product_name=product_name, store_name='MOYO', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_moyo(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = MoyoParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_moyo(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = MoyoParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = MoyoParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://www.moyo.ua/ua/oral-b_zubnaya_shchetka_pro_expert_vse_v_odnom_40_srednyaya_1_1sht/524960.html"))
    # asyncio.run(run_parsers("https://123"))
    
