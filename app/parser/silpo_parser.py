import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class SilpoParser(BaseParser):
    async def parse(self, url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        html_content = await self.fetch_page(url)
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            product_name = soup.find('h1', class_='ft-typo-22-semibold md:ft-typo-32-bold ft-text-black-87 ft-mb-16 md:ft-mb-20').text.strip()
            unit_of_measure = product_name.split(', ')[-1]
            
            price_block = soup.find('div', class_='ft-flex ft-justify-between ft-items-center ft-mb-16 md:ft-mb-24')
            price_with_currency = price_block.find('div', class_='product-page-price__main').text.strip()
            
            # Пошук ціни
            price = float(price_with_currency.split(' ')[0])
            
            # Пошук валюти
            currency = price_with_currency.split(' ')[1]
            
            # Пошук знижки
            discount = True if price_block.find('div', class_ = 'product-page-price__sale ng-star-inserted') else False
            
            # Пошук статуса товара
            if soup.find('div', class_='quantity').text.strip() == 'У кошик':
                status = 'Є в наявності'
            elif soup.find('div', class_='quantity').text.strip() == 'Товар закінчився':
                status = 'Немає в наявності'
            else: 
                status = None
            
            
            
            # print('--->' + product_name + '<---')
            # print('--->' + unit_of_measure + '<---')
            # print('--->' , price , '<---')
            # print('--->' + currency + '<---')
            # print('--->' + status + '<---')
            # print('--->' , discount , '<---')
            
            
            price_obj = Price(price=price, currency=currency, discount=discount, unit_of_measure=unit_of_measure, status=status)
            product_obj = Product(product_name=product_name, store_name='Сільпо', url=url, tg_id = tg_id)
            
            # print(product.prices[0])
            
            # async with SessionLocal() as session:
            #     session.add(product)
            #     await session.commit()
                
            return product_obj, price_obj
        else:
            return None


async def get_parse_silpo(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = SilpoParser(session)
        res = await parser.parse(url, tg_id)
        return res


async def run_parsers(urls: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = SilpoParser(session)
        res = await parser.parse(urls, tg_id=123)
        print(res)
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://silpo.ua/product/pechyvo-oreo-original-z-kakao-ta-nachynkoiu-z-vanilnym-smakom-685646"))
    # asyncio.run(run_parsers("https://123"))
    
