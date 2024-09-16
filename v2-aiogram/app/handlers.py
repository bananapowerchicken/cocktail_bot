# separately stored handlers

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.database.requests import get_ingredients

router = Router() # a connecting obj with run file

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


# # test button - shows ingredients from db table
# @router.message(lambda message: message.text == 'Test show ingrs')
# async def command_give_instruction_handler(message: Message):
#     """
#     This handler shows ingredients from db table
#     """
#     ingredients = await get_ingredients()
#     print(ingredients)
#     await message.answer(f'Here are all ingredients we have: \n {ingredients}')


@router.message()
async def handle_user_input(message: Message):
    """
    Этот хендлер обрабатывает ввод пользователя и показывает предложения
    """
    user_input = message.text.lower()

    # Получение всех ингредиентов из базы данных
    all_ingredients = await get_ingredients()
    
    # Фильтрация ингредиентов, которые начинаются с введенного текста
    filtered_ingredients = [ingredient for ingredient in all_ingredients if ingredient.lower().startswith(user_input)]
    filtered_ingredients = ['vodka', 'water']
    if filtered_ingredients:
        # Создание инлайн-клавиатуры с предложениями
        suggestions_kb = kb.create_ingredient_suggestions(filtered_ingredients)
        await message.answer("Here are some suggestions:", reply_markup=suggestions_kb)
    else:
        await message.answer("No matching ingredients found.")

# @router.callback_query(lambda c: c.data.startswith("ingredient:"))
# async def handle_ingredient_selection(message: Message):
#     """
#     Этот хендлер обрабатывает выбор ингредиента из инлайн-кнопок
#     """
#     ingredient = callback_query.data.split(':', 1)[1]
    
#     # Вы можете сохранить выбранный ингредиент или использовать его по вашему усмотрению
#     await message.answer(callback_query.from_user.id, f'You selected: {ingredient}')
    
#     # Можно запросить дополнительную информацию или продолжить ввод
#     await message.answer(callback_query.from_user.id, "Continue typing more ingredients or type /done to finish.")
    
#     await callback_query.answer()

# @router.message(lambda message: message.text.lower() == '/done')
# async def process_done(message: types.Message):
#     """
#     Этот хендлер обрабатывает команду /done и завершает сбор ингредиентов
#     """
#     # Завершите процесс сбора ингредиентов
#     await message.answer("You have finished entering ingredients.")