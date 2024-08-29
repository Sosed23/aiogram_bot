import aiohttp
import asyncio
from pprint import pprint
import json

async def catalog():
    url = "https://megacvet24.ru/mobile_app/full"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            unique_categories = []
            for poz in data[:10000]:
                string_values = dict(poz)
                string_values_category = string_values.get('category')

                if string_values_category not in unique_categories:
                    unique_categories.append(string_values_category)

            print(sorted(unique_categories))

results = asyncio.run(catalog())

# # Функция для получения первых 10 элементов из списка с выводом только артикула, картинки и цены
# def get_first_ten_elements_with_info(data):
#     elements = list(data)
#
#     for i in range(100):
#         element = elements.pop()
#         # Вывод информации о каждом элементе
#
#         print(element['category'])
#
# #         print(element['article'])
# #         print(element['image'][0])
# #         print(element['price'])
# #         print(f"{element['article']}, {element['name']}")
# #
# # # Вызов функции и вывод результатов

# get_first_ten_elements_with_info(results)
