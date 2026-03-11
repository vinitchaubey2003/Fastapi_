from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Session
from database import Base, engine, get_db

app = FastAPI()

# -----------------------
# MODELS
# -----------------------

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    staff_members = relationship("Staff", back_populates="department")


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    salary = Column(Integer)

    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="staff_members")


# create tables
Base.metadata.create_all(bind=engine)


# -----------------------
# CREATE DEPARTMENT
# -----------------------

@app.post("/departments")
def create_department(dep: dict, db: Session = Depends(get_db)):

    department = Department(
        name=dep["name"]
    )

    db.add(department)
    db.commit()

    return {"message": "Department created"}


# -----------------------
# CREATE STAFF
# -----------------------

@app.post("/staff")
def create_staff(staff: dict, db: Session = Depends(get_db)):

    new_staff = Staff(
        name=staff["name"],
        salary=staff["salary"],
        department_id=staff["department_id"]
    )

    db.add(new_staff)
    db.commit()

    return {"message": "Staff created"}


# -----------------------
# GET ALL DEPARTMENTS
# -----------------------

@app.get("/departments")
def get_departments(db: Session = Depends(get_db)):

    departments = db.query(Department).all()

    result = []

    for dep in departments:

        result.append({
            "department": dep.name,
            "staff": [s.name for s in dep.staff_members]
        })

    return result


# -----------------------
# SEARCH STAFF
# -----------------------

@app.get("/staff/search")
def search_staff(name: str, db: Session = Depends(get_db)):

    staff = db.query(Staff).filter(Staff.name == name).all()

    return staff


# -----------------------
# STAFF BY DEPARTMENT
# -----------------------

@app.get("/staff/department/{dep_id}")
def get_staff_by_department(dep_id: int, db: Session = Depends(get_db)):

    staff = db.query(Staff).filter(Staff.department_id == dep_id).all()

    return staff


# -----------------------
# UPDATE STAFF
# -----------------------

@app.put("/staff/{staff_id}")
def update_staff(staff_id: int, data: dict, db: Session = Depends(get_db)):

    staff = db.query(Staff).filter(Staff.id == staff_id).first()

    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    staff.name = data["name"]
    staff.salary = data["salary"]
    staff.department_id = data["department_id"]

    db.commit()

    return {"message": "Staff updated"}


# -----------------------
# DELETE STAFF
# -----------------------

@app.delete("/staff/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):

    staff = db.query(Staff).filter(Staff.id == staff_id).first()

    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    db.delete(staff)
    db.commit()

    return {"message": "Staff deleted"}