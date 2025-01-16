import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_shchodnya(url: str):
    # https://shchodnia.com/
    # https://shchodnia.com/katalog-114/dityam-5310/
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('shchodnia.com') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_shchodnya(url: str):
    # https://shchodnia.com/novinki-115/farea-men-shampun-dlya-volossya-z-hmelem-500-ml-60035/
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        # product_page = soup.find('div', class_='top-product-info')
        title = soup.find('div', class_='col-sm-6 col-md-7 right_col').find('h1')
        table = soup.find('div', class_='characteristics_block')
        price_block = soup.find('div', class_='for_clear')
        # status = soup.find('div', class_='availability').find('span')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if table and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://shchodnia.com/katalog-114/volossya-4822/'
    # res = is_url_for_shchodnya(url)
    res = await is_url_for_product_shchodnya(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())