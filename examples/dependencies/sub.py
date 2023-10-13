from typing import Annotated
from fastapi import Depends, Cookie, FastAPI

app = FastAPI()

def query_extracor(q: str | None = None):
    return q
def query_or_cookies_extractor(
    q: Annotated[str, Depends(query_extracor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q

@app.get("/items/")
async def read_query(query_or_default: Annotated[str, Depends(query_or_cookies_extractor)]):
    return{"query_or_cookies": query_or_default}