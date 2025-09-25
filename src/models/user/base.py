from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# User Role Constants
USER_ROLE_STUDENT = "student"
USER_ROLE_ADVISOR = "advisor"
USER_ROLE_PARENT = "parent"
USER_ROLE_ADMIN = "admin"

# User Status Constants
USER_STATUS_ACTIVE = "active"
USER_STATUS_INACTIVE = "inactive"
USER_STATUS_SUSPENDED = "suspended"
USER_STATUS_VERIFYING = "verifying"

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
    role: str = USER_ROLE_STUDENT
    status: str = USER_STATUS_VERIFYING
    
    # Profile Information
    profile_picture_url: Optional[str] = Field(None, max_length=500)
    timezone: Optional[str] = Field(None, max_length=50)
    language_preference: Optional[str] = Field("en", max_length=10)

# User Session Schemas
class UserSessionBase(BaseModel):
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    device_info: Optional[str] = Field(None, max_length=200)
