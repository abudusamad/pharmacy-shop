from typing import Annotated
from fastapi import Depends, HTTPException, FastAPI,Header

app = FastAPI()

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token
    
async def verif_key(x_key: Annotated[str, Header()]):
    if x_key != "fakw-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key
    
@app.get("/items/", dependencies=[Depends(verify_token), Depends(verif_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Benz"}]