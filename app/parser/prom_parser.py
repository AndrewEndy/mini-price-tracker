import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class PromParser(BaseParser):
    async def parse(self, html_content , url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_name = soup.find('h1', class_='_3Trjq F7Tdh vj3pM htldP').text.strip()
        
        # Пошук статуса
        # Пошук "В наявності" або "Готово до відправки"
        if soup.find('span', class_='_3Trjq aXB7S NSmdF'):
            status = soup.find('span', class_='_3Trjq aXB7S NSmdF').text.strip()
            
            if status == 'Готово к отправке': status = 'Готово до відправки'
            if status == 'В наличии': status = 'В наявності'
        
        # Пошук "Під заказ..."
        elif soup.find('span', class_='_3Trjq aXB7S etfhZ'):
            status = soup.find('span', class_='_3Trjq aXB7S etfhZ').text.strip()
            
        # Пошук "Недоступно"
        elif soup.find('span', class_='_3Trjq ffgjE IfSYo f8ZGq'):
            status = soup.find('span', class_='_3Trjq ffgjE IfSYo f8ZGq').text.strip()
        else:
            status = None
            
        
        if status != 'Недоступний':
            # Пошук ціни, знижки, валюти
            price_block = soup.find('div', class_='tqUsL')
            
            discount = True if price_block.find('div', class_='DdMjM') else False
            
            if discount:
                price_with_currency = price_block.find('div', class_='IP36L bkjEo').text.strip()
            else:
                price_with_currency = price_block.find('div', class_='bkjEo').text.strip()

            currency = 'грн' if price_with_currency.split()[-1] == '₴' else price_with_currency.split()[-1]
            
            # Якщо перед ціною є якийсь текст, наприклад "від"
            if not price_with_currency.split()[0].isdigit():
                price_with_currency = ' '.join(price_with_currency.split()[1:])
             
            price = float(''.join(price_with_currency.split()[:-1]))
            
        # Якщо товар недоступний, дані можуть бути, а можуть і не бути
        else:
            # Якщо дані є
            if not soup.find('div', class_='DoZv3 bkjEo') and soup.find('div', class_='bkjEo'):
                
                discount = False
            
                price_with_currency = soup.find('div', class_='bkjEo').text.strip()

                currency = 'грн' if price_with_currency.split()[-1] == '₴' else price_with_currency.split()[-1] 
                
                # Якщо перед ціною є якийсь текст, наприклад "від"
                if not price_with_currency.split()[0].isdigit():
                    price_with_currency = ' '.join(price_with_currency.split()[1:])
                
                price = float(''.join(price_with_currency.split()[:-1]))
                
            # Якщо немає даних
            else:
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
        product_obj = Product(product_name=product_name, store_name='Prom', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_prom(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = PromParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_prom(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = PromParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = PromParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://prom.ua/ua/p14116572-kotel-drovah-piroliznogo.html"))
    # asyncio.run(run_parsers("https://123"))
    
