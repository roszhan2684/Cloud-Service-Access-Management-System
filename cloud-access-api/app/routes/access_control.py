from fastapi import APIRouter
from app.services.utils import (
    get_user_subscription,
    get_plan_by_id,
    check_api_permission,
    check_usage_limit
)

router = APIRouter()

@router.get("/{user_id}/{api_name}")
async def check_api_access(user_id: str, api_name: str):
    subscription = await get_user_subscription(user_id)
    plan = await get_plan_by_id(subscription["plan_id"])
    check_api_permission(plan, api_name)
    check_usage_limit(subscription, plan, api_name)
    return {"access": True, "message": "Access granted"}
