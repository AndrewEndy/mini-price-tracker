import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_avrora(url: str):
    # https://avrora.ua/
    # https://avrora.ua/dityachi-tovari-ta-igrashki/
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('avrora.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_avrora(url: str):
    # https://avrora.ua/nabir-igrashkoviy-trek-z-budivelnoyu-tehnikoyu/
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')

        product_page = soup.find('div', class_='ty-product-block__left')
        title = soup.find('h1', class_='ty-product-block-title')
        price = soup.find('div', class_='ty-product-prices')
        price_with_currency = price.find('div', class_='ty-product-block__price-actual')
        
        # print(title)
        # print('\n',price,'\n')
        # print(price_with_currency, '\n\n')
        # print(product_page)
        
        if product_page and title and price and price_with_currency: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://avrora.ua/vsi-tovary/'
    # res = is_url_for_avrora(url)
    res = await is_url_for_product_avrora(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())