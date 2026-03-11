from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI()

data = [
    {"id": 1, "name": "Vinit", "role": "Developer"},
    {"id": 2, "name": "Rahul", "role": "Tester"}
]

@app.get("/employees")
def get_employees(request: Request):

    accept = request.headers.get("accept")

    # JSON
    if "application/json" in accept:
        return JSONResponse(content=data)

    # XML
    elif "application/xml" in accept:
        xml_data = "<employees>"
        for emp in data:
            xml_data += f"<employee><id>{emp['id']}</id><name>{emp['name']}</name><role>{emp['role']}</role></employee>"
        xml_data += "</employees>"
        return Response(content=xml_data, media_type="application/xml")

    # CSV
    elif "text/csv" in accept:
        csv_data = "id,name,role\n"
        for emp in data:
            csv_data += f"{emp['id']},{emp['name']},{emp['role']}\n"
        return Response(content=csv_data, media_type="text/csv")

    return JSONResponse(content=data)