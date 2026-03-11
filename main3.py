from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

class Employee(BaseModel):
    name:str
    department:str
    salary :int

class UpdateEmployee(BaseModel):
    name:Optional[str]=None
    department:Optional[str]=None
    salary:Optional[int]=None

employees=[
    {
        "id":1,"name":"vinit","department":"it","salary":30000
    }
]

@app.patch("/employees/{emp_id}")
def update_employee(emp_id:int,emp:UpdateEmployee):
    for employee in employees:
        if employee["id"]==emp_id:
            if emp.name is not None:
                employee["name"]=emp.name
            if emp.department is not None:
                employee["department"]=emp.department
            if emp.salary is not None:
                employee["salary"]=emp.salary

            return {"message":"Employee updated ","data":employee}
    raise HTTPException(status_code=404,detail="Employee not found")