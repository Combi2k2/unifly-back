"""
University Faculties CRUD API Router

This module handles university faculty CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging
import pprint

# Import actual university models
from src.models.university import Faculty

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

from src.config import MONGODB_UNIVERSITY_FACULTIES, QDRANT_UNIVERSITY_FACULTIES

# Configure logging
logger = logging.getLogger(__name__)

uni_faculty_router = APIRouter()

# Helper functions
def get_faculties_collection():
    """Get the faculties collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_FACULTIES]

# Faculty endpoints
@uni_faculty_router.post("/filter", response_model=List[Faculty])
async def get_university_faculties(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all university faculties with pagination and filtering"""
    try:
        collection = get_faculties_collection()
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [Faculty(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting university faculties: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving university faculties: {str(e)}"
        )

@uni_faculty_router.get("/{id}", response_model=Faculty)
async def get_university_faculty(id: int):
    """Get a specific university faculty by ID"""
    try:
        collection = get_faculties_collection()
        result = get_one(collection, {"faculty_id": id})
        result = Faculty(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid faculty ID format"
        )
    except Exception as e:
        logger.error(f"Error getting university faculty by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving university faculty: {str(e)}"
        )

@uni_faculty_router.post("/")
async def create_university_faculty(data: Faculty):
    """Create a new university faculty"""
    try:
        collection = get_faculties_collection()

        result = insert(collection, data)
        data = data.model_dump()
        metadata = {
            "faculty_id": data.pop("faculty_id"),
            "university_id": data.pop("university_id"),
            "reference": data.pop("contact")
        }
        insert_vecdb(QDRANT_UNIVERSITY_FACULTIES, pprint.pformat(data), metadata)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating university faculty: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating university faculty: {str(e)}"
        )

@uni_faculty_router.put("/")
async def update_university_faculties(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple university faculties based on filters"""
    try:
        collection = get_faculties_collection()
        result = update(collection, filters, data)
        
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                id = doc.get("faculty_id")
                metadata = {
                    "faculty_id": doc.pop("faculty_id"),
                    "university_id": doc.pop("university_id"),
                    "reference": doc.pop("contact")
                }
                update_vecdb(QDRANT_UNIVERSITY_FACULTIES, {"faculty_id": id}, pprint.pformat(doc), metadata)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating university faculties: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating university faculties: {str(e)}"
        )

@uni_faculty_router.delete("/")
async def delete_university_faculties(filters: Dict[str, Any]):
    """Delete multiple university faculties based on filters"""
    try:
        collection = get_faculties_collection()
        
        # Delete from MongoDB
        result = delete(collection, filters)
        
        # Delete from vector database
        if result.deleted_count > 0:
            delete_vecdb(QDRANT_UNIVERSITY_FACULTIES, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting university faculties: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting university faculties: {str(e)}"
        )

@uni_faculty_router.post("/count")
async def count_university_faculties(filters: Dict[str, Any] = {}):
    """Count all university faculties"""
    collection = get_faculties_collection()
    return count(collection, filters)
