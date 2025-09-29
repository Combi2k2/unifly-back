"""
Student CRUD API Router

This module handles student-specific CRUD operations (StudentProfile, StudentPreference).
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging

# Import actual user models
from src.models.user import StudentProfile, StudentPreference

# Import MongoDB operations
from src.integrations.internal.mongodb import (
    get_mongodb_database,
    insert,
    get_one,
    get_many,
    update,
    delete,
    count
)
from src.config import MONGODB_STUDENT_PROFILES, MONGODB_STUDENT_PREFERENCES

# Configure logging
logger = logging.getLogger(__name__)

student_router = APIRouter()

# Helper functions
def get_student_profiles_collection():
    """Get the student profiles collection"""
    db = get_mongodb_database()
    return db[MONGODB_STUDENT_PROFILES]

def get_student_preferences_collection():
    """Get the student preferences collection"""
    db = get_mongodb_database()
    return db[MONGODB_STUDENT_PREFERENCES]

# Student profile endpoints
@student_router.post("/student-profiles/filter", response_model=List[StudentProfile])
async def get_student_profiles(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all student profiles with pagination and filtering"""
    try:
        collection = get_student_profiles_collection()
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [StudentProfile(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting student profiles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving student profiles: {str(e)}"
        )

@student_router.get("/student-profiles/{id}", response_model=StudentProfile)
async def get_student_profile(id: int):
    """Get a specific student profile by user ID"""
    try:
        collection = get_student_profiles_collection()
        result = get_one(collection, {"userid": id})
        result = StudentProfile(**result) if result else None
        return result
    except Exception as e:
        logger.error(f"Error getting student profile by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving student profile: {str(e)}"
        )

@student_router.post("/student-profiles")
async def create_student_profile(data: StudentProfile):
    """Create a new student profile"""
    try:
        collection = get_student_profiles_collection()
        result = insert(collection, data)
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating student profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating student profile: {str(e)}"
        )

@student_router.put("/student-profiles")
async def update_student_profiles(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple student profiles based on filters"""
    try:
        collection = get_student_profiles_collection()
        result = update(collection, filters, data)
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating student profiles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating student profiles: {str(e)}"
        )

@student_router.delete("/student-profiles")
async def delete_student_profiles(filters: Dict[str, Any]):
    """Delete multiple student profiles based on filters"""
    try:
        collection = get_student_profiles_collection()
        result = delete(collection, filters)
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting student profiles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting student profiles: {str(e)}"
        )

@student_router.post("/student-profiles/count")
async def count_student_profiles(filters: Dict[str, Any] = {}):
    """Count student profiles"""
    try:
        collection = get_student_profiles_collection()
        return count(collection, filters)
    except Exception as e:
        logger.error(f"Error counting student profiles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error counting student profiles: {str(e)}"
        )

# Student preference endpoints
@student_router.post("/student-preferences/filter", response_model=List[StudentPreference])
async def get_student_preferences(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all student preferences with pagination and filtering"""
    try:
        collection = get_student_preferences_collection()
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [StudentPreference(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting student preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving student preferences: {str(e)}"
        )

@student_router.get("/student-preferences/{id}", response_model=StudentPreference)
async def get_student_preference(id: int):
    """Get a specific student preference by user ID"""
    try:
        collection = get_student_preferences_collection()
        result = get_one(collection, {"userid": id})
        result = StudentPreference(**result) if result else None
        return result
    except Exception as e:
        logger.error(f"Error getting student preference by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving student preference: {str(e)}"
        )

@student_router.post("/student-preferences")
async def create_student_preference(data: StudentPreference):
    """Create a new student preference"""
    try:
        collection = get_student_preferences_collection()
        result = insert(collection, data)
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating student preference: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating student preference: {str(e)}"
        )

@student_router.put("/student-preferences")
async def update_student_preferences(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple student preferences based on filters"""
    try:
        collection = get_student_preferences_collection()
        result = update(collection, filters, data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating student preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating student preferences: {str(e)}"
        )

@student_router.delete("/student-preferences")
async def delete_student_preferences(filters: Dict[str, Any]):
    """Delete multiple student preferences based on filters"""
    try:
        collection = get_student_preferences_collection()
        result = delete(collection, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting student preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting student preferences: {str(e)}"
        )

@student_router.post("/student-preferences/count")
async def count_student_preferences(filters: Dict[str, Any] = {}):
    """Count student preferences"""
    try:
        collection = get_student_preferences_collection()
        return count(collection, filters)
    except Exception as e:
        logger.error(f"Error counting student preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error counting student preferences: {str(e)}"
        )