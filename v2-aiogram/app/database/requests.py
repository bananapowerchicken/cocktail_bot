# requests to DB

from app.database.models import Ingredient, async_session
from sqlalchemy import select

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
