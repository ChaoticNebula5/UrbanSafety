from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class IncidentCategory(str, Enum):
    THEFT = "theft"
    ASSAULT = "assault"
    VANDALISM = "vandalism"
    TRAFFIC = "traffic"
    SUSPICIOUS = "suspicious_activity"
    OTHER = "other"


class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentCreate(BaseModel):

    title: str = Field(..., min_length=5, max_length=200, description="Brief incident title")
    description: str = Field(..., min_length=10, max_length=2000, description="Detailed description")
    
    latitude: float = Field(..., ge=30.0, le=31.0, description="Latitude (30.xx for Patiala)")
    longitude: float = Field(..., ge=76.0, le=77.0, description="Longitude (76.xx for Patiala)")
    
    reporter_name: str = Field(..., min_length=2, max_length=100)
    reporter_phone: str = Field(..., min_length=10, max_length=15)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Street lighting broken near Model Town",
                "description": "The street lights have been non-functional for 3 days, making the area unsafe at night.",
                "latitude": 30.3398,
                "longitude": 76.3869,
                "reporter_name": "Priya Sharma",
                "reporter_phone": "+919876543210"
            }
        }
    }


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    latitude: float
    longitude: float
    
    category: Optional[IncidentCategory] = None
    severity: Optional[IncidentSeverity] = None
    ai_summary: Optional[str] = None
    
    reporter_name: str
    reporter_phone: str
    
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True, 
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Street lighting broken near Model Town",
                "description": "The street lights have been non-functional for 3 days...",
                "latitude": 30.3398,
                "longitude": 76.3869,
                "category": "other",
                "severity": "medium",
                "ai_summary": "Infrastructure issue: Non-functional street lighting affecting public safety.",
                "reporter_name": "Priya Sharma",
                "reporter_phone": "+919876543210",
                "created_at": "2025-10-13T10:30:00Z",
                "updated_at": "2025-10-13T10:30:00Z"
            }
        }
    }


class IncidentListResponse(BaseModel):
    total: int
    incidents: list[IncidentResponse]
    page: int = 1
    page_size: int = 20
