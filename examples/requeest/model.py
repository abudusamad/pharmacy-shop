from typing import Any, List, Union
from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags : List[str] = []
    
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item

@app.get("/items", response_model= List[Item])
async def read_item() -> Any:
    return [
        Item(name= "Portal Gun", price = 43.5),
        Item(name = " Plumbus", price = 45.4, description="The name of the product is the same"),
    ]