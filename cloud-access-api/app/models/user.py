from pydantic import BaseModel, Field
from typing import Dict

class SubscriptionCreate(BaseModel):
    user_id: str = Field(..., example="user123")
    plan_id: str = Field(..., example="plan123")

class SubscriptionResponse(SubscriptionCreate):
    id: str
    usage: Dict[str, int] = Field(default_factory=dict)
