"""
Program CRUD API Router

This module handles program-specific CRUD operations (Program).
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging

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
from src.config import MONGODB_UNIVERSITY_PROGRAMS

# Configure logging
logger = logging.getLogger(__name__)

program_router = APIRouter()

# Helper functions
def get_programs_collection():
    """Get the programs collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_PROGRAMS]

# Health check endpoint
@program_router.get("/health")
async def health_check():
    """Health check for program CRUD operations"""
    return {"status": "healthy", "service": "program-crud"}

# Program endpoints
@program_router.get("/programs", response_model=List[Program])
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

@program_router.get("/programs/{program_id}", response_model=Program)
async def get_program(program_id: str):
    """Get a specific program by ID"""
    try:
        collection = get_programs_collection()
        result = get_one(collection, {"program_id": program_id})
        result = Program(**result) if result else None
        return result
    except Exception as e:
        logger.error(f"Error getting program by ID {program_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving program: {str(e)}"
        )

@program_router.post("/programs")
async def create_program(program_data: Program):
    """Create a new program"""
    try:
        collection = get_programs_collection()
        result = insert(collection, program_data)
        
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

@program_router.put("/programs/{program_id}")
async def update_program(program_id: str, program_data: Program):
    """Update a program"""
    # Validate that the program_id in the data matches the URL parameter
    if program_data.program_id != program_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Program ID mismatch: URL parameter ({program_id}) does not match data program_id ({program_data.program_id})"
        )
    
    try:
        collection = get_programs_collection()
        result = update(collection, {"program_id": program_id}, program_data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error updating program {program_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating program: {str(e)}"
        )

@program_router.delete("/programs/{program_id}")
async def delete_program(program_id: str):
    """Delete a program"""
    try:
        collection = get_programs_collection()
        result = delete(collection, {"program_id": program_id})
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error deleting program {program_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting program: {str(e)}"
        )

@program_router.put("/programs")
async def update_programs_bulk(
    filters: Dict[str, Any],
    update_data: Dict[str, Any]
):
    """Update multiple programs based on filters"""
    try:
        collection = get_programs_collection()
        result = update(collection, filters, update_data)
        
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

@program_router.delete("/programs")
async def delete_programs_bulk(filters: Dict[str, Any]):
    """Delete multiple programs based on filters"""
    try:
        collection = get_programs_collection()
        result = delete(collection, filters)
        
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
