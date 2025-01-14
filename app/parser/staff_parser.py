import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class StaffParser(BaseParser):
    async def parse(self, url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        html_content = await self.fetch_page(url)
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            product_name = soup.find('div', class_='product__title').find('h1').text.strip()
            
            # Пошук статуса товара
            if soup.find('div', class_='product__ends-container'):
                status = soup.find('div', class_='product__ends').text.strip() 
            else:
                status = 'Є в наявності'
                
            # Пошук ціни, знижки, валюти
            price_block = soup.find('div', class_='product__price')
            
            discount = True if price_block.find('span', class_='product__price--old') else False
            price = float(price_block.text.strip().split()[0])
            currency = price_block.text.strip().split()[-1].replace('.','')
            
            
            # print('--->' + product_name + '<---')
            # print('--->' + str(status) + '<---')
            # print('--->' + str(discount) + '<---')
            # print('--->' + currency + '<---')
            # print('--->' + str(price) + '<---')
            
            
            price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=None)
            product_obj = Product(product_name=product_name, store_name='Staff', url=url, tg_id=tg_id)
            
            # print(f'{product_obj}\n\n{price_obj}')
            
            # async with SessionLocal() as session:
            #     session.add(product)
            #     await session.commit()
                
            return product_obj, price_obj
        else:
            return None


async def get_parse_staff(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = StaffParser(session)
        res = await parser.parse(url, tg_id)
        return res


async def run_parsers(urls: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = StaffParser(session)
        res = await parser.parse(urls, tg_id=123)
        print(res)
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://www.staff-clothes.com/product/qwe0139/"))
    # asyncio.run(run_parsers("https://123"))
    
