from typing import List, Union
from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags : List[str] = []
    
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items")
async def read_item() -> List[Item]:
    return [
        Item(name= "Portal Gun", price = 43.5),
        Item(name = " Plumbus", price = 45.4, description="The name of the product is the same"),
    ]