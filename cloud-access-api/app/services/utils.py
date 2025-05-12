from bson import ObjectId
from fastapi import HTTPException
from app.db import db

def serialize_mongo_document(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

async def get_user_subscription(user_id: str):
    subscription = await db.subscriptions.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="User subscription not found.")
    return subscription

async def get_plan_by_id(plan_id: str):
    try:
        plan = await db.plans.find_one({"_id": ObjectId(plan_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid plan ID.")
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return plan

def check_api_permission(plan: dict, api_name: str):
    if api_name not in plan.get("permissions", []):
        raise HTTPException(status_code=403, detail="API not allowed in this plan.")

def check_usage_limit(subscription: dict, plan: dict, api_name: str):
    usage_count = subscription.get("usage", {}).get(api_name, 0)
    limit = plan.get("usage_limits", {}).get(api_name)
    if limit is None:
        raise HTTPException(status_code=403, detail="No limit defined for this API.")
    if usage_count >= limit:
        raise HTTPException(status_code=429, detail=f"Usage limit reached: {usage_count}/{limit}")
async def check_access_and_limit(user_id: str, api_name: str):
    subscription = await get_user_subscription(user_id)
    plan = await get_plan_by_id(subscription["plan_id"])
    check_api_permission(plan, api_name)
    check_usage_limit(subscription, plan, api_name)
