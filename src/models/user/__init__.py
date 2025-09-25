# System-level user models
from .base import (
    # User role constants
    USER_ROLE_STUDENT,
    USER_ROLE_ADVISOR,
    USER_ROLE_PARENT,
    USER_ROLE_ADMIN,
    
    # User status constants
    USER_STATUS_ACTIVE,
    USER_STATUS_INACTIVE,
    USER_STATUS_SUSPENDED,
    USER_STATUS_VERIFYING,
    
    # User models
    UserBase,
    UserSessionBase
)

# Student-specific models
from .usrStudent import (
    Education,
    Experience,
    Award,
    ExtraCurricular,
    StandardizedTest,
    StudentProfile,
    StudentPreference
)

# Placeholder models for other user types
from .usrAdvisor import (
    AdvisorProfile,
    AdvisorPreference
)

from .usrParent import (
    ParentProfile,
    ParentPreference
)

from .usrAdmin import (
    AdminProfile,
    AdminPreference
)

__all__ = [
    # System-level models - constants
    "USER_ROLE_STUDENT",
    "USER_ROLE_ADVISOR", 
    "USER_ROLE_PARENT",
    "USER_ROLE_ADMIN",
    "USER_STATUS_ACTIVE",
    "USER_STATUS_INACTIVE",
    "USER_STATUS_SUSPENDED",
    "USER_STATUS_VERIFYING",
    
    # System-level models - classes
    "UserBase",
    "UserSessionBase",
    
    # Student models
    "Education",
    "Experience",
    "Award",
    "ExtraCurricular",
    "StandardizedTest",
    "StudentProfile",
    "StudentPreference",
    
    # Advisor models
    "AdvisorProfile",
    "AdvisorPreference",
    
    # Parent models
    "ParentProfile",
    "ParentPreference",
    
    # Admin models
    "AdminProfile",
    "AdminPreference"
]
