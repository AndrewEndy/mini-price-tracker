import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class YabkoParser(BaseParser):
    async def parse(self, url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        html_content = await self.fetch_page(url)
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            product_name = soup.find('h1', class_='product-info__title').text.strip()
            
            # Пошук статуса
            if soup.find('div', class_='product-info-product_status'):
                status = soup.find('div', class_='product-info-product_status').text.strip()
                
                if status == 'В наличии': status = 'В наявності'
                if status == 'Осталось мало': status = 'Залишилось мало'
                if status == 'Предзаказ': status = 'Передзамовлення'
            else:
                status = None
                
                
            # Блок даних з ціною, знижкою, валютою
            price_block = soup.find('div', class_='product-prices')
            
            discount = True if price_block.find('div', class_='product-info__price-old') else False
            currency = price_block.find('div', class_='product-info__price-new').text.strip().split()[-1]
            price = float(''.join(price_block.find('div', class_='product-info__price-new').text.strip().split()[:-1]))
            

            # print('--->' + product_name + '<---')
            # print('--->' + status + '<---')
            # print('--->' , discount , '<---')
            # print('--->' + currency + '<---')
            # print('--->' , price , '<---')
            
            
            price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure='шт.')
            product_obj = Product(product_name=product_name, store_name='Ябко', url=url, tg_id=tg_id)
            
            # print(f'{product_obj}\n\n{price_obj}')
            
            # async with SessionLocal() as session:
            #     session.add(product)
            #     await session.commit()
                
            return product_obj, price_obj
        else:
            return None


async def get_parse_yabko(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = YabkoParser(session)
        res = await parser.parse(url, tg_id)
        return res


async def run_parsers(urls: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = YabkoParser(session)
        res = await parser.parse(urls, tg_id=123)
        print(res)
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://jabko.ua/gadzheti-i-drugoe/playstation/aksessuari-dlja-playstation/zarjadnoe-ustrojstvo-dlja-gejmpada-sony-dualsense-charging-station--9374107-"))
    # asyncio.run(run_parsers("https://123"))
    
