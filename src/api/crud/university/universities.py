"""
Universities CRUD API Router

This module handles university CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging
import pprint

# Import actual university models
from src.models.university import University

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

from src.config import MONGODB_UNIVERSITIES, QDRANT_UNIVERSITIES

# Configure logging
logger = logging.getLogger(__name__)

universities_router = APIRouter()

# Helper functions
def get_universities_collection():
    """Get the universities collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITIES]

# University endpoints
@universities_router.post("/filter", response_model=List[University])
async def get_universities(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all universities with pagination and filtering"""
    try:
        collection = get_universities_collection()
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [University(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting universities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving universities: {str(e)}"
        )

@universities_router.get("/{id}", response_model=University)
async def get_university(id: int):
    """Get a specific university by ID"""
    try:
        collection = get_universities_collection()
        result = get_one(collection, {"university_id": id})
        result = University(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid university ID format"
        )
    except Exception as e:
        logger.error(f"Error getting university by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving university: {str(e)}"
        )

@universities_router.post("/")
async def create_university(data: University):
    """Create a new university"""
    try:
        collection = get_universities_collection()

        result = insert(collection, data)
        data = data.model_dump()
        metadata = {
            "university_id": data.pop("university_id"),
            "reference": data.pop("contact")
        }
        insert_vecdb(QDRANT_UNIVERSITIES, pprint.pformat(data), metadata)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating university: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating university: {str(e)}"
        )

@universities_router.put("/")
async def update_universities(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple universities based on filters"""
    try:
        collection = get_universities_collection()
        result = update(collection, filters, data)
        
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                id = doc.get("university_id")
                metadata = {
                    "university_id": doc.pop("university_id"),
                    "reference": doc.pop("contact")
                }
                update_vecdb(QDRANT_UNIVERSITIES, {"university_id": id}, pprint.pformat(doc), metadata)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating universities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating universities: {str(e)}"
        )

@universities_router.delete("/")
async def delete_universities(filters: Dict[str, Any]):
    """Delete multiple universities based on filters"""
    try:
        collection = get_universities_collection()
        
        # Delete from MongoDB
        result = delete(collection, filters)
        
        # Delete from vector database
        if result.deleted_count > 0:
            delete_vecdb(QDRANT_UNIVERSITIES, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting universities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting universities: {str(e)}"
        )

@universities_router.post("/count")
async def count_universities(filters: Dict[str, Any] = {}):
    """Count all universities"""
    collection = get_universities_collection()
    return count(collection, filters)
