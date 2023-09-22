from fastapi import FastAPI, Form, Fil
from typing_extensions import Annotated



app = FastAPI()

@app.post("/logins/")
async def create_login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
