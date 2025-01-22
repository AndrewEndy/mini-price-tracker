import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class FocstrotParser(BaseParser):
    async def parse(self, html_content , url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_name = soup.find('h1', class_='page__title overflow').text.strip()
        
        # Пошук статуса
        if soup.find('div', class_='product-box__heading').find('div'):
            status = soup.find('div', class_='product-box__heading').find('div').text.strip()
            
            if status == 'В наличии': status = 'В наявності'
            if status == 'Заканчивается': status = 'Закінчується'
            if status == 'Нет в наличии': status = 'Немає в наявності'
        else:
            status = None
            
        # Якщо статус "Немає в наявності" або можуть бути дані про товар або ні    
        if status != 'Немає в наявності':
            # Пошук ціни, знижки, валюти
            price_block = soup.find('div', class_='product-box__main_price-wrapper')
            
            discount = True if price_block.find('div', class_='discount-item') else False
            price_with_currency = price_block.find('div', class_='product-box__main_price').text.strip()
            
            currency = 'грн' if price_with_currency.split()[-1] == '₴' else price_with_currency.split()[-1]
            price = float(''.join(price_with_currency.split()[:-1]))
        
        else:
            # Якщо є дані про товар
            if soup.find('div', class_='product-box__main_price-wrapper'):
                # Пошук ціни, знижки, валюти
                price_block = soup.find('div', class_='product-box__main_price-wrapper')
            
                discount = True if price_block.find('div', class_='discount-item') else False
                price_with_currency = price_block.find('div', class_='product-box__main_price arhive-price').text.strip()
                
                currency = 'грн' if price_with_currency.split()[-1] == '₴' else price_with_currency.split()[-1]
                price = float(''.join(price_with_currency.split()[:-1]))
            
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
        product_obj = Product(product_name=product_name, store_name='Фокстрот', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_focstrot(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = FocstrotParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_focstrot(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = FocstrotParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = FocstrotParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://www.foxtrot.com.ua/uk/shop/planshetiy-apple-ipad-air-109-4-gen-wi-fi-64gb-space-grey.html"))
    # asyncio.run(run_parsers("https://123"))
    
