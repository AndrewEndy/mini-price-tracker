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
            
            price = price_with_currency.split(' ')[0]
            currency = price_with_currency.split(' ')[1]
            discount = True if price_block.find('div', class_ = 'product-page-price__sale ng-star-inserted') else False
            
            # print('--->' + product_name + '<---')
            # print('--->' + unit_of_measure + '<---')
            # print('--->' + price + '<---')
            # print('--->' + currency + '<---')
            # print('--->' , discount , '<---')
            
            
            price = Price(price=float(price), currency=currency, discount=discount, unit_of_measure=unit_of_measure)
            product = Product(product_name=product_name, store_name='Сільпо', url=url, tg_id = tg_id)
            
            # print(product.prices[0])
            
            # async with SessionLocal() as session:
            #     session.add(product)
            #     await session.commit()
                
            return product, price
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
    asyncio.run(run_parsers("https://silpo.ua/product/svyniacha-rulka-mr-grill-cheska-zamorozhena-889932"))
    # asyncio.run(run_parsers("https://123"))
    
