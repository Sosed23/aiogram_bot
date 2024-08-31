from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardButton, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
import keyboards.keyboards as kb
import database.query_postgresql as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await rq.add_user(message.from_user.id, first_name, last_name)
    await message.answer('Добро пожаловать в магазин кроссовок!', reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.products(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('product_'))
async def category(callback: CallbackQuery):
    product_data = await rq.get_product(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {product_data.name}\nОписание: {product_data.description}\n'
                                  f'Цена: {product_data.price}$', reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Добавить в корзину', callback_data=f'cart_{product_data.id}')]]))


@router.callback_query(F.data.startswith('cart_'))
async def category(callback: CallbackQuery):
    product_data = await rq.get_product(callback.data.split('_')[1])
    await callback.answer(f'Вы выбрали товар: {product_data.name}')
    await callback.message.answer(f'Вы добавили в корзину: {product_data.name}')
    product_id = int(f'{product_data.id}')
    user_id = callback.from_user.id
    quantity = 1
    await rq.add_cart(user_id, product_id, quantity)


@router.message(F.text == 'Корзина')
async def echo(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f'user_id: {user_id}')
    try:
        cart_products = await rq.get_cart_user(user_id)
        for cart_product in cart_products:
            product_id = cart_product.product_id
            product = await rq.get_product(product_id)
            if product:
                await message.answer(f'Название: {product.name}; Цена: {product.price}; Изображение: {product.image}')
            else:
                await message.answer(f'Продукт с ID {product_id} не найден.')
    except Exception as e:
        await message.answer(f'Произошла ошибка: {e}')

