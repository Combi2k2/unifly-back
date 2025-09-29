"""
Scholarship CRUD API Package

This package contains all scholarship-related CRUD API routers organized by domain.
"""

from fastapi import APIRouter
from .hobo import hobo_router
from .hoboProviders import providers_router

scholarship_router = APIRouter()

# Include all scholarship sub-routers
scholarship_router.include_router(hobo_router, prefix="/scholarships", tags=["CRUD Scholarship-Detail"])
scholarship_router.include_router(providers_router, prefix="/scholarship-providers", tags=["CRUD Scholarship-Provider"])

__all__ = ["scholarship_router"]
