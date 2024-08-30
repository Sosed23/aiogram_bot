from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
# from megacvet_json import results
from database.orm_query import orm_get_categories, get_categories

def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_url_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()


# Создать микс из CallBack и URL кнопок
def get_inlineMix_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()

def inline_kb():
    btns = {
        'Кнопка 1': 'button1',
        'Кнопка 2': 'button2'
    }
    return get_callback_btns(btns=btns)

cars = ['Агапантус', 'Аллиум', 'Алхемилла', 'Альстромерии', 'Амарант сухоцвет', 'Амарантусы', 'Амариллисы', 'Амми сухоцвет', 'Ананасы', 'Анемоны', 'Антирринум (Львиный Зев)', 'Антуриумы', 'Артишоки', 'Аспарагус сухоцвет', 'Астеры', 'Астильбы', 'Астранция', 'Астры', 'Брассика', 'Бруния', 'Бруния сухоцвет', 'Бувардия', 'Букет невесты', 'Букеты', 'Букеты Дня', 'Букеты Любимой', 'Букеты из сухоцветов', 'Букеты с Перьями', 'Булгур сухоцвет', 'Бутоньерка', 'Вазы', 'Верба', 'Вероника', 'Ветки ели', 'Вибурнумы', 'Воздушные Шары', 'Гвоздики', 'Гелихризум сухоцвет', 'Гениста', 'Георгины', 'Герберы', 'Гермини', 'Гиацинты', 'Гиперикумы', 'Гипсофилы', 'Гипсофилы оптом', 'Гладиолусы', 'Гомфрена сухоцвет', 'Гортензии', 'Декор для букетов', 'Декоративные фрукты', 'Декоративные ягоды', 'Дельфиниум', 'Зелень', 'Илексы', 'Ирисы', 'Календулы', 'Каллы', 'Картамус', 'Керамика', 'Ковыль сухоцвет', 'Комнатные растения', 'Конверты', 'Конфеты', 'Корилус сухоцвет', 'Краспедия сухоцвет', 'Лаванда Сухоцвет', 'Лагурус сухоцвет', 'Латексные шары', 'Лепестки Роз', 'Леукодендрон', 'Леукоспермумы', 'Лизиантус', 'Лилии', 'Лимониум', 'Лимонные деревья', 'Лотосы', 'Лунария сухоцвет', 'Лён оптом', 'Лён сухоцвет', 'Маттиолы', 'Мимоза оптом', 'Мимозы', 'Мускари', 'Мягкие игрушки', 'Наборы Конфет', 'Наборы Шаров', 'Нарциссы', 'Нигелла сухоцвет', 'Новогодние букеты', 'Новогодние венки', 'Новогодние елки', 'Новогодние подсвечники', 'Новогодний декор', 'Овёс сухоцвет', 'Озотамнус сухоцвет', 'Оксипеталумы', 'Оранжевые Розы', 'Орнитогалумы', 'Орхидеи', 'Орхидея Дендробиум', 'Открытки', 'Пампасная Трава сухоцвет', 'Пионовидные Розы', 'Пионы', 'Писташ', 'Подарки', 'Подарочные наборы', 'Подарочные пакеты', 'Подсолнухи', 'Протеи', 'Пшеница сухоцвет', 'Ранункулюсы', 'Растения', 'Роза Эквадор', 'Роза стабилизированная', 'Розы', 'Розы оптом', 'Ромашки', 'Сантини', 'Свечи', 'Седумы', 'Семейный букет', 'Сенецио', 'Симфорикарпусы', 'Сирень', 'Сирень оптом', 'Скабиоза сухоцет', 'Скимии', 'Солидаго', 'Стабилизированные Розы', 'Стабилизированные Цветы', 'Статица', 'Сухоцветы', 'Сухоцветы оптом', 'Топперы', 'Траурные букеты', 'Траурные композиции', 'Трахелиум', 'Тюльпаны', 'Упаковка для букета', 'Фаленопсис', 'Фалярис сухоцвет', 'Физалисы', 'Фольгированные шары', 'Фрезии', 'Фрукты', 'Хамелациумы', 'Хвойные ветки', 'Хлопок Сухоцвет', 'Хризантемы', 'Цветы', 'Цветы оптом', 'Цветы поштучно', 'Целозия', 'Цены', 'Чашки', 'Шишки сухоцвет', 'Шоколадки', 'Эвкалипт', 'Эрингиумы', 'Эустомы']

def inline_cars():
    keybord = InlineKeyboardBuilder()
    for car in cars:
        keybord.add(InlineKeyboardButton(text=car, callback_data=f"car_{car}"))
    return keybord.adjust(2).as_markup()

async def categories():
    all_categories = await get_categories()
    for category in all_categories:
        name = f"{category.name}"
        print(name)

if __name__ == "__main__":
    asyncio.run(get_categories())