from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update
from sqlalchemy.orm import joinedload
from app.models import Product
from app.db import SessionLocal

async def delete_product_by_id(product_id: int) -> bool:
    """Видаляє продукт з бази даних за product_id.
    
    Args:
        product_id (int): Ідентифікатор продукту.

    Returns:
        bool: True, якщо продукт успішно видалено, False, якщо продукт не знайдено.
    """
    async with SessionLocal() as session:  # Ініціалізація асинхронної сесії
        async with session.begin():  # Початок транзакції
            # Знаходимо продукт за його ID
            query = select(Product).options(joinedload(Product.prices)).where(Product.product_id == product_id)
            result = await session.execute(query)
            product = result.scalars().first()

            if product is None:  # Продукт не знайдено
                # print(f"Продукт із product_id={product_id} не знайдено.")
                return False

            # Видаляємо продукт
            await session.delete(product)
            await session.commit()  # Застосовуємо зміни
            # print(f"Продукт із product_id={product_id} успішно видалено.")
            return True


async def is_url_in_db(url: str, tg_id: int) -> bool:
    """
    Перевіряє, чи існує запис із заданим URL і tg_id в базі даних.

    :param url: URL для перевірки.
    :param tg_id: Telegram ID користувача.
    :param session: Сесія бази даних.
    :return: True, якщо запис існує, інакше False.
    """
    
    async with SessionLocal() as session:  # Ініціалізація асинхронної сесії
        async with session.begin():  # Початок транзакції
            query = (
                select(Product)
                .options(joinedload(Product.user))  # Підвантаження даних про користувача (опціонально)
                .where(Product.url == url, Product.tg_id == tg_id)
            )
            result = await session.execute(query)
            product = result.scalars().first()
            return product is not None


async def add_new_product_to_db(product: Product) -> None:
    '''
    Вносить новий Product і прив\'заний до нього Price в базу даних 
    '''
    
    async with SessionLocal() as session:  # Ініціалізація асинхронної сесії
        async with session.begin():  # Початок транзакції
            session.add(product)
    

async def get_all_products() -> list['Product']:
    async with SessionLocal() as session:
        async with session.begin():
            query = select(Product).options(joinedload(Product.prices))
            result = await session.execute(query)
            products = result.unique().scalars().all()
    return products