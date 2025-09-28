"""
Scholarship CRUD API Router

This module handles scholarship-specific CRUD operations (Scholarship, ScholarshipProvider).
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging

# Import actual university models
from src.models.university import Scholarship, ScholarshipProvider

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
from src.config import MONGODB_UNIVERSITY_SCHOLARSHIPS

# Configure logging
logger = logging.getLogger(__name__)

scholarship_router = APIRouter()

# Helper functions
def get_scholarships_collection():
    """Get the scholarships collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_SCHOLARSHIPS]

def get_scholarship_providers_collection():
    """Get the scholarship providers collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_SCHOLARSHIPS]  # Using same collection for now

# Health check endpoint
@scholarship_router.get("/health")
async def health_check():
    """Health check for scholarship CRUD operations"""
    return {"status": "healthy", "service": "scholarship-crud"}

# Scholarship endpoints
@scholarship_router.get("/scholarships", response_model=List[Scholarship])
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

@scholarship_router.get("/scholarships/{scholarship_id}", response_model=Scholarship)
async def get_scholarship(scholarship_id: str):
    """Get a specific scholarship by ID"""
    try:
        collection = get_scholarships_collection()
        result = get_one(collection, {"scholarship_id": scholarship_id})
        result = Scholarship(**result) if result else None
        return result
    except Exception as e:
        logger.error(f"Error getting scholarship by ID {scholarship_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving scholarship: {str(e)}"
        )

@scholarship_router.post("/scholarships")
async def create_scholarship(scholarship_data: Scholarship):
    """Create a new scholarship"""
    try:
        collection = get_scholarships_collection()
        result = insert(collection, scholarship_data)
        
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

@scholarship_router.put("/scholarships/{scholarship_id}")
async def update_scholarship(scholarship_id: str, scholarship_data: Scholarship):
    """Update a scholarship"""
    # Validate that the scholarship_id in the data matches the URL parameter
    if scholarship_data.scholarship_id != scholarship_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scholarship ID mismatch: URL parameter ({scholarship_id}) does not match data scholarship_id ({scholarship_data.scholarship_id})"
        )
    
    try:
        collection = get_scholarships_collection()
        result = update(collection, {"scholarship_id": scholarship_id}, scholarship_data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error updating scholarship {scholarship_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating scholarship: {str(e)}"
        )

@scholarship_router.delete("/scholarships/{scholarship_id}")
async def delete_scholarship(scholarship_id: str):
    """Delete a scholarship"""
    try:
        collection = get_scholarships_collection()
        result = delete(collection, {"scholarship_id": scholarship_id})
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error deleting scholarship {scholarship_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting scholarship: {str(e)}"
        )

# Scholarship Provider endpoints
@scholarship_router.get("/providers", response_model=List[ScholarshipProvider])
async def get_scholarship_providers(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all scholarship providers with pagination and filtering"""
    try:
        collection = get_scholarship_providers_collection()
        
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [ScholarshipProvider(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting scholarship providers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving scholarship providers: {str(e)}"
        )

@scholarship_router.get("/providers/{provider_id}", response_model=ScholarshipProvider)
async def get_scholarship_provider(provider_id: str):
    """Get a specific scholarship provider by ID"""
    try:
        collection = get_scholarship_providers_collection()
        result = get_one(collection, {"provider_id": provider_id})
        result = ScholarshipProvider(**result) if result else None
        return result
    except Exception as e:
        logger.error(f"Error getting scholarship provider by ID {provider_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving scholarship provider: {str(e)}"
        )

@scholarship_router.post("/providers")
async def create_scholarship_provider(provider_data: ScholarshipProvider):
    """Create a new scholarship provider"""
    try:
        collection = get_scholarship_providers_collection()
        result = insert(collection, provider_data)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating scholarship provider: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating scholarship provider: {str(e)}"
        )

@scholarship_router.put("/providers/{provider_id}")
async def update_scholarship_provider(provider_id: str, provider_data: ScholarshipProvider):
    """Update a scholarship provider"""
    # Validate that the provider_id in the data matches the URL parameter
    if provider_data.provider_id != provider_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Provider ID mismatch: URL parameter ({provider_id}) does not match data provider_id ({provider_data.provider_id})"
        )
    
    try:
        collection = get_scholarship_providers_collection()
        result = update(collection, {"provider_id": provider_id}, provider_data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error updating scholarship provider {provider_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating scholarship provider: {str(e)}"
        )

@scholarship_router.delete("/providers/{provider_id}")
async def delete_scholarship_provider(provider_id: str):
    """Delete a scholarship provider"""
    try:
        collection = get_scholarship_providers_collection()
        result = delete(collection, {"provider_id": provider_id})
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error deleting scholarship provider {provider_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting scholarship provider: {str(e)}"
        )
