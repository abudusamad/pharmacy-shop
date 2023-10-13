from fastapi import FastAPI,Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from pydantic import BaseModel

app = FastAPI()

@app.exception_handler(ResponseValidationError)
async def validatiton_exception__handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail":exc.errors(), "body": exc.body})
    )
    
class Item(BaseModel):
    title: str
    size: int
    
@app.post("/items/")
async def create_item(item: Item):
    return item