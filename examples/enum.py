from main import app

from enum import Enum

class ModelName(str, Enum):
    lexnet:"lexnet"
    masnet:"masnet"
    josnet:"josnet"

@app.get("/models/{model_name}")

async def get_model(model_name:ModelName):
    if model_name is ModelName.josnet:
        return {"model_name":model_name, "message":"Hellow josnet how are you"}
    if model_name.value == "lexnet":
        return {"model_name":model_name, "message":"printing the name of the lexnet"}
    return {"model_name": model_name, "message":"model is the same as the order one "}

