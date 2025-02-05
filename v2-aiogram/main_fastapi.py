from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Добро пожаловать в API коктейлей!"}
