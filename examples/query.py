from main import app

fake_items_db= [{"item_name":"Foo"}, {"item_name":"Bar"},{"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip:int =0, limit:int =10):
    return fake_items_db[skip: skip +limit]

@app.get("/item/{item_id}")

async def get_item(item_id:str, q: str|None =None):
    if q:
        return{"item_id": item_id, "q":q}
    return{"item_id":item_id}

@app.get("/items/{item_id}")
async def read_item(item_id:str, q:str|None = None, short:bool =False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
        
    return item

#And of course, you can define some parameters as required, some as having a default value, and some entirely optional

@app.get("/items/{item_id}")
async def read_user_item(
item_id:str, needy:str, skip:int=0, limit:int | None=None
):
    item = {
        "item_id":item_id, "needy":needy,"skip":skip, "limit":limit
    }