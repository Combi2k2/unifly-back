"""
Campus CRUD API Router

This module handles campus CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging
import pprint

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

# Import vector database operations
from src.integrations.internal.langchain import (
    insert_vecdb,
    delete_vecdb,
    update_vecdb
)

from src.config import MONGODB_UNIVERSITY_CAMPUSES, QDRANT_UNIVERSITY_CAMPUSES

# Configure logging
logger = logging.getLogger(__name__)

campus_router = APIRouter()

# Helper functions
def get_campuses_collection():
    """Get the campuses collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_CAMPUSES]

# Campus endpoints
@campus_router.post("/filter", response_model=List[Campus])
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

@campus_router.get("/{id}", response_model=Campus)
async def get_campus(id: int):
    """Get a specific campus by ID"""
    try:
        collection = get_campuses_collection()
        result = get_one(collection, {"campus_id": id})
        result = Campus(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid campus ID format"
        )
    except Exception as e:
        logger.error(f"Error getting campus by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving campus: {str(e)}"
        )

@campus_router.post("/")
async def create_campus(data: Campus):
    """Create a new campus"""
    try:
        collection = get_campuses_collection()

        result = insert(collection, data)
        data = data.model_dump()
        metadata = {
            "campus_id": data.pop("campus_id"),
            "university_id": data.pop("university_id"),
            "reference": data.pop("contact")
        }
        insert_vecdb(QDRANT_UNIVERSITY_CAMPUSES, pprint.pformat(data), metadata)
        
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

@campus_router.put("/")
async def update_campuses(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple campuses based on filters"""
    try:
        collection = get_campuses_collection()
        result = update(collection, filters, data)
        
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                id = doc.get("campus_id")
                metadata = {
                    "campus_id": doc.pop("campus_id"),
                    "university_id": doc.pop("university_id"),
                    "reference": doc.pop("contact")
                }
                update_vecdb(QDRANT_UNIVERSITY_CAMPUSES, {"campus_id": id}, pprint.pformat(doc), metadata)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating campuses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating campuses: {str(e)}"
        )

@campus_router.delete("/")
async def delete_campuses(filters: Dict[str, Any]):
    """Delete multiple campuses based on filters"""
    try:
        collection = get_campuses_collection()
        
        # Delete from MongoDB
        result = delete(collection, filters)
        
        # Delete from vector database
        if result.deleted_count > 0:
            delete_vecdb(QDRANT_UNIVERSITY_CAMPUSES, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting campuses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting campuses: {str(e)}"
        )

@campus_router.post("/count")
async def count_campuses(filters: Dict[str, Any] = {}):
    """Count all campuses"""
    collection = get_campuses_collection()
    return count(collection, filters)

