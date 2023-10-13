from typing import Annotated


from fastapi import FastAPI, Form, File, UploadFile



app = FastAPI()

@app.post("/logins/")
async def create_login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return { "message": "No file sent"}
    else:   
        return {"file_size": len(file)}

@app.post("/uploadfiles/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:      
        return{"filename": file.filename}