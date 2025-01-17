import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_allo(url: str):
    # https://allo.ua/
    # https://allo.ua/ua/products/mobile/p-3/proizvoditel-apple/
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('allo.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_allo(url: str):
    # https://allo.ua/ua/televizory/televizor-kivi-24h710qb.html
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        product_page = soup.find('main', class_='p-main')
        title = soup.find('h1', class_='p-view__header-title')
        price_block = soup.find('div', class_='p-trade-wrapper p-main__trade')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if product_page and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://allo.ua/ua/poco_x7_flash_sale/'
    # res = is_url_for_allo(url)
    res = await is_url_for_product_allo(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())