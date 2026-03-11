from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
database_url="mssql+pyodbc://@VINIT\\SQLEXPRESS/fastapi_db?driver=ODBC+Driver+17+for+SQL+Server"

engine=create_engine(database_url)

SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()