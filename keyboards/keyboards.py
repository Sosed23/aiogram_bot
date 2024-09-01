from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardButton, InlineKeyboardMarkup
# from database.query import get_categories
from database.query_postgresql import get_categories, get_category_product


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Корзина')],
                                     [KeyboardButton(text='Контакты'),
                                      KeyboardButton(text='О нас')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


# async def categories():
#     all_categories = await get_categories()
#     keydoard = InlineKeyboardBuilder()
#     for category in all_categories:
#         keydoard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
#     keydoard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
#     return keydoard.adjust(2).as_markup()


async def categories():
    all_categories = await get_categories()
    keydoard = InlineKeyboardBuilder()
    for category in all_categories:
        keydoard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keydoard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keydoard.adjust(2).as_markup()


async def products(category_id):
    all_products = await get_category_product(category_id)
    keyboard = InlineKeyboardBuilder()
    for product in all_products:
        keyboard.add(InlineKeyboardButton(text=product.name, callback_data=f"product_{product.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()



