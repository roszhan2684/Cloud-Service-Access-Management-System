from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.services.jwt_handler import create_access_token, decode_access_token
from app.models.user import LoginRequest
from app.db import db  # Import your MongoDB client

router = APIRouter()
token_auth_scheme = HTTPBearer(auto_error=False)

# Static admin (optional, can be removed if full DB-backed)
static_admin = {
    "username": "roszhan",
    "password": "secret123",
    "role": "admin"
}

# Token generation
@router.post("/token")
async def login(form_data: LoginRequest):
    # Check if user is 'roszhan' (static admin)
    if form_data.username == static_admin["username"] and form_data.password == static_admin["password"]:
        access_token = create_access_token(data={
            "sub": static_admin["username"],
            "role": static_admin["role"]
        })
        return {"access_token": access_token, "token_type": "bearer"}

    # Else check from DB
    user = await db.users.find_one({"username": form_data.username})
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={
        "sub": user["username"],
        "role": user["role"]
    })

    return {"access_token": access_token, "token_type": "bearer"}

# Auth dependency
async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(token_auth_scheme)):
    if not credentials:
        return None

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload  # returns dict: {sub: ..., role: ...}
