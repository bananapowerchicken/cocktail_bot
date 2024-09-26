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

        # Первый запрос: находим рецепты, в которых есть хотя бы один из указанных ингредиентов
        recipe_ids_query = (
            select(Recipe.id)
            .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)
            .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id)
            .filter(Ingredient.name.in_(lowercase_ingrs))
            .distinct()  # Избегаем дубликатов рецептов
        )

        # Выполняем первый запрос
        recipe_ids_result = await session.execute(recipe_ids_query)
        recipe_ids = [row[0] for row in recipe_ids_result]

        # Если нет рецептов с указанными ингредиентами, возвращаем пустой список
        if not recipe_ids:
            return {}

        # Второй запрос: находим все ингредиенты для найденных рецептов
        query = (
            select(Recipe.id, Recipe.name, Recipe.instruction, Ingredient.name, RecipeIngredient.quantity, RecipeIngredient.unit)
            .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)
            .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id)
            .filter(Recipe.id.in_(recipe_ids))  # Выбираем рецепты, которые были найдены на предыдущем этапе
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