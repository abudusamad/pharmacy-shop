from main import app

from enum import Enum

class ModelName(str, Enum):
    alenet:"alenet"
    lenet:"lenet"
    opnet:"lenet"
    
@app.get("/model/{model_name}")
async def get_model(model__name: ModelName):
    if model__name is ModelName.alenet:
        return{"model_name": model__name, 'message': "deep Learning"}
    if model__name.value == "lenet":
        return{"model_name":model__name, "message":"all the images"}
    return{"model_name":model__name,"message":"Have some residuals"}