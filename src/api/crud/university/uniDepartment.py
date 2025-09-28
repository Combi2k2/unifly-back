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
@uni_department_router.get("/university-departments", response_model=List[Department])
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

@uni_department_router.get("/university-departments/{department_id}", response_model=Department)
async def get_university_department(department_id: str):
    """Get a specific university department by ID"""
    try:
        collection = get_departments_collection()
        result = get_one(collection, {"department_id": department_id})
        result = Department(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid department ID format"
        )
    except Exception as e:
        logger.error(f"Error getting university department by ID {department_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving university department: {str(e)}"
        )

@uni_department_router.post("/university-departments")
async def create_university_department(department_data: Department):
    """Create a new university department"""
    try:
        collection = get_departments_collection()
        
        # Insert into MongoDB
        result = insert(collection, department_data)
        
        # Prepare data for vector database
        vec_data = department_data.model_dump()
        vec_data.pop("department_id", None)
        vec_data.pop("faculty_id", None)
        vec_data.pop("university_id", None)
        vec_data.pop("contact", None)
        metadata = {
            "department_id": department_data.department_id,
            "university_id": department_data.university_id,
            "faculty_id": department_data.faculty_id
        }
        
        # Insert into vector database
        insert_vecdb(QDRANT_UNIVERSITY_DEPARTMENTS, pprint.pformat(vec_data), metadata)
        
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

@uni_department_router.put("/university-departments")
async def update_university_departments(
    filters: Dict[str, Any],
    update_data: Dict[str, Any]
):
    """Update multiple university departments based on filters"""
    try:
        collection = get_departments_collection()
        
        # Update in MongoDB
        result = update(collection, filters, update_data)
        
        # Update in vector database
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                vec_data = doc.copy()
                vec_data.pop("department_id", None)
                vec_data.pop("faculty_id", None)
                vec_data.pop("university_id", None)
                vec_data.pop("contact", None)
                metadata = {
                    "department_id": doc.get("department_id"),
                    "university_id": doc.get("university_id"),
                    "faculty_id": doc.get("faculty_id")
                }
                update_vecdb(QDRANT_UNIVERSITY_DEPARTMENTS, {"department_id": doc.get("department_id")}, pprint.pformat(vec_data), metadata)
        
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

@uni_department_router.delete("/university-departments")
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

@uni_department_router.get("/university-departments/count")
async def count_university_departments(filters: Dict[str, Any] = {}):
    """Count all university departments"""
    collection = get_departments_collection()
    return count(collection, filters)
