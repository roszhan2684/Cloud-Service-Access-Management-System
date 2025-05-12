from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.db import db
from app.models.permission import PermissionCreate

router = APIRouter()

def serialize_permission(permission):
    permission["id"] = str(permission["_id"])
    del permission["_id"]
    return permission

@router.post("/", status_code=201)
async def create_permission(permission: PermissionCreate):
    exists = await db.permissions.find_one({"name": permission.name})
    if exists:
        raise HTTPException(status_code=400, detail="Permission with this name already exists.")
    result = await db.permissions.insert_one(permission.dict())
    return {"id": str(result.inserted_id), "message": "Permission created successfully"}

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

@router.put("/{permission_id}", status_code=200)
async def update_permission(permission_id: str, updated: PermissionCreate):
    result = await db.permissions.update_one(
        {"_id": ObjectId(permission_id)},
        {"$set": updated.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found or no changes made.")
    return {"message": "Permission updated successfully"}

@router.delete("/{permission_id}", status_code=200)
async def delete_permission(permission_id: str):
    result = await db.permissions.delete_one({"_id": ObjectId(permission_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": "Permission deleted successfully"}
