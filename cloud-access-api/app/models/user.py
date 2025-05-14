from pydantic import BaseModel, Field
from typing import Dict

class SubscriptionCreate(BaseModel):
    user_id: str = Field(..., example="user123")
    plan_id: str = Field(..., example="plan123")

class SubscriptionResponse(SubscriptionCreate):
    id: str
    usage: Dict[str, int] = Field(default_factory=dict)
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # e.g., "user" or "admin"
