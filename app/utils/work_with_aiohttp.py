import asyncio
import aiohttp
from app.config import headers

# Функція для парсингу одного сайту
async def fetch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            print('200')  
            return url, html  
    except Exception as e:
        print(f'ERROR fetch| err: {e}')
        return url, None  # Обробка помилок


# Функція для обмеження та виконання парсингу
async def limited_fetch(sem, session, url):
    async with sem:  # Виконуємо завдання з обмеженням
        return await fetch(session, url)


# Головна функція для парсингу кількох сайтів
async def get_gather(urls):
    semaphore = asyncio.Semaphore(10)  # Обмеження діє тільки в цій функції
    async with aiohttp.ClientSession() as session:
        tasks = [limited_fetch(semaphore, session, url) for url in urls]
        return await asyncio.gather(*tasks)






urls = [
    "https://github.com/AndrewEndy/mini-price-tracker",
    "https://www.google.com/search?client=firefox-b-d&q=%D0%BF%D0%B5%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%B4%D0%B0%D1%87",
    "https://docs.python.org/uk/3/tutorial/controlflow.html#match-statements",
    "httpsasdasd",  
]


if __name__ == "__main__":
    results = asyncio.run(get_gather(urls))
    # for url, content in results:
    #     print(f"URL: {url}\nContent: {content[:100]}...\n")  # Вивід перших 100 символів
