from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse
import os

app=FastAPI()

file_path="sample.pdf"

#GET method

@app.get("/download")
def download_file():
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,detail="file not found")
    
    return FileResponse(file_path,media_type="application/pdf")

#HEAD METHOD

@app.head("/download")
def check_file():
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,detail="File not found")
    
    file_size=os.path.getsize(file_path)

    return {
        "file_size":file_size
    }