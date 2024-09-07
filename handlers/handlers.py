from itertools import product

from aiogram import F, Router, types, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart

from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardButton, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from pyexpat.errors import messages

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
    await message.answer('Добро пожаловать в магазин цветов!', reply_markup=kb.main)
    # await message.answer_photo('AgACAgQAAxkDAAIIBmbTJM-gFaZ4rETI_X_-ZV_lDnAbAALNtDEbIbJ1UkhHmD2CuCVWAQADAgADdwADNQQ')


@router.message(F.text == '💐 Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]
    products = await rq.get_category_product(int(category_id))

    for product in products:
        # Отправляем фото продукта
        await callback.message.answer_photo(
            photo=product.image,
            caption=f'Название: {product.name}\nАртикул: {product.description}\nЦена: {product.price} руб.',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'cart_{product.id}')]]
            )
        )

    await callback.answer('Вы выбрали категорию')
    # await callback.message.answer('Выберите товар по категории',
    #                               reply_markup=await kb.products(callback.data.split('_')[1]))

#
# async def category(callback: CallbackQuery):
#     category_id = callback.data.split('_')[1]
#     products = await rq.get_category_product(int(category_id))
#
#     for product in products:
#         # Предположим, что product.image_urls содержит строку с ссылками на изображения, разделенными запятыми
#         image_urls = product.image_urls.split(', ')
#
#         # Отправляем первое фото продукта с кнопками
#         await callback.message.answer_photo(
#             photo=image_urls[0],
#             caption=f'Название: {product.name}\nОписание: {product.description}\nЦена: {product.price}$',
#             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#                 [InlineKeyboardButton(text='Назад', callback_data=f'prev_{product.id}_0'),
#                  InlineKeyboardButton(text='Вперед', callback_data=f'next_{product.id}_0')],
#                 [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'cart_{product.id}')]]
#             )
#         )
#
#     await callback.answer('Вы выбрали категорию')

# @router.callback_query_handler(lambda c: c.data.startswith('prev_') or c.data.startswith('next_'))
# async def navigate_images(callback: CallbackQuery):
#     action, product_id, current_index = callback.data.split('_')
#     current_index = int(current_index)
#     product = await rq.get_product(int(product_id))  # Предположим, что есть функция для получения одного продукта
#     image_urls = product.image_urls.split(', ')
#
#     if action == 'next':
#         new_index = (current_index + 1) % len(image_urls)
#     else:
#         new_index = (current_index - 1) % len(image_urls)
#
#     # Обновляем фото и кнопки
#     await callback.message.edit_media(
#         media=InputMediaPhoto(media=image_urls[new_index]),
#         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#             [InlineKeyboardButton(text='Назад', callback_data=f'prev_{product.id}_{new_index}'),
#              InlineKeyboardButton(text='Вперед', callback_data=f'next_{product.id}_{new_index}')],
#             [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'cart_{product.id}')]]
#         )
#     )


# @router.callback_query(F.data.startswith('product_'))
# async def category(callback: CallbackQuery):
#     product_data = await rq.get_product(callback.data.split('_')[1])
#     await callback.answer('Вы выбрали товар')
#     await callback.message.answer(f'Название: {product_data.name}\nОписание: {product_data.description}\n'
#                                   f'Цена: {product_data.price}$', reply_markup=InlineKeyboardMarkup(
#         inline_keyboard=[[InlineKeyboardButton(text='Добавить в корзину', callback_data=f'cart_{product_data.id}')]]))


@router.callback_query(F.data.startswith('cart_'))
async def category(callback: CallbackQuery):
    product_data = await rq.get_product(callback.data.split('_')[1])
    await callback.answer(f'Вы выбрали товар: {product_data.name}')
    await callback.message.answer(f'Вы добавили в корзину: {product_data.name}')
    product_id = int(f'{product_data.id}')
    user_id = callback.from_user.id
    quantity = 1
    await rq.add_cart(user_id, product_id, quantity)


@router.message(F.text == '🛒 Корзина')
async def echo(message: types.Message):
    user_id = message.from_user.id
    cart_products = await rq.get_cart_user(user_id)

    if cart_products is None or len(cart_products) == 0:
        await message.answer('Ваша корзина пуста')
        return

    for cart_product in cart_products:
        product_id = cart_product.product_id
        cart_product_quantity = await rq.get_cart_product_user(user_id, product_id)
        product = await rq.get_product(product_id)
        category_name = await rq.get_category_name(product.category_id)
        await message.answer_photo(photo=product.image,
                            caption=f'Название: {product.name}\nКатегория: {category_name}\nЦена: {product.price}\n'
                                    f'Кол-во: {cart_product_quantity.quantity} шт.',
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Удалить из корзины',
                             callback_data=f'delete_{cart_product.id}')]]))



@router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: CallbackQuery):
    cart_id = int(callback.data.split('_')[1])
    user_id = int(callback.from_user.id)

    product_id = await rq.get_cart_id_user(cart_id=cart_id, user_id=user_id)

    # await callback.message.answer (text=f'ИД товара {product_id.product_id}')

    product_name = await rq.get_product(product_id.product_id)

    await rq.delete_cart_product(pr_id=cart_id)

    await callback.answer(f'Вы удалили товар: {product_name.name}')
    await callback.message.answer(f'Вы удалили из корзины: {product_name.name}')




@router.message(F.text == '☎️ Контакты')
async def contacts(message: types.Message):
    await message.answer(
        f'📞 Телефон: 8 (495) 121-24-30\n'
        f'🕓 Время работы магазина: с 8:00 до 21:00\n'
        f'🚩 Адрес розничного магазина: Сенная площадь, Санкт-Петербург'
    )

    # Отправка местоположения
    await message.answer_location(latitude=59.9343, longitude=30.3198)