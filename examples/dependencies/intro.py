from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"},{"item_name": "Bars"},{"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str |None = None, skip: int = 0, limit: int =100):
        self.q = q
        self.skip = skip
        self.limit = limit
        

# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}

# CommonsDep = Annotated[dict, Depends(common_parameters)]

# @app.get("/items/")
# async def read_items(common: CommonsDep):
#     return common

# @app.get("/users/")
# async def read_users(commons: CommonsDep):
#     return commons

@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response={}
    if commons.q:
        response.update({"q": commons.q})
        items = fake_items_db[commons.skip : commons.skip + commons.limit]
        response.update({"items": items})
    return response