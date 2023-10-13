from pydantic import BaseModel
from typing import Annotated
from fastapi import Query

from main import app

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get("/item/{item_id}")
async def get_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item


# And of course, you can define some parameters as required, some as having a default value, and some entirely optional

@app.get("/items/{item_id}")
async def read_user_item(
        item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {
        "item_id": item_id, "needy": needy, "skip": skip, "limit": limit
    }


# When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.

# A request body is data sent by the client to your API. A response body is the data your API sends to the client.

# Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time.

# REQUEST BODY
class Item(BaseModel):
    name :str
    price: float
    description: str | None
    tax: float | None
    
@app.post("/item/")
async def create_item(item:Item):
    item_dict= item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax" : price_with_tax})
    return item_dict

# RESQUEST BODY + PATH PARAMETER

@app.put("/items/{item_id}")
async def create_item(item_id:int, item: Item, q: str | None = None):
    result ={"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q":q})
    return result


#QUERY PARAMETER AND STRING VALIDATION
@app.get("/item")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None
):
    results ={[{"item_id":"Foo"}, {"item_id":"Koo"}]}
    if q:
        results.update({q:"q"})
    return results

