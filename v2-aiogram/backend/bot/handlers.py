# separately stored handlers

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.database.requests import get_ingredients, find_recipes_by_ingredients, search_cocktail_by_name

router = Router() # a connecting obj with run file

search_ingrs = False # identifies if we are searching ingrs or not
search_cocktails = False # identifies if we are searching cocktails or not
ingrs_list = [] # list of ingredients will be filled with users ingrs


@router.message(CommandStart())
async def command_start_handler(message: Message):
    """
    This handler receives messages with `/start` command
    """
    await message.answer("Привет! Я бот, который поможет тебе выбрать коктейль на основе твоих ингредиентов.\nЧтобы начать, нажми кнопку 'Ввести ингредиенты'. Можешь ввести первые несколько букв или даже одну, а я предложу тебе варианты известных мне ингредиентов. \nКогда закончишь, нажми кнопку 'Давай рецепты!'", reply_markup=kb.main_kb) # a handler for start command


@router.message(lambda message: message.text == 'Ввести ингредиенты')
async def command_give_instruction_handler(message: Message):
    """
    This handler identifies that adding ingredients is started
    """
    await message.answer('Жду ингредиенты...')
    global search_ingrs
    search_ingrs = True


@router.message(lambda message: message.text == 'Мои ингредиенты')
async def command_give_instruction_handler(message: Message):
    """
    This handler identifies that adding ingredients is finished
    """
    # await message.answer('Ингредиенты приняты!')
    global search_ingrs
    search_ingrs = False
    global ingrs_list
    show_ingrs = ''
    for ingr in ingrs_list:
        show_ingrs += ' - '
        show_ingrs += ingr
        show_ingrs += '\n'

    if len(ingrs_list):
        await message.answer(f'Твой список ингредиентов:\n{show_ingrs}')
        await message.answer(f'Если все ингредиенты введены правильно, жми "Давай рецепты!" Если нет - жми "Ввести ингредиенты" и добавляй дальше')
    else:
        await message.answer(f'Нет ингредиентов. Введи, плиз.')


@router.message(lambda message: message.text == 'Давай рецепты!')
async def command_give_instruction_handler(message: Message):
    """
    This handler gives recipes with user ingrs
    """
    global ingrs_list

    res = await find_recipes_by_ingredients(ingrs_list)
    # try pretty recipe output
    # тут тренирую красивый вывод
    # тут напишу, что понадобится, типа вот, что вам нужно, а вот алгоритм
    res_text = ''
    cocktail_num = 0

    for k in res.keys():
        cocktail_num += 1
        print(k) # name of cocktail
        res_text += f'Коктейль №{cocktail_num}: "{k}"'
        res_text += '\n\n'

        print(res[k]['ingredients']) # list of ingredients
        for ingr in res[k]['ingredients']:
            ingr_str = ' - '
            for v in ingr.values():
                ingr_str += f'{v} '                
            print(ingr_str)
            res_text += ingr_str
            res_text += '\n'

        print(res[k]['instruction']) # instruction of cocktail
        res_text += '\n'
        res_text += res[k]['instruction']
        res_text += '\n\n'

    await message.answer(res_text)


@router.message(lambda message: message.text == 'Очистить мои ингредиенты')
async def command_give_instruction_handler(message: Message):
    """
    This handler makes ingredients' list empty
    """
    await message.answer('Список с ингредиентами очищен')
    global search_ingrs
    search_ingrs = False
    global ingrs_list
    ingrs_list = []
    # await message.answer(f'Ingredients list: {ingrs_list}')


# # Обработчик кнопки "Искать по названию коктейля"
# @router.message(lambda message: message.text == 'Искать по названию коктейля')
# async def command_give_instruction_handler(message: Message):
#     """
#     Этот обработчик отправляет запрос пользователю ввести название коктейля
#     """
#     # Отправляем сообщение, что нужно ввести название коктейля
#     await message.answer("Пожалуйста, введите название коктейля для поиска с заглавной буквы:")
    
#     # Отправляем сообщение с кнопкой "Завершить поиск"
#     await message.answer("Если хотите завершить поиск, нажмите 'Завершить поиск'.")



# # Обработчик для текста, который пользователь введет
# @router.message()
# async def handle_user_input(message: Message):
#     """
#     Этот обработчик ищет коктейли по введенному пользователем тексту
#     """
#     user_input = message.text.strip()  # Извлекаем текст из сообщения пользователя

#     # Если пользователь нажал кнопку "Завершить поиск", прекращаем обработку поиска
#     if user_input == "Завершить поиск":
#         await message.answer("Поиск завершен. Бот больше не будет обрабатывать запросы на поиск.")
#         return  # Прекращаем обработку любых дальнейших сообщений

    
#     # Если текст не является командой "Искать по названию коктейля", выполняем поиск
#     if user_input and user_input != 'Искать по названию коктейля':
#         # Ищем коктейли, чьи названия содержат введенную подстроку
#         cocktails = await search_cocktail_by_name(user_input)
        
#         if cocktails:
#             # Если коктейли найдены, отправляем их пользователю
#             response = "Найдено коктейлей:\n\n"
#             for cocktail in cocktails:
#                 response += f"🍹 {cocktail.name}\n"
#                 response += f"Инструкция: {cocktail.instruction}\n\n"
#             await message.answer(response)
#         else:
#             # Если ничего не найдено
#             await message.answer("Коктейли с таким названием не найдены.")


@router.callback_query()
async def handle_callback_query(callback_query: CallbackQuery):
    """
    Обрабатывает callback-запросы от инлайн-клавиатуры.
    """
    data = callback_query.data
    if data.startswith("ingredient_"):
        ingredient = data[len("ingredient_"):].replace("_", " ").capitalize()
        
        global ingrs_list
        # Добавляем ингредиент в список
        if ingredient not in ingrs_list:
            ingrs_list.append(ingredient)
        
        await callback_query.message.answer(f"Ингредиент '{ingredient}' добавлен в список.")
        await callback_query.answer()  # Отвечаем на callback-запрос, чтобы убрать анимацию


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

        if filtered_ingredients:
            # Создание инлайн-клавиатуры с предложениями
            suggestions_kb = kb.create_ingredient_suggestions(filtered_ingredients)
            await message.answer("Выбирай ингредиенты:", reply_markup=suggestions_kb)
        else:
            await message.answer("Нет ингредиентов, начинающихся с этого текста :(")



    