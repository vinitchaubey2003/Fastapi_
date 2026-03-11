from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    name: str
    department: str
    salary: int

employees = {}

# POST → Create
@app.post("/employees/{emp_id}")
def create_employee(emp_id: int, emp: Employee):
    employees[emp_id] = emp
    return {
        "message": "Employee created"
    }

# PUT → Update
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp: Employee):
    if emp_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")

    employees[emp_id] = emp
    return {
        "message": "Employee updated"
    }