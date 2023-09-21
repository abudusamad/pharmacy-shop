from fastapi import FastAPI, status
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from fastapi.encoders import jsonable_encoder


app = FastAPI()

# Tags with Enums¶
# If you have a big application, you might end up accumulating several tags, and you would want to make sure you always use the same tag for related path operations.

# In these cases, it could make sense to store the tags in an Enum.

# FastAPI supports that the same way as with plain strings:

class Tags(Enum):
    items= "items"
    users: "users"
    
@app.get("/items/", tags=[Tags.items])
async def get_items():
    return["Portal gun", "Plumbus"]

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Risky", "Morty"]

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags= set[str] = []
    title: str
    timestamp: datetime
    description: str | None = None

    

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

fake_db = {}

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
