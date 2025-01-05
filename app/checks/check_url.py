import asyncio
import aiohttp
from app.config import headers
from app.checks.check_silpo import is_url_for_product_silpo, is_url_for_silpo



async def check_connection_to_url(url):
    '''Функція перевіряє чи можна підключитись до сайту'''
    try:
        async with aiohttp.ClientSession() as session:  
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status()  # Перевірка статусу відповіді
                # print(response.status)
                return True
    except aiohttp.ClientError as e:
        print(f"Помилка підключення до {url}: {e}")
        return False
    

async def check_desired_site(url: str, store_name: str) -> bool:
    '''Функція опреділяє потрібний сайт і перевіряє чи підходить він для парсингу'''
    flag = False
    
    if store_name == 'rozetka':
        pass
    
    if store_name == 'silpo':
        if not is_url_for_silpo(url): return False
        flag = await is_url_for_product_silpo(url)
    
    return flag