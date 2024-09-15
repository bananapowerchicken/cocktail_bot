# describing database

import os

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv

# load vars from .env file 
load_dotenv()
SQL_ALCHEMY_URL = os.getenv('SQL_ALCHEMY_URL')

engine = create_async_engine(SQL_ALCHEMY_URL, echo=True) # echo True = logging on

async_session = async_sessionmaker(engine)

# to do: clear for what async attrs
class Base(AsyncAttrs, DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    instruction:  Mapped[str] = mapped_column(String(100))

    # Many-to-Many through RecipeIngredient table
    ingredients: Mapped[list["RecipeIngredient"]] = relationship('RecipeIngredient', back_populates='recipe')



class Ingredient(Base):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    # Many-to-Many through RecipeIngredient table
    recipes: Mapped[list["RecipeIngredient"]] = relationship('RecipeIngredient', back_populates='ingredient')


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    recipe_id:  Mapped[int] = mapped_column(ForeignKey('recipes.id'))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('ingredients.id'))
    quantity: Mapped[int] = mapped_column()
    unit: Mapped[str] = mapped_column(String(10))

    # many-to-one connections
    recipe = relationship('Recipe', back_populates='ingredients')
    ingredient: Mapped["Ingredient"] = relationship('Ingredient', back_populates='recipes')

