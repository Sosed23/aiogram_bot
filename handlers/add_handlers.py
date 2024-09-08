from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext

import database.query_postgresql as rq
import keyboards.keyboards as kb


router_add = Router()

class Add_product(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    category_id = State()


@router_add.message(Command('reg'))
async def add_prod_start(message: Message, state: FSMContext):
    await state.set_state(Add_product.name)
    await message.answer('Введите название товара')
    
    
@router_add.message(Add_product.name)
async def add_prod_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Add_product.description)
    await message.answer('Введите описание товара')


@router_add.message(Add_product.description)
async def add_prod_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Add_product.price)
    await message.answer('Введите стоимость товара')


@router_add.message(Add_product.price)
async def add_prod_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(Add_product.image)
    await message.answer('Введите ссылку на фото товара')


@router_add.message(Add_product.image)
async def add_prod_image(message: Message, state: FSMContext):
    await state.update_data(image=message.text)
    await state.set_state(Add_product.category_id)
    await message.answer('Укажите категорию товара', reply_markup=await kb.add_categories())


@router_add.callback_query(F.data.startswith('addcategory_'))
async def add_prod_category(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[1]
    await state.update_data(category_id=int(category_id))
    data = await state.get_data()
    
    product_data = {
        "name": data.get("name"),
        "description": data.get("description"), 
        "price": data.get("price"),
        "image": data.get("image"),
        "category": data.get("category_id")
    }
    
    await rq.orm_add_product(product_data)
    await callback.message.answer(
        f'<strong>Добавлен новый товар:</strong>\n'
        f'Название товара: {data["name"]}\n'
        f'Описание товара: {data["description"]}\n'
        f'Стоимость товара: {data["price"]}\n'
        f'Ссылка на фото товара: {data["image"]}\n'
        f'Категория товара: {data["category_id"]}',
        parse_mode="HTML"
    )
    await state.clear()


# @router_add.message(Add_product.category_id)
# async def add_prod_category(message: Message, state: FSMContext):
#     await state.update_data(category_id=message.text)
#     data = await state.get_data()
    
#     product_data = {
#         "name": data.get("name"),
#         "description": data.get("description"), 
#         "price": data.get("price"),
#         "image": data.get("image"),
#         "category": data.get("category_id")
#     }
    
#     await rq.orm_add_product(product_data)
#     await message.answer(f'Добавлен новый товаар:\nНазвание товара: {data["name"]}\nОписание товара: {data["description"]}\n'
#                          f'Стоимость товара: {data["price"]}\nСсылка на фото товара: {data["image"]}\nКатегория товара: {data["category_id"]}')
#     await state.clear()
    
