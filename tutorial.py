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

class Student(BaseModel):
    name: str
    age: int
    year: str


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    Year: Optional[str] = None
    
    
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
def create_student(student_id: int, student:Student):
    if student_id in students:
        return{"Error" : " Student already exits"}
    students[student_id] = Student
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id:int, student:StudentUpdate):
    if student_id not in students:
        return {"Error" : "Student does not exist"}
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.year != None:
        students[student_id].year = student.year
        return students[student_id]


 @app.delete("/delete-student/{student_id}")
  def delete_student(student_id: int):
    if student_id is not in students:
        return{"Error": "Student does not exit"}
    del students[student_id]
    return {"message": "Student deleted successfully"}