from typing import Union, List
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tag: List[str] = []
    
@app.put("/items{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id":item_id, "item": item}
    return results