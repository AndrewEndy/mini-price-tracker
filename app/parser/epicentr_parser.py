import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class EpicentrParser(BaseParser):
    async def parse(self, html_content, url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_name = soup.find('h1', class_='_aql9TB _7TBdaN _GuJjCI').text.strip()
        
        # Пошук статуса товара
        if soup.find('div', class_='_A7y+id'):
            status = soup.find('div', class_='_A7y+id').text.strip()
        else: 
            status = None
            
            
        if status != 'Немає в наявності':
            
            # Пошук акції
            if soup.find('s', class_='_Yf4yHx'):
                discount = True
            else:
                discount = False
                
                
            if discount:
                price_block = soup.find('div', class_='_Al-5uY _gqV+xi',).text.strip()
            else:
                price_block =   soup.find('div', class_='_Al-5uY').text.strip()
                
            # Пошук валюти
            currency = 'грн' if price_block.split('/')[0][-1] == '₴' else price_block.split('/')[0].split()[-1]
            
            # Пошук одиниці виміру
            unit_of_measure = price_block.split('/')[-1]
            
            # Пошук ціни
            price = float(''.join(price_block.split('/')[0].split()[:-1]))
            
        else:
            discount = False
            price = 0.0
            currency = None
            unit_of_measure = None
        
        # print('--->' + product_name + '<---')
        # print('--->' + status + '<---')
        # print('--->' , discount , '<---')
        # print('--->' + currency + '<---')
        # print('--->' + unit_of_measure + '<---')
        # print('--->' , price , '<---')
        
        
        price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=unit_of_measure)
        product_obj = Product(product_name=product_name, store_name='Епіцентр', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_epicentr(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = EpicentrParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_epicentr(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = EpicentrParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = EpicentrParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://epicentrk.ua/ua/shop/zaryadnoe-ustroystvo-forte-cb-15fp-forte-cb-15fp.html?trk=M2YwNzZiODFlMzczMDc0M2JiZjU3YWM4NzMwY2E0MGMtMi0wMDAyMjM5Mzgt"))
    # asyncio.run(run_parsers("https://123"))
    
