from dotenv import load_dotenv
import os, requests, pprint


load_dotenv()

PF_TOKEN = os.environ.get("PF_TOKEN")
PF_URL = os.environ.get("PF_URL")

def price():
    url = f"{PF_URL}/directory/1430/entry/list"

    headers = {
        'Authorization': 'Bearer {}'.format(PF_TOKEN),
        'accept': 'application/json'
    }

    body = {
      "offset": 0,
      "pageSize": 100,
      "fields": "name,4304,key,",
    }
    response = requests.post(url, headers=headers, data=body)
    return response.json()

# Получаем данные
data = price()
print(data)


# Проверяем, что данные получены и выводим только id
if isinstance(data, list):  # Если результат - это список
    for item in data:
        print(item.get('value'))  # Выводим только id
else:
    print(data.get('value'))  # Если результат - это один объект