from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: int
    is_active: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"messages": "Hello world"}


app.get("/items/{items_id}")


def read_items(items_id: int, q: Union[str, None] = None):
    return {"items_id": items_id, "q": q}


@app.put("/items/{items_id}")
def put_items(items_id: int, items: Item):
    return {"Items_name": items.name, "item_id": items_id}

def get_inform():
    return{"message": "Hello World"}