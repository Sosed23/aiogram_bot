from database.engine import session_maker
from sqlalchemy import select, update, delete
from database.models import Category, Product


async def get_categories():
    async with session_maker() as session:
        return await session.scalars(select(Category))


async def get_category_product(category_id):
    async with session_maker() as session:
        return await session.scalars(select(Product).where(Product.category_id == int(category_id)))


async def get_product(product_id):
    async with session_maker() as session:
        return await session.scalar(select(Product).where(Product.id == int(product_id)))
