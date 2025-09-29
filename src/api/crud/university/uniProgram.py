"""
Program CRUD API Router

This module handles program CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging
import pprint

# Import actual university models
from src.models.university import Program

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

from src.config import MONGODB_UNIVERSITY_PROGRAMS, QDRANT_UNIVERSITY_PROGRAMS

# Configure logging
logger = logging.getLogger(__name__)

program_router = APIRouter()

# Helper functions
def get_programs_collection():
    """Get the programs collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_PROGRAMS]

# Program endpoints
@program_router.post("/filter", response_model=List[Program])
async def get_programs(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all programs with pagination and filtering"""
    try:
        collection = get_programs_collection()
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [Program(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting programs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving programs: {str(e)}"
        )

@program_router.get("/{id}", response_model=Program)
async def get_program(id: int):
    """Get a specific program by ID"""
    try:
        collection = get_programs_collection()
        result = get_one(collection, {"program_id": id})
        result = Program(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid program ID format"
        )
    except Exception as e:
        logger.error(f"Error getting program by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving program: {str(e)}"
        )

@program_router.post("/")
async def create_program(data: Program):
    """Create a new program"""
    try:
        collection = get_programs_collection()

        result = insert(collection, data)
        data = data.model_dump()
        metadata = {
            "program_id": data.pop("program_id"),
            "department_id": data.pop("department_id"),
            "university_id": data.pop("university_id"),
            "reference": data.pop("contact")
        }
        insert_vecdb(QDRANT_UNIVERSITY_PROGRAMS, pprint.pformat(data), metadata)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating program: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating program: {str(e)}"
        )

@program_router.put("/")
async def update_programs(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple programs based on filters"""
    try:
        collection = get_programs_collection()
        result = update(collection, filters, data)
        
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                id = doc.get("program_id")
                metadata = {
                    "program_id": doc.pop("program_id"),
                    "department_id": doc.pop("department_id"),
                    "university_id": doc.pop("university_id"),
                    "reference": doc.pop("contact")
                }
                update_vecdb(QDRANT_UNIVERSITY_PROGRAMS, {"program_id": id}, pprint.pformat(doc), metadata)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating programs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating programs: {str(e)}"
        )

@program_router.delete("/")
async def delete_programs(filters: Dict[str, Any]):
    """Delete multiple programs based on filters"""
    try:
        collection = get_programs_collection()
        
        # Delete from MongoDB
        result = delete(collection, filters)
        
        # Delete from vector database
        if result.deleted_count > 0:
            delete_vecdb(QDRANT_UNIVERSITY_PROGRAMS, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting programs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting programs: {str(e)}"
        )

@program_router.post("/count")
async def count_programs(filters: Dict[str, Any] = {}):
    """Count all programs"""
    collection = get_programs_collection()
    return count(collection, filters)
