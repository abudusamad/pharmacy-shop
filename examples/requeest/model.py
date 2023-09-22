from typing import Any, List, Union
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse

from pydantic import BaseModel, EmailStr

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags : List[str] = []
    
class BaseUser(BaseModel):
    username:str
    email: EmailStr
    full_name: str | None = None
    
class UserIn(BaseUser):
    password: str
    
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item

@app.post("/users/")
async def create_user(user: UserIn) -> BaseUser:
    return user
@app.get("/items/", response_model= List[Item])
async def read_item() -> Any:
    return [
        Item(name= "Portal Gun", price = 43.5),
        Item(name = " Plumbus", price = 45.4, description="The name of the product is the same"),
    ]

@app.get("/portals/")
async def get_portal(teleport: bool =False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?")
    return JSONResponse(content=("message": "Here's your interdimensional portal."))