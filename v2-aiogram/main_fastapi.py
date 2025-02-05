# http://127.0.0.1:8000 - address
# uvicorn main:app --reload - launch

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import Recipe, async_session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# helps to display the recipes - smth with cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Получаем сессию для работы с БД
def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home():
    return {"message": "Добро пожаловать в API коктейлей!"}


@app.get("/recipes")
async def get_recipes(db: AsyncSession = Depends(get_db)):
    # Выполняем асинхронный запрос к БД
    query = select(Recipe)
    result = await db.execute(query)
    recipes = result.scalars().all()  # Получаем все рецепты

    # Возвращаем рецепты в формате JSON
    return [{"id": recipe.id, "name": recipe.name, "instruction": recipe.instruction} for recipe in recipes]

