"""
CRUD API Router Module

This module provides the main CRUD router that handles all CRUD operations
for different entities in the system.
"""

from fastapi import APIRouter
from .user import user_router
from .university import university_router
from .scholarship import scholarship_router
# from .plan import plan_router

# Create the main CRUD router
crud_router = APIRouter(tags=["CRUD Operations"])

# Include sub-routers
crud_router.include_router(user_router, tags=["CRUD User"])
crud_router.include_router(university_router, tags=["CRUD University"])
crud_router.include_router(scholarship_router, tags=["CRUD Scholarship"])
# crud_router.include_router(plan_router, tags=["Plan CRUD"])

__all__ = ["crud_router"]
