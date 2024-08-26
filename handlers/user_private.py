import requests, json, asyncpg
from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from data import price


from keyboards import reply


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
            if value:
                values.append(value)

    # Форматируем данные для вывода
    formatted_values = "\n".join(values)

    await message.answer(f"Полученные данные:\n{formatted_values}", reply_markup=reply.test_kb)