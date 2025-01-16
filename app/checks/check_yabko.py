import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_yabko(url: str):
    # https://jabko.ua/lviv/
    # https://jabko.ua/lviv/gadzheti-i-drugoe/droni/
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('jabko.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_yabko(url: str):
    # https://jabko.ua/iphone/b-u-iphone/b-u-apple-iphone-12/b-u-iphone-12-64gb--white-
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        product_page = soup.find('div', class_='top-product-info')
        title = soup.find('h1', class_='product-info__title')
        price_block = soup.find('div', class_='product-prices')
        rating = soup.find('div', class_='product-info__flex-grade')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(rating, '\n\n')
        # print(product_page)
        
        if product_page and title and price_block and rating: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://jabko.ua/gadzheti-i-drugoe/tehnika-dlja-doma/portativnij-proektor-xgimi-mogo-2-pro--xk04t-'
    # res = is_url_for_yabko(url)
    res = await is_url_for_product_yabko(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())