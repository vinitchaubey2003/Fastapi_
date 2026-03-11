from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DATABASE_NAME")]
collection = db["users"]

# Helper function
def user_helper(user):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"]
    }

# Model
class User(BaseModel):
    name: str
    email: EmailStr
    age: int

# CREATE
@app.post("/users")
async def create_user(user: User):
    new_user = await collection.insert_one(user.dict())
    created_user = await collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return user_helper(created_user)

# GET ALL
@app.get("/users")
async def get_users():
    users = []
    async for user in collection.find():
        users.append(user_helper(user))
    return users

# GET ONE
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await collection.find_one(
        {"_id": ObjectId(user_id)}
    )
    if user:
        return user_helper(user)
    raise HTTPException(status_code=404, detail="User not found")

# UPDATE
@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict()}
    )
    if result.modified_count == 1:
        updated_user = await collection.find_one(
            {"_id": ObjectId(user_id)}
        )
        return user_helper(updated_user)
    raise HTTPException(status_code=404, detail="User not updated")

# DELETE
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    result = await collection.delete_one(
        {"_id": ObjectId(user_id)}
    )
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")