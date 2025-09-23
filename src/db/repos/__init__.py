"""
Database Repository Package
Contains repository classes for different data stores
"""

from .user import UserRepository
from .student import StudentRepository
from .university import UniversityRepository

__all__ = [
    'UserRepository',
    'StudentRepository',
    'UniversityRepository'
]