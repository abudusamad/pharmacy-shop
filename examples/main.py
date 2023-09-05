from fastapi import FastAPI

app =FastAPI()

@app.get("/")

def get_inform():
    return{"message": "Hello World"}