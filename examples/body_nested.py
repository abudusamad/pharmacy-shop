from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Image(BaseModel):
    name: str
    url: HttpUrl


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tag: set[str] = set()
    img: List[Image] | None = None
    
class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: List[Item]


@app.put("/items{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.post('/offers/')
async def post_offer(offer: Offer):
    return offer
