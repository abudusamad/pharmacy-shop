from typing import Annotated, Any

from fastapi import Depends, FastAPI

app= FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bens"}, {"item_name": "Bars"}]

class CommonQueryParamas:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
        

@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParamas, Depends()]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
        items=fake_items_db[commons.ski: commons.skip + commons.limit]
        response.update({"items": items})
        return response