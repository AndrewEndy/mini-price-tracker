import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_prom(url: str):
    # https://prom.ua/ua/
    # https://prom.ua/ua/Rashodnye-materialy-dlya-ofisa
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('prom.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_prom(url: str):
    # https://prom.ua/p45660520-shkaf-kupe-1600h450h2100.html
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        product_page = soup.find('div', class_='MafxA sMS5m')
        title = soup.find('h1', class_='_3Trjq F7Tdh vj3pM htldP')
        price_block = soup.find('div', class_='tqUsL')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if product_page and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://prom.ua/ua/Doski-razdelochnye'
    # res = is_url_for_prom(url)
    res = await is_url_for_product_prom(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())