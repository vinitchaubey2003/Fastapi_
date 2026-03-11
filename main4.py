from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

class Employee(BaseModel):
    name:str
    department:str
    salary:int

class Update_Employee(BaseModel):
    name:Optional[str]=None
    department:Optional[str]=None
    salary:Optional[int]=None

employees=[]
current_id=1

@app.post("/employees")
def create_employee(emp:Employee):
    global current_id

    new_employee={
        "id":current_id,
        "name":emp.name,
        "department":emp.department,
        "salary":emp.salary
    }
    employees.append(new_employee)
    current_id+=1

    return {
        "message":"Employee created ","data":new_employee
    }

@app.get("/employees")
def get_all_employees():
    return{
        "data":employees
    }
@app.get("/employees/{emp_id}")
def get_employee(emp_id:int):
    for employee in employees:
        if employee["id"]==emp_id:
            return {"data":employee}
    raise HTTPException(status_code=404,detail="employee not found")

#put->update
@app.put("/employees/{emp_id}")
def update_full_employee(emp_id:int,emp:Employee):
    for employee in employees:
        if employee["id"]==emp_id:
            employee["name"]=emp.name
            employee["department"]=emp.department
            employee["salary"]=emp.salary
            return {
                "message":"Employee fully update","data":employee
            }
    raise HTTPException(status_code=404,detail="Employee not found")

#PATCH (PARTIAL UPDATE)
@app.patch("/employees/{emp_id}")
def update_partial_employee(emp_id:int,emp:Update_Employee):
    for employee in employees:
        if employee["id"]==emp_id:
            if emp.name is not None:
                employee["name"]=emp.name
            if emp.department is not None:
                employee["department"]=emp.department
            if emp.salary is not None:
                employee["salary"]=emp.salary

            return {
                "message":"Employee partially update","data":employee
            }
    raise HTTPException(status_code=404,detail="Employee not found")

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id:int):
    for index,employee in enumerate(employees):
        if employee["id"]==emp_id:
            deleted_employee=employees.pop(index)
            return {"message":"Employee delated","data":deleted_employee}
    raise HTTPException(status_code=404,detail="Employee not found")

