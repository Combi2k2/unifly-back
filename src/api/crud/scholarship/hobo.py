"""
Scholarship CRUD API Router

This module handles scholarship CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging
import pprint

# Import actual university models
from src.models.university import Scholarship

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

from src.config import MONGODB_SCHOLARSHIPS, QDRANT_SCHOLARSHIPS

# Configure logging
logger = logging.getLogger(__name__)

hobo_router = APIRouter()

# Helper functions
def get_scholarships_collection():
    """Get the scholarships collection"""
    db = get_mongodb_database()
    return db[MONGODB_SCHOLARSHIPS]

# Scholarship endpoints
@hobo_router.post("/filter", response_model=List[Scholarship])
async def get_scholarships(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all scholarships with pagination and filtering"""
    try:
        collection = get_scholarships_collection()
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [Scholarship(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting scholarships: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving scholarships: {str(e)}"
        )

@hobo_router.get("/{id}", response_model=Scholarship)
async def get_scholarship(id: int):
    """Get a specific scholarship by ID"""
    try:
        collection = get_scholarships_collection()
        result = get_one(collection, {"scholarship_id": id})
        result = Scholarship(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid scholarship ID format"
        )
    except Exception as e:
        logger.error(f"Error getting scholarship by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving scholarship: {str(e)}"
        )

@hobo_router.post("/")
async def create_scholarship(data: Scholarship):
    """Create a new scholarship"""
    try:
        collection = get_scholarships_collection()

        result = insert(collection, data)
        data = data.model_dump()
        metadata = {
            "scholarship_id": data.pop("scholarship_id"),
            "provider_id": data.pop("provider_id"),
            "reference": data.pop("contact")
        }
        insert_vecdb(QDRANT_SCHOLARSHIPS, pprint.pformat(data), metadata)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating scholarship: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating scholarship: {str(e)}"
        )

@hobo_router.put("/")
async def update_scholarships(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple scholarships based on filters"""
    try:
        collection = get_scholarships_collection()
        result = update(collection, filters, data)
        
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                id = doc.get("scholarship_id")
                metadata = {
                    "scholarship_id": doc.pop("scholarship_id"),
                    "provider_id": doc.pop("provider_id"),
                    "reference": doc.pop("contact")
                }
                update_vecdb(QDRANT_SCHOLARSHIPS, {"scholarship_id": id}, pprint.pformat(doc), metadata)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating scholarships: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating scholarships: {str(e)}"
        )

@hobo_router.delete("/")
async def delete_scholarships(filters: Dict[str, Any]):
    """Delete multiple scholarships based on filters"""
    try:
        collection = get_scholarships_collection()
        
        # Delete from MongoDB
        result = delete(collection, filters)
        
        # Delete from vector database
        if result.deleted_count > 0:
            delete_vecdb(QDRANT_SCHOLARSHIPS, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting scholarships: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting scholarships: {str(e)}"
        )

@hobo_router.post("/count")
async def count_scholarships(filters: Dict[str, Any] = {}):
    """Count all scholarships"""
    collection = get_scholarships_collection()
    return count(collection, filters)
