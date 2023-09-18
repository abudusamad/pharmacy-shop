from datetime import datetime
from typing import Annotated, Union

from fastapi import Body, FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI()

items = {
	"foo": {"name": "fighters", "size": 6},
	"bar": {"name": "Tenders", "size": 3}
}

class Item(BaseModel):
	title: str
	timestamp: datetime
	description: Union[str, None] = None



@app.put("items/{item_id")
async def upsert_item(
		item_id: str,
		name: Annotated[str | None, Body()] = None,
		size: Annotated[str | None, Body()] = None,
):
	if item_id in items:
		item = items[item_id]
		item["name"] = name
		item["size"] = size
		return item
	else:
		item = {"name": name, "size": size}
		items[item_id] = item
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


@app.put("items/{id}")
def update_item(id: str, item: Item):
	json_compatible_item_data = jsonable_encoder(item)
	return JSONResponse(content=json_compatible_item_data)
