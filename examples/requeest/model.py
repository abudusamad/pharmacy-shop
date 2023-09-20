from typing import List, Union, Any

from fastapi import FastAPI
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
    
