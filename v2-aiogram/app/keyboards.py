# bot keyboard description

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# main keyboard
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Gimme cocktails!')],
    [KeyboardButton(text='Add ingredients')],
    [KeyboardButton(text='Stop adding ingredients')],
    [KeyboardButton(text='Clean ingredients')],
    [KeyboardButton(text='RECIPE')],
    [KeyboardButton(text='Help - mock')]
])


def create_ingredient_suggestions(ingredients):
    # Создаем список строк, каждая строка - это список кнопок
    # inline_keyboard = [[InlineKeyboardButton(text=ingredient, callback_data=f"ingredient:{ingredient}")]
    #                    for ingredient in ingredients]
    inline_keyboard = [[InlineKeyboardButton(text=ingredient, callback_data=f"ingredient_{ingredient.lower()}")]
                       for ingredient in ingredients]
    
    # Создаем объект клавиатуры с параметром inline_keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard

# def create_ingredient_suggestions(ingredients):
#     """
#     Создает инлайн-клавиатуру с предложениями ингредиентов.
#     """
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     buttons = [
#         InlineKeyboardButton(text=ingredient, callback_data=f"ingredient_{ingredient.lower()}")
#         for ingredient in ingredients
#     ]
#     keyboard.add(*buttons)
#     return keyboard
