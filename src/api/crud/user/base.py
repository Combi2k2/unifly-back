"""
Base User CRUD API Router

This module handles general user CRUD operations (UserBase).
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging

# Import actual user models
from src.models.user import UserBase

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
from src.config import MONGODB_USER_BASE

# Configure logging
logger = logging.getLogger(__name__)

user_base_router = APIRouter()

# Helper function
def get_users_collection():
    """Get the users collection"""
    db = get_mongodb_database()
    return db[MONGODB_USER_BASE]

# User endpoints
@user_base_router.get("/users", response_model=List[UserBase])
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all users with pagination and filtering"""
    try:
        collection = get_users_collection()
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [UserBase(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {str(e)}"
        )

@user_base_router.get("/users/{id}", response_model=UserBase)
async def get_user(id: int):
    """Get a specific user by ID"""
    try:
        collection = get_users_collection()
        result = get_one(collection, {"userid": id})
        result = UserBase(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    except Exception as e:
        logger.error(f"Error getting user by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user: {str(e)}"
        )

@user_base_router.post("/users")
async def create_user(data: UserBase):
    """Create a new user"""
    try:
        collection = get_users_collection()
        result = insert(collection, data)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@user_base_router.put("/users")
async def update_users(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple users based on filters"""
    try:
        collection = get_users_collection()
        result = update(collection, filters, data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating users: {str(e)}"
        )

@user_base_router.delete("/users")
async def delete_users(filters: Dict[str, Any]):
    """Delete multiple users based on filters"""
    try:
        collection = get_users_collection()
        result = delete(collection, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting users: {str(e)}"
        )

@user_base_router.get("/users/count")
async def count_users(filters: Dict[str, Any] = {}):
    """Count all users"""
    collection = get_users_collection()
    return count(collection, filters)