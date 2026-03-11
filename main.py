from fastapi import FastAPI,HTTPException
from typing import Optional
from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import List

app=FastAPI()

@app.get("/")
def root():
    return {"message":"Welcome to mapvinit"}

@app.get("/users")
def get_users():
    return[
        {"id":1,"name":"vinit"},
        {"id":2,"name":"Rahul"}
    ]

employees=[
         {"id":1,"name":"vinit","department":"IT","salary":40000 },
         {"id": 2, "name": "Rahul", "department": "HR", "salary": 25000},
    {"id": 3, "name": "Aman", "department": "IT", "salary": 35000},
    {"id": 4, "name": "Neha", "department": "Sales", "salary": 30000},
    {"id": 5, "name": "Priya", "department": "IT", "salary": 50000},
]
 
@app.get("/employees")
def get_employees(
    page:int=1,
    limit:int=5,
    department:Optional[str]=None,
    min_salary:Optional[int]=None,
):
    
    data=employees

    #department filter
    if department:
        data=[emp for emp in data if emp["department"]==department]
    #min_ salry filter
    if min_salary:
        data=[emp for emp in data if emp["salary"]>=min_salary]

    #pagination logic
    start=(page-1)*limit
    end=start+limit

    return data[start:end]

class Employee(BaseModel):
    name:str
    department:str
    salary:int

employees=[]

#POST METHOD
@app.post("/employees")
def create_employee(emp:Employee):
    employees.append(emp)
    return {"message":"Employee added suceesfully","data":emp}


class EmployeeCreate(BaseModel):
    name:str=Field(...,min_length=3)
    email:EmailStr
    department:str
    salary:int=Field(..., gt=0)

class EmployeeResponse(BaseModel):
    id:int
    name:str
    department:str
    salary:int
    create_at:datetime

employees:List[dict]=[]
current_id=1

@app.post("/employees",response_model=EmployeeResponse)
def create_employee(emp:EmployeeCreate):
    global current_id


    for existing in employees:
        if existing["email"]==emp.email:
            raise HTTPException(status_code=400,deatil="emial already exist")
        
        new_employee={
            "id":current_id,
            "name":emp.name,
            "department":emp.department,
            "salary":emp.salary,
            "created_at":datetime.utcnow()
    
        }


        employees.append(new_employee)
        current_id+=1

        return new_employee
    
#HEAD METHOD ->sirf header data deta hi body ka data nhi deta

@app.get("/vinit")
def get_employees():
    return {"message":"Employeelist"}
    
