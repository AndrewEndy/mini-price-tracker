import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_kasta(url: str):
    # https://kasta.ua/
    # https://kasta.ua/uk/m/tovary-ua-brands/?new=true&affiliation=zhinkam&affiliation=cholovikam&kind=kofta&kind=svetr
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('kasta.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_kasta(url: str):
    # https://kasta.ua/uk/product/18601285:702/
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        product_page = soup.find('div', class_='p__bg')
        title = soup.find('h1', class_='p__pads p__title p__name p__dsc-order-1 m-0')
        price_block = soup.find('div', class_='p__pads flex center pt-24 p__dsc-order-2')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if product_page and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://kasta.ua/uk/m/brand-Puma-assortment/?affiliation=cholovikam'
    # res = is_url_for_kasta(url)
    res = await is_url_for_product_kasta(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())