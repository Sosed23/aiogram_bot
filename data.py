from dotenv import load_dotenv
import os, requests, pprint
import aiohttp
import asyncio


load_dotenv()

PF_TOKEN = os.environ.get("PF_TOKEN")
PF_URL = os.environ.get("PF_URL")

async def price():
    url = f"{PF_URL}/directory/1430/entry/list"

    headers = {
        'Authorization': 'Bearer {}'.format(PF_TOKEN),
        'accept': 'application/json'
    }

    body = {
      "offset": 0,
      "pageSize": 100,
      "fields": "name,4304,key",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as response:
            return await response.json()

print(asyncio.run(price()))


# values = []
# for entry in response.get('directoryEntries', []):
#     custom_field_data = entry.get('customFieldData', [])
#     for field_data in custom_field_data:
#         value = field_data.get('value')
#         if value:
#             values.append(value)
#
# # Вывод значений
# for value in values:
#     print(value)
