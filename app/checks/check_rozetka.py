import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_rozetka(url: str):
    # https://rozetka.com.ua/ua/
    # https://hard.rozetka.com.ua/gigabyte-gv-n4060wf2oc-8gd/p385179081/
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('rozetka.com.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_rozetka(url: str):
    # https://rozetka.com.ua/croci_8023222064157/p214289035/
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')

        product_page = soup.find('div', class_='product-about__right-inner')
        title = soup.find('h1', class_='title__font ng-star-inserted')
        price = soup.find('div', class_='product-price__wrap ng-star-inserted')
        rating = soup.find('div', class_='rating text-base')
        
        # print(title)
        # print('\n',price,'\n')
        # print(rating)
        
        if product_page and title and price and rating: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://rozetka.com.ua/ua/promo/giftsforyourself/'
    # res = is_url_for_rozetka(url)
    res = await is_url_for_product_rozetka(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())