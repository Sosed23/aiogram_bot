import requests, json, asyncpg
from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from megacvet_json import catalog, get_first_ten_elements_with_info
from data import price

from keyboards import reply
from keyboards import inline
from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()


bot = Bot(token=os.environ.get("BOT_TOKEN"))

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я вируальный помощник!', reply_markup=reply.test_kb)


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

@user_private_router.message(F.text.lower() == 'каталог')
async def echo(message: types.Message):
    await message.answer("Это каталог", reply_markup=reply.del_kb)
    # Асинхронно вызываем функцию price и обрабатываем данные
    data_catalog = await catalog()

    await message.answer(f"{print(data_catalog)}")


@user_private_router.callback_query(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    message_text = callback_query.data  # Извлечение текста сообщения из callback_data
    await bot.answer_callback_query(callback_query.id, text='Вы нажали кнопку!')
    await bot.send_message(callback_query.from_user.id, f'Вы передали сообщение: {message_text}')

