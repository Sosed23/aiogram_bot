from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
import database.query_postgresql as rq

router_add = Router()

class Add_product(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    category = State()


@router_add.message(Command('reg'))
async def add_prod_start(message: Message, state: FSMContext):
    await state.set_state(Add_product.name)
    await message.answer('Введите название товара')
    
    
@router_add.message(Add_product.name)
async def add_prod_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Add_product.description)
    await message.answer('Введите описание товара')


@router_add.message(Add_product.name)
async def add_prod_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Add_product.description)
    await message.answer('Введите описание товара')


@router_add.message(Add_product.number)
async def two_three(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    
    product_data = {
        "name": data.get("name"),
        "description": "default description",  # можно также получить описание из state
        "price": 0.0,  # можно также получить цену из state
        "image": "default_image.png",  # можно задать изображение или получить из state
        "category": 1  # также можно получить категорию из state
    }
    
    await rq.orm_add_product(product_data)
    await message.answer(f'Спасибо, регистрация звершена.\nИмя: {data["name"]}\nНомер: {data["number"]}')
    await state.clear()
    