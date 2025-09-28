"""
Campus CRUD API Router

This module handles campus-specific CRUD operations (Campus).
Facilities are embedded within Campus data, not stored separately.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging

# Import actual university models
from src.models.university import Campus

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
from src.config import (
    MONGODB_UNIVERSITY_CAMPUSES
)

# Configure logging
logger = logging.getLogger(__name__)

campus_router = APIRouter()

# Helper functions
def get_campuses_collection():
    """Get the campuses collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_CAMPUSES]


# Health check endpoint
@campus_router.get("/health")
async def health_check():
    """Health check for campus CRUD operations"""
    return {"status": "healthy", "service": "campus-crud"}

# Campus endpoints
@campus_router.get("/campuses", response_model=List[Campus])
async def get_campuses(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all campuses with pagination and filtering"""
    try:
        collection = get_campuses_collection()
        
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [Campus(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting campuses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving campuses: {str(e)}"
        )

@campus_router.get("/campuses/{campus_id}", response_model=Campus)
async def get_campus(campus_id: str):
    """Get a specific campus by ID"""
    try:
        # Validate campus_id format (should be an integer)
        try:
            campus_id_int = int(campus_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid campus_id format: {campus_id}. Expected integer."
            )
        
        collection = get_campuses_collection()
        result = get_one(collection, {"campus_id": campus_id_int})
        result = Campus(**result) if result else None
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campus by ID {campus_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving campus: {str(e)}"
        )

@campus_router.post("/campuses")
async def create_campus(campus_data: Campus):
    """Create a new campus"""
    try:
        collection = get_campuses_collection()
        result = insert(collection, campus_data)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating campus: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating campus: {str(e)}"
        )

@campus_router.put("/campuses")
async def update_campuses_bulk(
    filters: Dict[str, Any], 
    update_data: Dict[str, Any]
):
    """Update multiple campuses based on filters"""
    try:
        collection = get_campuses_collection()
        result = update(collection, filters, update_data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error updating campuses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating campuses: {str(e)}"
        )

@campus_router.delete("/campuses")
async def delete_campuses_bulk(filters: Dict[str, Any]):
    """Delete multiple campuses based on filters"""
    try:
        collection = get_campuses_collection()
        result = delete(collection, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error deleting campuses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting campuses: {str(e)}"
        )

@campus_router.get("/campuses/count")
async def count_campuses(filters: Optional[Dict[str, Any]] = {}):
    """Count campuses based on filters"""
    try:
        collection = get_campuses_collection()
        result = count(collection, filters)
        return {"count": result}
    except Exception as e:
        logger.error(f"Error counting campuses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error counting campuses: {str(e)}"
        )

