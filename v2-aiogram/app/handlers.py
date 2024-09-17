# separately stored handlers

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.database.requests import get_ingredients

router = Router() # a connecting obj with run file

search_ingrs = False # identifies if we are searching ingrs or not

@router.message(CommandStart())
async def command_start_handler(message: Message):
    """
    This handler receives messages with `/start` command
    """
    await message.answer("Hello, I'm a cocktail bot!", reply_markup=kb.main_kb) # a handler for start command


# don't like that have to check the exact text on the btn!
@router.message(lambda message: message.text == 'Gimme cocktails!')
async def command_give_instruction_handler(message: Message):
    """
    This handler sends an instruction after pressing Gimme cocktail btn
    """
    await message.answer('Please, type your ingredients')


@router.message(lambda message: message.text == 'Add ingredients')
async def command_give_instruction_handler(message: Message):
    """
    This handler identifies that adding ingredients is started
    """
    await message.answer('Waiting for your ingredients')
    global search_ingrs
    search_ingrs = True

@router.message()
async def handle_user_input(message: Message):
    """
    Этот хендлер обрабатывает ввод пользователя и показывает предложения
    """
    global search_ingrs  # Use global variable to check if we're searching for ingredients

    print(search_ingrs)

    if search_ingrs:
        user_input = message.text.lower()

        # Получение всех ингредиентов из базы данных
        all_ingredients = await get_ingredients()
        
        # Фильтрация ингредиентов, которые начинаются с введенного текста
        filtered_ingredients = [ingredient for ingredient in all_ingredients if ingredient.lower().startswith(user_input)]
        # filtered_ingredients = ['vodka', 'water']
        if filtered_ingredients:
            # Создание инлайн-клавиатуры с предложениями
            suggestions_kb = kb.create_ingredient_suggestions(filtered_ingredients)
            await message.answer("Here are some suggestions:", reply_markup=suggestions_kb)
        else:
            await message.answer("No matching ingredients found.")

