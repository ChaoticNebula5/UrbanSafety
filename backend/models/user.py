from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    phone: str = Field(..., description="Phone number with country code")
    email: Optional[str] = Field(None, description="Optional email address")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Rajesh Kumar",
                "phone": "+919876543210",
                "email": "rajesh@example.com"
            }
        }
    }
