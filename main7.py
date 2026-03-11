from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import Column,String,Integer, column
from sqlalchemy.orm import Session
from database import engine,Base,get_db

app=FastAPI()

class Employee(Base):
    __tablename__="employees"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    department=Column(String)
    salary=Column(Integer)

Base.metadata.create_all(bind=engine)

#CREATE
@app.post("/employees")

def create_employee(emp:dict,db:Session=Depends(get_db)):

    employee=Employee(
        id=emp["id"],
        name=emp["name"],
        department=emp["department"],
        salary=emp["salary"]

    )
    db.add(employee)
    db.commit()

    return {"message":"Employee created"}

#Read

@app.get("/employees")
def get_employees(db:Session=Depends(get_db)):

    employees=db.query(Employee).all()
    return employees

#Update

@app.put("/employees/{emp_id}")
def update_employee(emp_id:int,emp:dict,db:Session=Depends(get_db)):
    employee=db.query(Employee).filter(Employee.id==emp_id).first()

    if not employee:
        raise HTTPException(status_code=404,detail="Employee_not found")
    
    employee.name=emp["name"]
    employee.department=emp["department"]
    employee.salary=emp["salary"]

    db.commit()

    return {"message":"Employee updated"}

#Delete

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id:int,db:Session=Depends(get_db)):

    employee=db.query(Employee).filter(Employee.id==emp_id).first()

    if not employee:
        raise HTTPException(status_code=404,detail="Employee not found")
    
    db.delete(employee)
    db.commit()

    return {"message":"Employee deleted"}