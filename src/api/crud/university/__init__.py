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
from .uniScholarship import scholarship_router

university_router = APIRouter()

# Include all university sub-routers
university_router.include_router(universities_router, tags=["Universities CRUD"])
university_router.include_router(uni_faculty_router, tags=["University Faculties CRUD"])
university_router.include_router(uni_department_router, tags=["University Departments CRUD"])
university_router.include_router(campus_router, prefix="/campus", tags=["Campus CRUD"])
university_router.include_router(program_router, prefix="/programs", tags=["Program CRUD"])
university_router.include_router(people_router, prefix="/people", tags=["People CRUD"])
university_router.include_router(research_router, prefix="/research", tags=["Research CRUD"])
university_router.include_router(scholarship_router, prefix="/scholarships", tags=["Scholarship CRUD"])

__all__ = ["university_router"]
