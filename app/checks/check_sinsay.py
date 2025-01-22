import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers
import json


def is_url_for_sinsay(url: str):
    # https://www.sinsay.com/ua/uk/
    # https://www.sinsay.com/ua/uk/cholovik/odiah/dzhynsy
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('sinsay.com') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_sinsay(url: str):
    # https://www.sinsay.com/ua/uk/fotoramka-735ck-00x
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        script_tag = soup.find('script', type='application/ld+json')

        # print(script_tag)

        if script_tag:
    
            data = json.loads(script_tag.string)
            
            # Отримуємо потрібні дані
            product_name = data.get('name')
            currency = data.get('offers', {}).get('priceCurrency')
            price = data.get('offers', {}).get('price')
            
            if product_name and price and currency: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://www.sinsay.com/ba/bs/'
    # res = is_url_for_sinsay(url)
    res = await is_url_for_product_sinsay(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())