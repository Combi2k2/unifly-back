"""
University CRUD API Package

This package contains all university-related CRUD API routers organized by domain.
"""

from fastapi import APIRouter
from .universities import universities_router
from .uniFaculty import uni_faculty_router
from .uniDepartment import uni_department_router
from .uniCampus import campus_router
from .uniProgram import program_router
from .uniPeople import people_router
from .uniResearch import research_router

university_router = APIRouter()

# Include all university sub-routers
university_router.include_router(universities_router, prefix="/universities", tags=["CRUD Universities"])
university_router.include_router(uni_faculty_router, prefix="/university-faculties", tags=["CRUD University-Faculty"])
university_router.include_router(uni_department_router, prefix="/university-departments", tags=["CRUD University-Department"])
university_router.include_router(campus_router, prefix="/university-campuses", tags=["CRUD University-Campus"])
university_router.include_router(program_router, prefix="/university-programs", tags=["CRUD University-Program"])
university_router.include_router(people_router, prefix="/university-people", tags=["CRUD University-Person"])
university_router.include_router(research_router, prefix="/university-research", tags=["CRUD University-Research"])

__all__ = ["university_router"]
