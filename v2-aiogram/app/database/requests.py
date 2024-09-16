# requests to DB

from app.database.models import Ingredient, async_session
from sqlalchemy import select


async def get_ingredients():
    async with async_session() as session:
        res = await session.execute(select(Ingredient))
        ingredients = res.scalars().all()
        return ingredients

