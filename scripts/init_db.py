import asyncio
from app.db import engine, Base

async def init_db():
    """Ініціалізація бази даних: видалення та створення всіх таблиць."""
    async with engine.begin() as conn:
        print("Створення таблиць...")
        # Виконує синхронізацію з базою даних
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Таблиці створені успішно.")

if __name__ == "__main__":
    asyncio.run(init_db())
