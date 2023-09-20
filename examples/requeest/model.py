from typing import List, Union, Any

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []
    
@app.post("/items/", response_model=Item)
async def create_items(item: Item) -> Any :
    return item

@app.get("/items/", response_model=List[Item])
async def read_items() -> Any:
    return[
        Item(name= "Portal Gun", price= 45.6),
        Item(name= "Plumbus", price=32.0)
    ]