from fastapi import FastAPI
from app.routes import (
    plans,
    permissions,
    subscriptions,
    access_control,
    usage,
    auth,
    cloud_apis
)

app = FastAPI(title="Roszhan-Jenny-Sufiyan's_Cloud Service Access Management System")

# Plan Management APIs
app.include_router(plans.router, prefix="/plans", tags=["Plans"])

# Permission Management APIs
app.include_router(permissions.router, prefix="/permissions", tags=["Permissions"])

# User Subscription APIs (JWT Protected)
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])

# Access Control APIs (JWT Protected)
app.include_router(access_control.router, prefix="/access", tags=["Access Control"])

# Usage Tracking APIs (JWT Protected)
app.include_router(usage.router, prefix="/usage", tags=["Usage Tracking"])

# Auth APIs (Login / Token Generation)
app.include_router(auth.router, tags=["Authentication"])

# Dummy Cloud APIs (JWT + Access Control + Usage Tracking)
app.include_router(cloud_apis.router, tags=["Cloud Services"])

# ========== Default Route ==========
@app.get("/")
async def root():
    return {"message": "Roszhan-Jenny-Sufiyan's Cloud Service Access Management System"}
from app.routes import users
app.include_router(users.router, prefix="/users", tags=["Users"])
