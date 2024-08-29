import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from dotenv import load_dotenv
import aiohttp
import asyncio

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для получения данных каталога
async def fetch_catalog():
    url = "https://megacvet24.ru/mobile_app/full"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                logging.info(f"Catalog data fetched successfully: {data}")
                return data
            else:
                logging.error(f"Failed to fetch catalog data. Status code: {response.status}")
                return []

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Введите запрос в строке поиска, чтобы найти товары.")

@dp.inline_query()
async def inline_query_handler(query: InlineQuery):
    query_text = query.query.lower()
    catalog_data = await fetch_catalog()

    if not catalog_data:
        logging.warning("No catalog data available.")
        return

    results = []
    for item in catalog_data:
        if query_text in item['name'].lower():
            result = InlineQueryResultArticle(
                id=item['article'],
                title=item['name'],
                input_message_content=InputTextMessageContent(
                    message_text=f"{item['name']}\nЦена: {item['price']} рублей",
                    parse_mode="Markdown"
                ),
                thumb_url=item['image'][0] if item['image'] else None,
                description=f"{item['price']} рублей"
            )
            results.append(result)

    await query.answer(results, cache_time=1, is_personal=True)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())