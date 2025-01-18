import asyncio
import aiohttp
from app.config import headers
from app.checks.check_silpo import is_url_for_product_silpo, is_url_for_silpo
from app.checks.check_willmax import is_url_for_product_willmax, is_url_for_willmax
from app.checks.check_rozetka import is_url_for_product_rozetka, is_url_for_rozetka
from app.checks.check_avrora import is_url_for_product_avrora, is_url_for_avrora
from app.checks.check_epicentr import is_url_for_product_epicentr, is_url_for_epicentr
from app.checks.check_yabko import is_url_for_product_yabko, is_url_for_yabko
from app.checks.check_staff import is_url_for_product_staff, is_url_for_staff
from app.checks.check_shchodnya import is_url_for_product_shchodnya, is_url_for_shchodnya
from app.checks.check_eva import is_url_for_product_eva, is_url_for_eva
from app.checks.check_focstrot import is_url_for_product_focstrot, is_url_for_focstrot
from app.checks.check_moyo import is_url_for_product_moyo, is_url_for_moyo
from app.checks.check_allo import is_url_for_product_allo, is_url_for_allo
from app.checks.check_kasta import is_url_for_product_kasta, is_url_for_kasta
from app.checks.check_prom import is_url_for_product_prom, is_url_for_prom



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
    
    if store_name == 'avrora':
        if not is_url_for_avrora(url): return False
        flag = await is_url_for_product_avrora(url)
    
    
    if store_name == 'rozetka':
        if not is_url_for_rozetka(url): return False
        flag = await is_url_for_product_rozetka(url)
    
    
    if store_name == 'willmax':
        if not is_url_for_willmax(url): return False
        flag = await is_url_for_product_willmax(url)
    
    
    if store_name == 'silpo':
        if not is_url_for_silpo(url): return False
        flag = await is_url_for_product_silpo(url)
        
        
    if store_name == 'epicentr':
        if not is_url_for_epicentr(url): return False
        flag = await is_url_for_product_epicentr(url)
        
        
    if store_name == 'yabko':
        if not is_url_for_yabko(url): return False
        flag = await is_url_for_product_yabko(url)
    
    
    if store_name == 'staff':
        if not is_url_for_staff(url): return False
        flag = await is_url_for_product_staff(url)
        
        
    if store_name == 'shchodnya':
        if not is_url_for_shchodnya(url): return False
        flag = await is_url_for_product_shchodnya(url) 
    
    
    if store_name == 'eva':
        if not is_url_for_eva(url): return False
        flag = await is_url_for_product_eva(url)    
        
        
    if store_name == 'focstrot':
        if not is_url_for_focstrot(url): return False
        flag = await is_url_for_product_focstrot(url) 
        
    
    if store_name == 'moyo':
        if not is_url_for_moyo(url): return False
        flag = await is_url_for_product_moyo(url) 
        
        
    if store_name == 'allo':
        if not is_url_for_allo(url): return False
        flag = await is_url_for_product_allo(url) 
    
    
    if store_name == 'kasta':
        if not is_url_for_kasta(url): return False
        flag = await is_url_for_product_kasta(url) 
        
        
    if store_name == 'prom':
        if not is_url_for_prom(url): return False
        flag = await is_url_for_product_prom(url) 
    
    return flag