from pydantic import BaseModel, Field

class PermissionCreate(BaseModel):
    name: str = Field(..., example="api1")
    endpoint: str = Field(..., example="/api1")
    description: str = Field(..., example="First example cloud service")

class PermissionResponse(PermissionCreate):
    id: str
