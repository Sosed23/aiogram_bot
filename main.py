import asyncio, requests
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.user_private import user_private_router

from dotenv import load_dotenv
import os

load_dotenv()


bot = Bot(token=os.environ.get("BOT_TOKEN"))
dp = Dispatcher()

dp.include_router(user_private_router)

# @dp.message(Command("history"))
# async def show_history(message: types.Message):
#     # Получение списка операций
#     operations = client.operations.list(label='1775933471')
#
#     # Вывод операций
#     for operation in operations:
#         print(operation.id, operation.amount, operation.date)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=['*'])

if __name__ == "__main__":
    asyncio.run(main())
