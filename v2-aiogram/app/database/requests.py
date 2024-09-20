# requests to DB

from app.database.models import Ingredient, async_session, RecipeIngredient, Recipe
from sqlalchemy import select, func
from sqlalchemy.orm import aliased

# get all ingredients from DB
# TO DO - not all of course - too many
async def get_ingredients() -> list:
    async with async_session() as session:
        # Выполняем запрос, чтобы получить все  ингредиенты
        result = await session.execute(select(Ingredient))
        
        # Извлекаем скалярные результаты
        ingredients = result.scalars().all()
        
        # Преобразуем в список названий ингредиентов
        ingredient_names = [ingredient.name for ingredient in ingredients]
        
        # Возвращаем список ингредиентов
        return ingredient_names


# Асинхронная функция для поиска рецептов по списку ингредиентов
async def find_recipes_by_ingredients(ingredient_names: list[str]) -> list[dict]:
    async with async_session() as session:  # Используем контекст с асинхронной сессией
        ingredient_alias = aliased(Ingredient)  # Создаем алиас для таблицы ингредиентов

        lowercase_ingrs = [ingr.lower() for ingr in ingredient_names]
        
        print(f'AAAA {lowercase_ingrs}')
        # # Подзапрос для фильтрации рецептов, содержащих все указанные ингредиенты
        # subquery = (
        #     select(Recipe.id)
        #     .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id) # Явно указываем, как соединять Recipe с RecipeIngredient
        #     .join(ingredient_alias, ingredient_alias.id == RecipeIngredient.ingredient_id)
        #     .filter(ingredient_alias.name.in_(ingredient_names))
        #     .group_by(Recipe.id)
        #     .having(func.count(RecipeIngredient.ingredient_id) == len(ingredient_names))
        # ).subquery()

        # # Основной запрос для получения названия рецепта, инструкции и ингредиентов
        # query = (
        #     select(Recipe.name, Recipe.instruction, Ingredient.name, RecipeIngredient.quantity, RecipeIngredient.unit)
        #     .select_from(Recipe)  # Явно указываем, что начинаем с Recipe
        #     .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)  # Указываем, как соединять с RecipeIngredient
        #     .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id)  # Указываем соединение с Ingredient
        #     .filter(Recipe.id.in_(subquery))  # Фильтруем рецепты по подзапросу
        # )

        query = (
            select(Recipe.id, Recipe.name, Recipe.instruction, Ingredient.name, RecipeIngredient.quantity, RecipeIngredient.unit)
            .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)
            .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id)  # Указываем соединение с Ingredient
            .filter(Ingredient.name.in_(lowercase_ingrs))  # Фильтрация по списку ингредиентов
            .select_from(Recipe) # Явно указываем, что начинаем с Recipe
        )

        # Выполняем запрос
        result = await session.execute(query)
        rows = result.all()

        recipes = {}
        for recipe_id, recipe_name, instruction, ingredient_name, quantity, unit in rows:
            if recipe_name not in recipes:
                recipes[recipe_name] = {
                    'instruction': instruction,
                    'ingredients': []
                }
            # Добавляем ингредиенты к рецепту
            recipes[recipe_name]['ingredients'].append({
                'name': ingredient_name,
                'quantity': quantity,
                'unit': unit
            })
        
        return recipes


        # Возвращаем список рецептов с ингредиентами
        return recipes