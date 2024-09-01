from aiogram import F, Router, types, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardButton, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
import keyboards.keyboards as kb
import database.query_postgresql as rq

router = Router()


from dotenv import load_dotenv
import os

load_dotenv()


bot = Bot(token=os.environ.get("BOT_TOKEN"))


@router.message(CommandStart())
async def cmd_start(message: Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await rq.add_user(message.from_user.id, first_name, last_name)
    await message.answer('Добро пожаловать в магазин кроссовок!', reply_markup=kb.main)
    await message.answer_photo('AgACAgQAAxkDAAIIBmbTJM-gFaZ4rETI_X_-ZV_lDnAbAALNtDEbIbJ1UkhHmD2CuCVWAQADAgADdwADNQQ')


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
    cart_products = await rq.get_cart_user(user_id)
    for cart_product in cart_products:
        product_id = cart_product.product_id
        product = await rq.get_product(product_id)
        await message.answer(f'Название: {product.name}; Цена: {product.price}; Изображение: {product.image}, '
                             f'delete_{cart_product.id}',
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Удалить из корзины',
                             callback_data=f'delete_{cart_product.id}')]]))


@router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: CallbackQuery):
    product_data = await rq.delete_cart_product(pr_id=int(callback.data.split('_')[1]))
    await callback.answer(f'Вы удалили товар: {product_data}')
    await callback.message.answer(f'Вы удалили из корзину: {product_data}')

# @router.message(F.text == 'фото')
# async def photo_id(message: types.Message):
#     url_photo='https://megacvet24.ru/image/catalog/lyon-malinovyy-suhocvet.jpg'
#
#     sent_message = await bot.send_photo(chat_id=message.chat.id, photo=url_photo)
#
#     photo__id = sent_message.photo[-1].file_id
#     await message.answer(f'Изображение загружено. Photo ID: {photo__id}')
#     await message.answer_photo(f'{photo__id}')

