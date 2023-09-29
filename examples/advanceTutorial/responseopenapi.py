from typing import Union

from fastapi import FastAPI, responses
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
	id: str
	value: str



responsess = {
	404: {"description": "Item not found"},
	302: {"description": "The item was moved"},
	403: {"description": "Not enough privileges"},
}


class Message(BaseModel):
	message: str


app = FastAPI()



@app.get(
	"/items/{item_id",
	response_model=Item,
	responses={**responses, 200: {"content": {"image/png":()}}}

)
async def read_item(item_id: str, img: Union[bool, None] = None):
	if item_id == "foo":
		return {"id": "foo", "value": "there goes my hero"}
	else:
		return JSONResponse(status_code=404, content={"message": "Item not found"})