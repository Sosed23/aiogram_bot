from database.engine import session_maker
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from database.models import Category, Product, User, Cart


async def get_categories():
    async with session_maker() as session:
        return await session.scalars(select(Category))


async def get_category_product(category_id):
    async with session_maker() as session:
        return await session.scalars(select(Product).where(Product.category_id == int(category_id)))


async def get_category_name(category_id):
    async with session_maker() as session:
        result = await session.execute(select(Category.name).where(Category.id == int(category_id)))
        return result.scalar()


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
        # return await session.scalars(select(Cart).where(Cart.user_id == int(user_id)))
        query = select(Cart).where(Cart.user_id == user_id).options(joinedload(Cart.product))
        result = await session.scalars(query)
        return result.all()


async def get_cart_product_user(user_id: int, product_id: int):
    async with session_maker() as session:
        result = await session.execute(select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id))
        return result.scalar_one_or_none()


async def add_cart(user_id: int, product_id: int, quantity: int):
    async with session_maker() as session:
        # session.add(Cart(user_id=user_id, product_id=product_id, quantity=quantity))
        # await session.commit()
        query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id).options(
            joinedload(Cart.product))
        cart = await session.execute(query)
        cart = cart.scalar()
        if cart:
            cart.quantity += 1
            await session.commit()
            return cart
        else:
            session.add(Cart(user_id=user_id, product_id=product_id, quantity=1))
            await session.commit()


async def delete_cart_product(pr_id: int):
    async with session_maker() as session:
        stmt = delete(Cart).where(Cart.id == int(pr_id))
        await session.execute(stmt)
        await session.commit()
