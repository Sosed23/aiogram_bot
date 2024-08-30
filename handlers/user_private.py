import requests, json, asyncpg
from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import InlineQueryResultArticle, InlineQuery, InputTextMessageContent
from aiogram.utils import markdown

from data import price
import aiohttp
import asyncio
from keyboards import reply
from keyboards import inline
from aiogram import Bot
from dotenv import load_dotenv
import os
from database import query_postgresql as rq
from keyboards import keyboards as kb

load_dotenv()


user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я вируальный помощник!', reply_markup=kb.main)


@user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
async def echo(message: types.Message):
    await message.answer("Это меню", reply_markup=reply.del_kb)
    # Асинхронно вызываем функцию price и обрабатываем данные
    data_j = await price()

    values = []
    for entry in data_j.get('directoryEntries', []):
        custom_field_data = entry.get('customFieldData', [])
        for field_data in custom_field_data:
            value = field_data.get('value')
            await message.answer(f"Полученные данные:\n{field_data}", reply_markup=inline.inline_kb())
    #         if value:
    #             values.append(value)
    #
    # # Форматируем данные для вывода
    # formatted_values = "\n".join(values)
    #
    # await message.answer(f"Полученные данные:\n{formatted_values}", reply_markup=reply.test_kb)

# @user_private_router.message(F.text.lower() == 'каталог')
# async def catalog_cmd(message: types.Message):
#     await message.answer("Это каталог", reply_markup=reply.del_kb)
#
#     async def catalog():
#         url = "https://megacvet24.ru/mobile_app/full"
#
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 data = await response.json()
#                 return data
#
#     async def get_first_ten_elements_with_info(data):
#         elements = list(data)
#
#         for i in range(10):
#             element = elements.pop()
#             await message.answer(f"{element['article']}, {element['name']}, {element['image']}",
#                                  reply_markup=inline.get_callback_btns(
#                                      btns={
#                                          'Удалить': f"delete_{element['article']}",
#                                          'Изменить': f"change_{element['article']}"
#                                      }
#                                  ),
#                                  )
#     data = await catalog()
#     await get_first_ten_elements_with_info(data)


@user_private_router.message(Command('get'))
async def get_photo(message: types.Message):
    await message.answer_photo(photo='https://megacvet24.ru/image/catalog/gipsofila-golubaya-i-orhideya-kosmos-sinyaya.jpg',
                               caption='Это ФОТО')


@user_private_router.message(F.photo)
async def get_photo(message: types.Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')


@user_private_router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: types.CallbackQuery):
    product_id = callback.data.split('_')[-1]
    await callback.answer('Товар удален')
    await callback.message.answer(f'Товар удален!{product_id}')


@user_private_router.message(F.text.lower() == 'кар')
async def cars(message: types.Message):
    await message.answer('Инлайн-кнопки', reply_markup=inline.inline_cars())


@user_private_router.callback_query(F.data.startswith('car_'))
async def delete_product(callback: types.CallbackQuery):
    product_id = callback.data.split('_')[-1]
    await callback.answer('Товар удален')
    await callback.message.answer(f'Товар удален!{product_id}')


@user_private_router.message(F.text.lower() == 'каталог')
async def catalog(message: types.Message):
    await message.answer('Выберете категорию товара', reply_markup=await kb.categories())


@user_private_router.callback_query(F.data.startswith('category_'))
async def category(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.products(callback.data.split('_')[1]))


@user_private_router.callback_query(F.data.startswith('product_'))
async def category(callback: types.CallbackQuery):
    product_data = await rq.get_product(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {product_data.name}\nОписание: {product_data.description}\n'
                                  f'Цена: {product_data.price}\n{product_data.image}',
                                  reply_markup=await kb.products(callback.data.split('_')[1]))
