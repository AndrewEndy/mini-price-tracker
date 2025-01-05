import aiohttp
from typing import List
from abc import ABC, abstractmethod
from app.config import headers
from app.models import Product



class BaseParser(ABC):
    def __init__(self, http_session: aiohttp.ClientSession):
        self.http_session = http_session  # Асоційоване підключення для асинхронних запитів

    @abstractmethod
    async def parse(self, url: str) -> List[Product]:
        """Абстрактний метод для парсингу. Має бути реалізований у кожному підкласі"""
        pass

    async def fetch_page(self, url: str)  -> str | None:
        """Отримання HTML-сторінки або None у разі помилки"""
        try:
            async with self.http_session.get(url=url, headers=headers) as response:
                response.raise_for_status()  # Перевірка статусу відповіді
                print(response.status)
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Помилка підключення до {url}: {e}")
            return None