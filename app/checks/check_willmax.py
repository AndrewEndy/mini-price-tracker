import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_willmax(url: str):
    # https://www.willmax.com.ua/
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        parts = parts[0].split('.')
        
        # print(f'|{parts}|')
        
        if parts[1] == 'willmax': return True
        return False
    except Exception:
        return False
    
    
async def is_url_for_product_willmax(url: str):
    # https://www.willmax.com.ua/whey-protein-80-1kg-shokolad
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.find('div', class_='title-product')
        price = soup.find('div', class_='product_page_price price')
        rating = soup.find('div', class_='box-review')
        
        # print(title)
        # print('\n',price,'\n')
        # print(rating)
        
        if not title or not price or not rating: return False
        
        return True
        
    except Exception:
        return False


async def start():
    url = 'https://www.willmax.com.ua/kazein/'
    res = await is_url_for_product_willmax(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())