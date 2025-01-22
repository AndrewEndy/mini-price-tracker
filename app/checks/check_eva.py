import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_eva(url: str):
    # https://eva.ua/ua/
    # https://eva.ua/ua/220/bytovaja-himija/
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('eva.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_eva(url: str):
    # https://eva.ua/ua/pr726751/
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        product_page = soup.find('div', class_='product__info')
        title = soup.find('h1', class_='sf-heading__title')
        price_block = soup.find('div', class_='product__price-info')
        # status = soup.find('div', class_='a-product-stock')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if product_page and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://eva.ua/ua/promotion/online/'
    # res = is_url_for_eva(url)
    res = await is_url_for_product_eva(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())