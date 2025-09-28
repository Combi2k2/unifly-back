"""
User CRUD API Router Module

This module provides the main user CRUD router that includes all user-related sub-routers.
"""

from fastapi import APIRouter
from .base import user_base_router
from .usrStudent import student_router
from .usrAdmin import admin_router
from .usrAdvisor import advisor_router
from .usrParent import parent_router

# Create the main user router
user_router = APIRouter()

# Include sub-routers
user_router.include_router(user_base_router, tags=["User Base CRUD"])
user_router.include_router(student_router, tags=["Student CRUD"])
user_router.include_router(admin_router, tags=["Admin CRUD"])
user_router.include_router(advisor_router, tags=["Advisor CRUD"])
user_router.include_router(parent_router, tags=["Parent CRUD"])

__all__ = ["user_router"]

