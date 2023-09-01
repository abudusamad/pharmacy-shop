from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def index():
    return {"hello": "World"}


students ={
    1:{
        "name": "John",
        "age": 23,
        "class": "year 4"
    }
}

class student(BaseModel):
    name:str
    age: int
    year: str
    
    
@app.get("/get_student/{student_id}")
def get_student(student_id : int = Path( description= "Enter the ID you want to view", gt=0, lt=10)):
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student_name(*, student_id:int, name:Optional [str], test: int):
    for student_id in students:
        if students[student_id]["name"] == "name":
            return students[student_id]
    return {"Data" : "Not found"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student:student):
    if student_id in students:
        return{"Error" : " Student already exits"}
    students[student_id] = student
    return students[student_id]