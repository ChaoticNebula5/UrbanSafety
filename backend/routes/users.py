from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from passlib.context import CryptContext
from services.db_service import db_service

router = APIRouter(prefix="/api/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EmergencyContact(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15)


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6, max_length=100)
    email: Optional[str] = None
    emergency_contacts: List[EmergencyContact] = Field(default_factory=list)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Rajesh Kumar",
                "phone": "9876543210",
                "password": "securepass123",
                "email": "rajesh@example.com",
                "emergency_contacts": [
                    {"name": "Mom", "phone": "9876000001"},
                    {"name": "Dad", "phone": "9876000002"}
                ]
            }
        }
    }


class UserLogin(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15)
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    emergency_contacts: List[Dict[str, str]]


@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user_data: UserRegister):
    try:
        existing = await db_service.get_user_by_phone(user_data.phone)
        if existing:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        
        password_hash = pwd_context.hash(user_data.password)
        
        emergency_contacts_dict = [c.dict() for c in user_data.emergency_contacts]
        
        user = await db_service.create_user(
            name=user_data.name,
            phone=user_data.phone,
            password_hash=password_hash,
            email=user_data.email,
            emergency_contacts=emergency_contacts_dict
        )
        
        return UserResponse(
            id=user.id,
            name=user.name,
            phone=user.phone,
            email=user.email,
            emergency_contacts=user.emergency_contacts or []
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=UserResponse)
async def login_user(credentials: UserLogin):
    try:
        user = await db_service.get_user_by_phone(credentials.phone)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid phone number or password")
        
        if not pwd_context.verify(credentials.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid phone number or password")
        
        return UserResponse(
            id=user.id,
            name=user.name,
            phone=user.phone,
            email=user.email,
            emergency_contacts=user.emergency_contacts or []
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user profile by ID"""
    user = await db_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        name=user.name,
        phone=user.phone,
        email=user.email,
        emergency_contacts=user.emergency_contacts or []
    )
