import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_epicentr(url: str):
    # https://epicentrk.ua/
    # https://epicentrk.ua/ua/shop/viski/
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('epicentrk.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_epicentr(url: str):
    # https://epicentrk.ua/ua/shop/stelazh-metalevyi-metkas-1600x800x300-mm-dsp-polytsia-4-sht-tsynk.html
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -------------------------------------------------

        product_page = soup.find('div', class_='_TFdhZS _B-qWOB _mzoRO9 _Hhg1Gu _QvYS+W')
        product_page2 = soup.find('div', class_='_TFdhZS _B-qWOB _mzoRO9 _Hhg1Gu _lcqAuU')
        title = soup.find('h1', class_='_aql9TB _7TBdaN _GuJjCI')
        status = soup.find('div', class_='_A7y+id')
        
        
        # print(title)
        # print('\n',product_page2,'\n')
        # print(status, '\n\n')
        # print(product_page)
        
        if product_page and title and status and product_page2: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://epicentrk.ua/ua/actions/utsenka.html'
    # res = is_url_for_epicentr(url)
    res = await is_url_for_product_epicentr(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())