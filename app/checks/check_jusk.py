import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_jusk(url: str):
    # https://jysk.ua/
    # https://jysk.ua/vanna/zanaviski-dlya-dushu
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('jysk.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_jusk(url: str):
    # https://jysk.ua/spalnya/matraci/bezpruzhinni-matraci/matrats-bezpruzhynnyy-90x200sm-wellpur-hovda-gf110
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        product_page = soup.find('section', class_='product-intro')
        title = soup.find('div', class_='product-sumbox-sub-series')
        price_block = soup.find('div', class_='product-card-body-content')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if product_page and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://jysk.ua/outlet'
    # res = is_url_for_jusk(url)
    res = await is_url_for_product_jusk(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())