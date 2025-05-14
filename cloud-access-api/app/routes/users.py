from fastapi import APIRouter, HTTPException, Depends, Request
from bson import ObjectId
from typing import Optional
from app.db import db
from app.models.user import UserCreate
from app.routes.auth import get_current_user

router = APIRouter()

def serialize_user(user):
    user["id"] = str(user["_id"])
    del user["_id"]
    del user["password"]
    return user

# ✅ Create user (open to public, admin check for role='admin')
@router.post("/", status_code=201)
async def create_user(
    new_user: UserCreate,
    request: Request,
    current_user: Optional[dict] = Depends(get_current_user)
):
    exists = await db.users.find_one({"username": new_user.username})
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    if new_user.role == "admin":
        if not current_user or current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Only admins can create admin users")

    result = await db.users.insert_one(new_user.dict())
    return {"id": str(result.inserted_id), "message": "User created successfully"}

# 🔐 Admin-only: Delete a user
@router.delete("/{username}", status_code=200)
async def delete_user(username: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete users")

    result = await db.users.delete_one({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": f"User '{username}' deleted successfully"}
@router.get("/", status_code=200)
async def get_all_users(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can view all users")

    users = []
    async for user in db.users.find():
        users.append(serialize_user(user))
    return users
