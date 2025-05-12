from fastapi import APIRouter, HTTPException, Depends
from app.services.utils import check_access_and_limit
from app.routes.auth import get_current_user  # ✅ Import JWT guard
from app.db import db

router = APIRouter()

async def track_usage(user_id: str, api_name: str):
    sub = await db.subscriptions.find_one({"user_id": user_id})
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    usage = sub.get("usage", {})
    usage[api_name] = usage.get(api_name, 0) + 1

    await db.subscriptions.update_one(
        {"user_id": user_id},
        {"$set": {"usage": usage}}
    )

    return usage[api_name]

# Register 6 dummy APIs with access control + JWT + usage tracking
for i in range(1, 7):
    api_name = f"api{i}"

    async def generic_endpoint(user_id: str, api=api_name, user=Depends(get_current_user)):
        await check_access_and_limit(user_id, api)
        used = await track_usage(user_id, api)
        return {
            "message": f"Accessed {api}",
            "usage_count": used
        }

    router.add_api_route(
        path=f"/cloud/{api_name}/{{user_id}}",
        endpoint=generic_endpoint,
        methods=["GET"],
        name=f"Access {api_name}"
    )
