import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_staff(url: str):
    # https://www.staff-clothes.com/parnyam/
    # https://www.staff-clothes.com/devushkam/
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('staff-clothes.com') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_staff(url: str):
    # https://www.staff-clothes.com/product/qwe0129/
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        # product_page = soup.find('div', class_='top-product-info')
        title = soup.find('div', class_='product__title')
        price_block = soup.find('div', class_='product__price')
        product_info = soup.find('div', class_='product__category product__category--desc')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if product_info and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://www.staff-clothes.com/favorites/'
    # res = is_url_for_staff(url)
    res = await is_url_for_product_staff(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())