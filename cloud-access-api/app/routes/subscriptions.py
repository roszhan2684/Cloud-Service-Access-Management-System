from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.db import db
from app.models.user import SubscriptionCreate
from app.routes.auth import get_current_user  # ⬅️ Import dependency
from datetime import datetime

router = APIRouter()

def serialize_subscription(sub):
    sub["id"] = str(sub["_id"])
    del sub["_id"]
    return sub

@router.post("/", status_code=201)
async def subscribe_user(data: SubscriptionCreate, user=Depends(get_current_user)):
    existing = await db.subscriptions.find_one({"user_id": data.user_id})
    if existing:
        raise HTTPException(status_code=400, detail="User already subscribed.")
    plan = await db.plans.find_one({"_id": ObjectId(data.plan_id)})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    usage = {api: 0 for api in plan["permissions"]}
    record = {
        "user_id": data.user_id,
        "plan_id": data.plan_id,
        "usage": usage,
        "created_at": datetime.utcnow()
    }
    result = await db.subscriptions.insert_one(record)
    return {"id": str(result.inserted_id), "message": "User subscribed successfully"}

@router.get("/{user_id}", status_code=200)
async def get_user_subscription(user_id: str, user=Depends(get_current_user)):
    sub = await db.subscriptions.find_one({"user_id": user_id})
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return serialize_subscription(sub)

@router.get("/{user_id}/usage", status_code=200)
async def get_usage_stats(user_id: str, user=Depends(get_current_user)):
    sub = await db.subscriptions.find_one({"user_id": user_id})
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub.get("usage", {})

@router.put("/{user_id}", status_code=200)
async def change_user_plan(user_id: str, data: SubscriptionCreate, user=Depends(get_current_user)):
    plan = await db.plans.find_one({"_id": ObjectId(data.plan_id)})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    usage = {api: 0 for api in plan["permissions"]}
    result = await db.subscriptions.update_one(
        {"user_id": user_id},
        {"$set": {"plan_id": data.plan_id, "usage": usage}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or no change made.")
    return {"message": "User plan updated successfully"}
