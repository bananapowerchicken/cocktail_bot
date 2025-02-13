# bot keyboard description

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# main keyboard
# main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
#     keyboard=[
#     [KeyboardButton(text='Ввести ингредиенты')],
#     [KeyboardButton(text='Мои ингредиенты')],
#     [KeyboardButton(text='Очистить мои ингредиенты')],
#     [KeyboardButton(text='Давай рецепты!')],
#     [KeyboardButton(text='Искать по названию коктейля')],
#     [KeyboardButton(text='Завершить поиск')],
# ])

# 2 buttons in row
main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, keyboard=[
    [KeyboardButton(text='Ввести ингредиенты'), KeyboardButton(text='Мои ингредиенты')],
    [KeyboardButton(text='Очистить мои ингредиенты'), KeyboardButton(text='Давай рецепты!')],
    # [KeyboardButton(text='Искать по названию коктейля'), KeyboardButton(text='Завершить поиск')],
])


def create_ingredient_suggestions(ingredients):
    # Создаем список строк, каждая строка - это список кнопок
    inline_keyboard = [[InlineKeyboardButton(text=ingredient, callback_data=f"ingredient_{ingredient.lower()}")]
                       for ingredient in ingredients]
    
    # Создаем объект клавиатуры с параметром inline_keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard

