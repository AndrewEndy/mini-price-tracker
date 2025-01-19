import asyncio
import aiohttp
from typing import List, Tuple
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .base_parser import BaseParser
from app.models import Product, Price
from app.db import SessionLocal


class JuskParser(BaseParser):
    async def parse(self, html_content , url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_name = soup.find('div', class_='product-sumbox-sub-series').text.strip()
        
        price_block = soup.find('div', class_='product-card-body-content')
        
        discount = True if price_block.find('span', class_='ssr-product-price-support d-block price-before text-bold beforeprice') else False
        
        # Пошук ціни, валюти, одиниці виміру
        if discount:
            if price_block.find('span', class_='ssr-product-price product-price discountprice'):
                price_currency_uom = price_block.find('span', class_='ssr-product-price product-price discountprice').text.strip()
            elif price_block.find('span', class_='ssr-product-price product-price offerprice'):
                price_currency_uom = price_block.find('span', class_='ssr-product-price product-price offerprice').text.strip()
        else:
            price_currency_uom = price_block.find('span', class_='ssr-product-price product-price normalprice').text.strip()
            
        unit_of_measure = price_currency_uom.split('/')[-1] + '.'
        currency = price_currency_uom.split('/')[0].split()[-1]
        price = float(''.join(price_currency_uom.replace(',','.').split('/')[0].split()[:-1]))
        
        status = None
        
        # print('--->' + product_name + '<---')
        # print('--->' + str(status) + '<---')
        # print('--->' + str(discount) + '<---')
        # print('--->' + str(price) + '<---')
        # print('--->' + str(currency) + '<---')
        # print('--->' + str(unit_of_measure) + '<---')
        
        
        
        
        price_obj = Price(price=price, currency=currency, discount=discount, status=status, unit_of_measure=unit_of_measure)
        product_obj = Product(product_name=product_name, store_name='Jusk', url=url, tg_id=tg_id)
        
        # print(f'{product_obj}\n\n{price_obj}')
        
        # async with SessionLocal() as session:
        #     session.add(product)
        #     await session.commit()
            
        return product_obj, price_obj


async def get_parse_jusk(url: str, tg_id: int) -> Tuple['Product', 'Price'] | None:
    async with aiohttp.ClientSession() as session:
        parser = JuskParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id)
            return res
        else: 
            return None


async def get_parsed_changes_jusk(html_content, url: str, tg_id: int) -> Tuple['Product', 'Price']:
    async with aiohttp.ClientSession() as session:
        parser = JuskParser(session)
        return await parser.parse(html_content, url, tg_id)


async def run_parsers(url: List[str]) -> None:
    """Тест роботи парсира"""
    async with aiohttp.ClientSession() as session:
        parser = JuskParser(session)
        html_content = await parser.fetch_page(url)
        
        if html_content:
            res = await parser.parse(html_content, url, tg_id=123)
            print(res)
        else: 
            return None
        

if __name__ == "__main__":
    asyncio.run(run_parsers("https://jysk.ua/vanna/zanaviski-dlya-dushu/zanaviska-dlya-dushu-gusum-150x200sm-bilyy"))
    # asyncio.run(run_parsers("https://123"))
    
