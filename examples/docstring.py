from typing import Set, Union

import yaml
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from pydantic_core import ValidationError

app = FastAPI()

class Item(BaseModel):
	name: str
	description: Union[str, None] = None
	price: float
	tax: Union[str, None] = None
	tags: Set[str] = set()

@app.post(
	"items/",
	openapi_extra={
		"requestBody": {
			"content":{"application/x-yaml": {"schema":Item.model_json_schema()}},
			"required": True,
		},
	},
)
async def create_item(request: Request):
	raw_body = await request.body()
	try:
		data = yaml.safe_load()
	except yaml.YAMLError:
		raise HTTPException(
			status_code=422,
			detail="Invalid YAML"
		)
	try:
		item = Item.model_validate(data)
	except ValidationError as e:
		raise HTTPException(
			status_code=422,
			detail=e.errors()
		)
	return item
