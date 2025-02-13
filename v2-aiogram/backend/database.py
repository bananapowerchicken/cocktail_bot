# connection to the database

import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv


# load vars from .env file 
load_dotenv()
SQL_ALCHEMY_URL = os.getenv('SQL_ALCHEMY_URL')
engine = create_async_engine(SQL_ALCHEMY_URL, echo=True) # echo True = logging on

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
