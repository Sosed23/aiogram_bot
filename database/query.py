# from database.engine import session_maker
from sqlalchemy import select, update, delete
from database.models_sqlite import Category, async_session


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
    