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
@uni_faculty_router.get("/university-faculties", response_model=List[Faculty])
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

@uni_faculty_router.get("/university-faculties/{faculty_id}", response_model=Faculty)
async def get_university_faculty(faculty_id: str):
    """Get a specific university faculty by ID"""
    try:
        collection = get_faculties_collection()
        result = get_one(collection, {"faculty_id": faculty_id})
        result = Faculty(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid faculty ID format"
        )
    except Exception as e:
        logger.error(f"Error getting university faculty by ID {faculty_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving university faculty: {str(e)}"
        )

@uni_faculty_router.post("/university-faculties")
async def create_university_faculty(faculty_data: Faculty):
    """Create a new university faculty"""
    try:
        collection = get_faculties_collection()
        
        # Insert into MongoDB
        result = insert(collection, faculty_data)
        
        # Prepare data for vector database
        vec_data = faculty_data.model_dump()
        vec_data.pop("faculty_id", None)
        vec_data.pop("university_id", None)
        vec_data.pop("contact", None)
        metadata = {
            "faculty_id": faculty_data.faculty_id,
            "university_id": faculty_data.university_id
        }
        
        # Insert into vector database
        insert_vecdb(QDRANT_UNIVERSITY_FACULTIES, pprint.pformat(vec_data), metadata)
        
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

@uni_faculty_router.put("/university-faculties")
async def update_university_faculties(
    filters: Dict[str, Any],
    update_data: Dict[str, Any]
):
    """Update multiple university faculties based on filters"""
    try:
        collection = get_faculties_collection()
        
        # Update in MongoDB
        result = update(collection, filters, update_data)
        
        # Update in vector database
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                vec_data = doc.copy()
                vec_data.pop("faculty_id", None)
                vec_data.pop("university_id", None)
                vec_data.pop("contact", None)
                metadata = {
                    "faculty_id": doc.get("faculty_id"),
                    "university_id": doc.get("university_id")
                }
                update_vecdb(QDRANT_UNIVERSITY_FACULTIES, {"faculty_id": doc.get("faculty_id")}, pprint.pformat(vec_data), metadata)
        
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

@uni_faculty_router.delete("/university-faculties")
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

@uni_faculty_router.get("/university-faculties/count")
async def count_university_faculties(filters: Dict[str, Any] = {}):
    """Count all university faculties"""
    collection = get_faculties_collection()
    return count(collection, filters)
