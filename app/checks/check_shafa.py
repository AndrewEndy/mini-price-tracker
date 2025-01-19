import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_shafa(url: str):
    # https://shafa.ua/uk/
    # https://shafa.ua/uk/aksesuary?search_text=%D0%BD%D0%B5%D0%BC%D0%B0%D1%94+%D0%B2+%D0%BD%D0%B0%D1%8F%D0%B2%D0%BD%D0%BE%D1%81%D1%82%D1%96
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('shafa.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_shafa(url: str):
    # https://shafa.ua/uk/home/bytovaya-himiya/hozyajstvennye-myla/96728706-10-od-kokosove-milo-mylzava-universal-150-g?from-adv=true
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        product_page = soup.find('div', class_='b-product b-product_type')
        title = soup.find('h1', class_='b-product__title')
        price_block = soup.find('div', class_='b-product-price')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if product_page and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://shafa.ua/social/posts'
    # res = is_url_for_shafa(url)
    res = await is_url_for_product_shafa(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())