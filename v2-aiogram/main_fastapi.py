# http://127.0.0.1:8000 - address
# uvicorn main:app --reload - launch

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Добро пожаловать в API коктейлей!"}
