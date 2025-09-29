"""
University Departments CRUD API Router

This module handles university department CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging
import pprint

# Import actual university models
from src.models.university import Department

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

from src.config import MONGODB_UNIVERSITY_DEPARTMENTS, QDRANT_UNIVERSITY_DEPARTMENTS

# Configure logging
logger = logging.getLogger(__name__)

uni_department_router = APIRouter()

# Helper functions
def get_departments_collection():
    """Get the departments collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_DEPARTMENTS]

# Department endpoints
@uni_department_router.post("/filter", response_model=List[Department])
async def get_university_departments(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all university departments with pagination and filtering"""
    try:
        collection = get_departments_collection()
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [Department(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting university departments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving university departments: {str(e)}"
        )

@uni_department_router.get("/{id}", response_model=Department)
async def get_university_department(id: int):
    """Get a specific university department by ID"""
    try:
        collection = get_departments_collection()
        result = get_one(collection, {"department_id": id})
        result = Department(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid department ID format"
        )
    except Exception as e:
        logger.error(f"Error getting university department by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving university department: {str(e)}"
        )

@uni_department_router.post("/")
async def create_university_department(data: Department):
    """Create a new university department"""
    try:
        collection = get_departments_collection()

        result = insert(collection, data)
        data = data.model_dump()
        metadata = {
            "department_id": data.pop("department_id"),
            "faculty_id": data.pop("faculty_id"),
            "university_id": data.pop("university_id"),
            "reference": data.pop("contact")
        }
        insert_vecdb(QDRANT_UNIVERSITY_DEPARTMENTS, pprint.pformat(data), metadata)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating university department: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating university department: {str(e)}"
        )

@uni_department_router.put("/")
async def update_university_departments(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple university departments based on filters"""
    try:
        collection = get_departments_collection()
        result = update(collection, filters, data)
        
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                id = doc.get("department_id")
                metadata = {
                    "department_id": doc.pop("department_id"),
                    "faculty_id": doc.pop("faculty_id"),
                    "university_id": doc.pop("university_id"),
                    "reference": doc.pop("contact")
                }
                update_vecdb(QDRANT_UNIVERSITY_DEPARTMENTS, {"department_id": id}, pprint.pformat(doc), metadata)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating university departments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating university departments: {str(e)}"
        )

@uni_department_router.delete("/")
async def delete_university_departments(filters: Dict[str, Any]):
    """Delete multiple university departments based on filters"""
    try:
        collection = get_departments_collection()
        
        # Delete from MongoDB
        result = delete(collection, filters)
        
        # Delete from vector database
        if result.deleted_count > 0:
            delete_vecdb(QDRANT_UNIVERSITY_DEPARTMENTS, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting university departments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting university departments: {str(e)}"
        )

@uni_department_router.post("/count")
async def count_university_departments(filters: Dict[str, Any] = {}):
    """Count all university departments"""
    collection = get_departments_collection()
    return count(collection, filters)
