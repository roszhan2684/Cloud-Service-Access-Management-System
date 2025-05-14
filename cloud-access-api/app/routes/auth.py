# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from app.services.jwt_handler import create_access_token, decode_access_token
# from app.models.user import LoginRequest  # Import your login model

# router = APIRouter()
# token_auth_scheme = HTTPBearer()

# # Temporary fake user DB
# fake_users = {
#     "roszhan": {
#         "username": "roszhan",
#         "password": "secret123",
#         "role": "admin"
#     },
#     "john": {
#         "username": "john",
#         "password": "user123",
#         "role": "user"
#     }
# }


# @router.post("/token")
# async def login(form_data: LoginRequest):
#     user = fake_users.get(form_data.username)

#     if not user or user["password"] != form_data.password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     # Include role in the token
#     access_token = create_access_token(data={
#         "sub": user["username"],
#         "role": user["role"]
#     })

#     return {"access_token": access_token, "token_type": "bearer"}

# # Dependency to use in protected routes
# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
#     token = credentials.credentials
#     payload = decode_access_token(token)
#     if payload is None:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
#     return payload  # returns full dict with sub and role
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from typing import Optional

# token_auth_scheme = HTTPBearer(auto_error=False)  # ← Make it optional

# async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(token_auth_scheme)):
#     if not credentials:
#         return None  # No token = not logged in

#     token = credentials.credentials
#     payload = decode_access_token(token)
#     if payload is None:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
#     return payload
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.services.jwt_handler import create_access_token, decode_access_token
from app.models.user import LoginRequest

router = APIRouter()

# Auth scheme for token-based access
token_auth_scheme = HTTPBearer(auto_error=False)

# ✅ Only one admin: roszhan
fake_users = {
    "roszhan": {
        "username": "roszhan",
        "password": "secret123",
        "role": "admin"
    }
}

# ✅ Login route to generate token
@router.post("/token")
async def login(form_data: LoginRequest):
    user = fake_users.get(form_data.username)

    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={
        "sub": user["username"],
        "role": user["role"]
    })

    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Auth dependency (optional)
async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(token_auth_scheme)):
    if not credentials:
        return None  # Not logged in

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload  # Includes 'sub' and 'role'
