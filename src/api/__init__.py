"""
API Module

This module provides the main API router that includes all sub-routers
for different API endpoints.
"""

from fastapi import APIRouter
from .crud import crud_router

# Create the main API router
api_router = APIRouter(tags=["API"])

# Include sub-routers
api_router.include_router(crud_router)

__all__ = ["api_router"]
