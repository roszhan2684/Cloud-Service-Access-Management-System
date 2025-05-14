from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.models.plan import PlanCreate
from app.db import db
from app.routes.auth import get_current_user

router = APIRouter()

# Helper to serialize MongoDB documents
def serialize_plan(plan):
    plan["id"] = str(plan["_id"])
    del plan["_id"]
    return plan

# Admin-only dependency
def admin_only(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")

@router.post("/", status_code=201, dependencies=[Depends(admin_only)])
async def create_plan(plan: PlanCreate):
    existing = await db.plans.find_one({"name": plan.name})
    if existing:
        raise HTTPException(status_code=400, detail="Plan with this name already exists.")
    result = await db.plans.insert_one(plan.dict())
    return {"id": str(result.inserted_id), "message": "Plan created successfully"}

@router.get("/", status_code=200)
async def get_all_plans():
    plans = []
    async for plan in db.plans.find():
        plans.append(serialize_plan(plan))
    return plans

@router.get("/{plan_id}", status_code=200)
async def get_plan(plan_id: str):
    try:
        plan = await db.plans.find_one({"_id": ObjectId(plan_id)})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return serialize_plan(plan)
    except:
        raise HTTPException(status_code=400, detail="Invalid plan ID format")

@router.put("/{plan_id}", status_code=200, dependencies=[Depends(admin_only)])
async def update_plan(plan_id: str, updated_plan: PlanCreate):
    result = await db.plans.update_one(
        {"_id": ObjectId(plan_id)},
        {"$set": updated_plan.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found or no change detected")
    return {"message": "Plan updated successfully"}

@router.delete("/{plan_id}", status_code=200, dependencies=[Depends(admin_only)])
async def delete_plan(plan_id: str):
    result = await db.plans.delete_one({"_id": ObjectId(plan_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan deleted successfully"}
