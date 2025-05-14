from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.db import db
from app.models.permission import PermissionCreate
from typing import List
from app.routes.auth import get_current_user

router = APIRouter()

# Helper to serialize MongoDB documents
def serialize_permission(permission):
    permission["id"] = str(permission["_id"])
    del permission["_id"]
    return permission

# Admin-only dependency
def admin_only(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")

@router.post("/", status_code=201, dependencies=[Depends(admin_only)])
async def create_permissions(permissions: List[PermissionCreate]):
    created = []
    for perm in permissions:
        exists = await db.permissions.find_one({"name": perm.name})
        if exists:
            continue  # Skip existing permission names silently
        result = await db.permissions.insert_one(perm.dict())
        created.append(str(result.inserted_id))
    
    if not created:
        raise HTTPException(status_code=400, detail="No new permissions were created. All names already exist.")
    
    return {
        "message": f"{len(created)} permissions created successfully",
        "ids": created
    }

@router.get("/", status_code=200)
async def get_all_permissions():
    permissions = []
    async for permission in db.permissions.find():
        permissions.append(serialize_permission(permission))
    return permissions

@router.get("/{permission_id}", status_code=200)
async def get_permission(permission_id: str):
    try:
        permission = await db.permissions.find_one({"_id": ObjectId(permission_id)})
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        return serialize_permission(permission)
    except:
        raise HTTPException(status_code=400, detail="Invalid permission ID format")

@router.put("/{permission_id}", status_code=200, dependencies=[Depends(admin_only)])
async def update_permission(permission_id: str, updated: PermissionCreate):
    result = await db.permissions.update_one(
        {"_id": ObjectId(permission_id)},
        {"$set": updated.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found or no changes made.")
    return {"message": "Permission updated successfully"}

@router.delete("/{permission_id}", status_code=200, dependencies=[Depends(admin_only)])
async def delete_permission(permission_id: str):
    result = await db.permissions.delete_one({"_id": ObjectId(permission_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": "Permission deleted successfully"}
