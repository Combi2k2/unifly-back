"""
Research CRUD API Router

This module handles research-specific CRUD operations (ResearchLab).
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging

# Import actual university models
from src.models.university import ResearchLab

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
from src.config import MONGODB_UNIVERSITY_RESEARCH

# Configure logging
logger = logging.getLogger(__name__)

research_router = APIRouter()

# Helper functions
def get_research_labs_collection():
    """Get the research labs collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_RESEARCH]

# Health check endpoint
@research_router.get("/health")
async def health_check():
    """Health check for research CRUD operations"""
    return {"status": "healthy", "service": "research-crud"}

# Research Lab endpoints
@research_router.get("/research-labs", response_model=List[ResearchLab])
async def get_research_labs(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all research labs with pagination and filtering"""
    try:
        collection = get_research_labs_collection()
        
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [ResearchLab(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting research labs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving research labs: {str(e)}"
        )

@research_router.get("/research-labs/{lab_id}", response_model=ResearchLab)
async def get_research_lab(lab_id: str):
    """Get a specific research lab by ID"""
    try:
        collection = get_research_labs_collection()
        result = get_one(collection, {"lab_id": lab_id})
        result = ResearchLab(**result) if result else None
        return result
    except Exception as e:
        logger.error(f"Error getting research lab by ID {lab_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving research lab: {str(e)}"
        )

@research_router.post("/research-labs")
async def create_research_lab(lab_data: ResearchLab):
    """Create a new research lab"""
    try:
        collection = get_research_labs_collection()
        result = insert(collection, lab_data)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating research lab: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating research lab: {str(e)}"
        )

@research_router.put("/research-labs/{lab_id}")
async def update_research_lab(lab_id: str, lab_data: ResearchLab):
    """Update a research lab"""
    # Validate that the lab_id in the data matches the URL parameter
    if lab_data.lab_id != lab_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lab ID mismatch: URL parameter ({lab_id}) does not match data lab_id ({lab_data.lab_id})"
        )
    
    try:
        collection = get_research_labs_collection()
        result = update(collection, {"lab_id": lab_id}, lab_data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error updating research lab {lab_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating research lab: {str(e)}"
        )

@research_router.delete("/research-labs/{lab_id}")
async def delete_research_lab(lab_id: str):
    """Delete a research lab"""
    try:
        collection = get_research_labs_collection()
        result = delete(collection, {"lab_id": lab_id})
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error deleting research lab {lab_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting research lab: {str(e)}"
        )

@research_router.put("/research-labs")
async def update_research_labs_bulk(
    filters: Dict[str, Any],
    update_data: Dict[str, Any]
):
    """Update multiple research labs based on filters"""
    try:
        collection = get_research_labs_collection()
        result = update(collection, filters, update_data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating research labs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating research labs: {str(e)}"
        )

@research_router.delete("/research-labs")
async def delete_research_labs_bulk(filters: Dict[str, Any]):
    """Delete multiple research labs based on filters"""
    try:
        collection = get_research_labs_collection()
        result = delete(collection, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting research labs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting research labs: {str(e)}"
        )
