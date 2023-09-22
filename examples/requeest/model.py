from typing import List, Union, Any

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Item(BaseModel):
    name:str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []

    
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None
    

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None
 
class UserIn(BaseUser):
    password: str
    
    
@app.post("/items/", response_model=Item)
async def create_items(item: Item) -> Any :
    return item

@app.post("/Users/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user

@app.get("/items/", response_model=List[Item])
async def read_items() -> Any:
    return[
        Item(name= "Portal Gun", price= 45.6),
        Item(name= "Plumbus", price=32.0)
    ]
    


@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Union[Response, dict]:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}




items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
