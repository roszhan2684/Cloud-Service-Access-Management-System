from pydantic import BaseModel, Field
from typing import List, Optional

class PlanCreate(BaseModel):
    name: str = Field(..., example="Pro Plan")
    description: Optional[str] = Field(None, example="Provides access to all core APIs")
    permissions: List[str] = Field(..., example=["api1", "api2"])
    usage_limits: dict = Field(..., example={"api1": 1000, "api2": 500})

class PlanResponse(PlanCreate):
    id: str
