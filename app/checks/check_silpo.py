import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_silpo(url: str):
    # https://silpo.ua/
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0] == 'silpo.ua': return True
        return False
    except Exception:
        return False
    

async def is_url_for_product_silpo(url: str):
    # https://silpo.ua/product/
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[1] != 'product': return False
        
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')

        product_page = soup.find('div', class_='product-page__data')
        if not product_page: return False
        
        return True
        
    except Exception:
        return False


async def start():
    url = 'https://silpo.ua/'
    res = await is_url_for_product_silpo(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())