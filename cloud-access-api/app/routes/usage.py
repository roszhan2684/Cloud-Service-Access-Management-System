from fastapi import APIRouter, HTTPException, Body
from app.db import db
from bson import ObjectId

router = APIRouter()

@router.post("/{user_id}", summary="Track usage of an API for a user")
async def track_usage(user_id: str, api_name: str = Body(...)):
    sub = await db.subscriptions.find_one({"user_id": user_id})
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    plan = await db.plans.find_one({"_id": ObjectId(sub["plan_id"])})
    if not plan or api_name not in plan["permissions"]:
        raise HTTPException(status_code=403, detail="API not permitted in this plan")

    usage = sub.get("usage", {})
    usage[api_name] = usage.get(api_name, 0) + 1

    await db.subscriptions.update_one(
        {"user_id": user_id},
        {"$set": {"usage": usage}}
    )

    return {"message": f"API call to {api_name} recorded", "total_used": usage[api_name]}

@router.get("/{user_id}/limit", summary="Check current usage limits")
async def check_limit(user_id: str):
    sub = await db.subscriptions.find_one({"user_id": user_id})
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    plan = await db.plans.find_one({"_id": ObjectId(sub["plan_id"])})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    usage = sub.get("usage", {})
    limits = plan.get("usage_limits", {})

    overused = [api for api, limit in limits.items() if usage.get(api, 0) >= limit]

    return {
        "usage": usage,
        "limits": limits,
        "blocked": overused
    }
