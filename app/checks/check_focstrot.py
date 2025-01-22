import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_focstrot(url: str):
    # https://www.foxtrot.com.ua/
    # https://www.foxtrot.com.ua/uk/shop/noutbuki_apple-macbook-air-m3.html
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('foxtrot.com.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_focstrot(url: str):
    # https://www.foxtrot.com.ua/uk/shop/stiralki_samsung_dv90ta040ae-ua.html
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        product_page = soup.find('div', class_='product-box__heading')
        title = soup.find('h1', class_='page__title overflow')
        price_block = soup.find('div', class_='product-box__item-container')
        # status = soup.find('div', class_='a-product-stock')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if product_page and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://www.foxtrot.com.ua/uk/actions/46911'
    # res = is_url_for_focstrot(url)
    res = await is_url_for_product_focstrot(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())