from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    ADVISOR = "advisor"
    PARENT = "parent"
    ADMIN = "admin"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

# User Schemas
class UserBase(BaseModel):
    # Basic Information
    userid: int = Field(description="Unique identifier for the user")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[datetime] = None
    nationality: Optional[str] = Field(None, max_length=100)
    
    # Authentication
    hashed_password: str
    
    # User Management
    role: UserRole = UserRole.STUDENT
    status: UserStatus = UserStatus.PENDING_VERIFICATION
    
    # Profile Information
    profile_picture_url: Optional[str] = Field(None, max_length=500)
    timezone: Optional[str] = Field(None, max_length=50)
    language_preference: Optional[str] = Field("en", max_length=10)

# User Session Schemas
class UserSessionBase(BaseModel):
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    device_info: Optional[str] = Field(None, max_length=200)