from typing import Annotated, Union

from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id:Annotated[Union[str, None], Cookie() ] = None):
    return {"item_id":item_id}