import asyncio
import aiohttp
from bs4 import BeautifulSoup
from app.config import headers


def is_url_for_moyo(url: str):
    # https://www.moyo.ua/ua/
    # https://www.moyo.ua/ua/krasota-i-zdorove/ukhod-polost-rta/zubnye-shchetki/?page=2
    
    try:
        parts = url.split('//')
        parts = parts[1].split('/')
        
        if parts[0].find('moyo.ua') != -1: return True

        return False
    except Exception:
        return False
    
    
async def is_url_for_product_moyo(url: str):
    # https://www.moyo.ua/ua/smartfon_tecno_pova_6_li7_6_78_8_256gb_2sim_6000ma_ch_meteorite_grey/582647.html
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        # -----------------------------------------------------------------

        product_page = soup.find('div', class_='product_info')
        title = soup.find('h1', class_='product_name')
        price_block = soup.find('div', class_='product_price')
        
        # print(title)
        # print('\n',price_block,'\n')
        # print(product_info, '\n\n')

        
        if product_page and title and price_block: return True
        
        return False
        
    except Exception:
        return False


async def start():
    url = 'https://www.moyo.ua/ua/actions/rozprodazh-ostannikh-modeley.html'
    # res = is_url_for_moyo(url)
    res = await is_url_for_product_moyo(url)
    print(res)


if __name__ == '__main__':
   asyncio.run(start())