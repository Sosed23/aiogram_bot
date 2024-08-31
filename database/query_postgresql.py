from database.engine import session_maker
from sqlalchemy import select, update, delete
from database.models import Category, Product, User, Cart


async def get_categories():
    async with session_maker() as session:
        return await session.scalars(select(Category))


async def get_category_product(category_id):
    async with session_maker() as session:
        return await session.scalars(select(Product).where(Product.category_id == int(category_id)))


################ ПРОДУКТ ##################

async def get_product(product_id):
    async with session_maker() as session:
        return await session.scalar(select(Product).where(Product.id == int(product_id)))


async def add_user(user_id: int, first_name: str, last_name: str):
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))

        if not user:
            session.add(User(user_id=user_id, first_name=first_name, last_name=last_name))
            await session.commit()


#################### КОРЗИНА ########################

async def get_cart_user(user_id):
    async with session_maker() as session:
        return await session.scalars(select(Cart).where(Cart.user_id == int(user_id)))


async def add_cart(user_id: int,product_id: int, quantity: int):
    async with session_maker() as session:
        session.add(Cart(user_id=user_id, product_id=product_id, quantity=quantity))
        await session.commit()
