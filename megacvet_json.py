# import aiohttp
# import asyncio
# from pprint import pprint
# import json
#
# async def catalog():
#     url = "https://megacvet24.ru/mobile_app/full"
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             data = await response.json()
#             return data
#
# # Функция для получения первых 10 элементов из списка с выводом только артикула, картинки и цены
# def get_first_ten_elements_with_info(data):
#     elements = list(data)
#
#     for i in range(10):
#         element = elements.pop()
#         # Вывод информации о каждом элементе
#         print(element['article'])
#         print(element['image'][0])
#         print(element['price'])
#         print(f"{element['article']}, {element['name']}")
#
# # Вызов функции и вывод результатов
# results = asyncio.run(catalog())
# get_first_ten_elements_with_info(results)
