import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class ShchodnyaParser(BaseParser):
    async def parse(self, html_content , url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        unit_of_measure = None
        
        product_name = soup.find('div', class_='col-sm-6 col-md-7 right_col').find('h1').text.strip()
        
        # Пошук одиниці виміру товара
        table = soup.find('div', class_='characteristics_block')
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all("td")
            if cells[0].get_text(strip=True) == "Об`єм" or cells[0].get_text(strip=True) == "Кількість" or cells[0].get_text(strip=True) == "Вага":
                unit_of_measure = cells[1].get_text(strip=True)
                break
        
        
        # Пошук статуса
        if soup.find('div', class_='availability'):
            status = soup.find('div', class_='availability').find('span').text.strip()
        else:
            status = None

        # Якщо статус = "Немає в наявності" - на сторінці відсутні майже всі дані про товар
        if status != 'Немає в наявності':
            # Пошук ціни, знижки, валюти
            price_block = soup.find('div', class_='price_container for_clear col-md-3')
            
            discount = True if price_block.find('div', class_='price-old') else False
            
            if discount:
                price_with_currency = price_block.find('div', class_='price-new').text.strip()
            else:
                price_with_currency = price_block.find('div', class_='price').text.strip().split('/ ')[0]
                
            price = float(''.join(price_with_currency.split()[:-1]))
            currency = price_with_currency.split()[-1]
        
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
        # print('--->' + str(unit_of_measure) + '<---')
        
        
        
        price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=unit_of_measure)
        product_obj = Product(product_name=product_name, store_name='Щодня', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_shchodnya(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = ShchodnyaParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_shchodnya(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = ShchodnyaParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = ShchodnyaParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://shchodnia.com/katalog-114/makiyaj-4915/ochi-4958/olivtsi-dlya-ochey-4962/olivets-dlya-ochey-bless-beauty-chorniy-292/"))
    # asyncio.run(run_parsers("https://123"))
    
