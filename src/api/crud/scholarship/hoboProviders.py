"""
Scholarship Provider CRUD API Router

This module handles scholarship provider CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging
import pprint

# Import actual university models
from src.models.university import ScholarshipProvider

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

from src.config import MONGODB_SCHOLARSHIP_PROVIDERS, QDRANT_SCHOLARSHIP_PROVIDERS

# Configure logging
logger = logging.getLogger(__name__)

providers_router = APIRouter()

# Helper functions
def get_scholarship_providers_collection():
    """Get the scholarship providers collection"""
    db = get_mongodb_database()
    return db[MONGODB_SCHOLARSHIP_PROVIDERS]

# Scholarship Provider endpoints
@providers_router.post("/filter", response_model=List[ScholarshipProvider])
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

@providers_router.get("/{id}", response_model=ScholarshipProvider)
async def get_scholarship_provider(id: int):
    """Get a specific scholarship provider by ID"""
    try:
        collection = get_scholarship_providers_collection()
        result = get_one(collection, {"provider_id": id})
        result = ScholarshipProvider(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid provider ID format"
        )
    except Exception as e:
        logger.error(f"Error getting scholarship provider by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving scholarship provider: {str(e)}"
        )

@providers_router.post("/")
async def create_scholarship_provider(data: ScholarshipProvider):
    """Create a new scholarship provider"""
    try:
        collection = get_scholarship_providers_collection()

        result = insert(collection, data)
        data = data.model_dump()
        metadata = {
            "provider_id": data.pop("provider_id"),
            "reference": data.pop("contact")
        }
        insert_vecdb(QDRANT_SCHOLARSHIP_PROVIDERS, pprint.pformat(data), metadata)
        
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

@providers_router.put("/")
async def update_scholarship_providers(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple scholarship providers based on filters"""
    try:
        collection = get_scholarship_providers_collection()
        result = update(collection, filters, data)
        
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                id = doc.get("provider_id")
                metadata = {
                    "provider_id": doc.pop("provider_id"),
                    "reference": doc.pop("contact")
                }
                update_vecdb(QDRANT_SCHOLARSHIP_PROVIDERS, {"provider_id": id}, pprint.pformat(doc), metadata)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating scholarship providers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating scholarship providers: {str(e)}"
        )

@providers_router.delete("/")
async def delete_scholarship_providers(filters: Dict[str, Any]):
    """Delete multiple scholarship providers based on filters"""
    try:
        collection = get_scholarship_providers_collection()
        
        # Delete from MongoDB
        result = delete(collection, filters)
        
        # Delete from vector database
        if result.deleted_count > 0:
            delete_vecdb(QDRANT_SCHOLARSHIP_PROVIDERS, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting scholarship providers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting scholarship providers: {str(e)}"
        )

@providers_router.post("/count")
async def count_scholarship_providers(filters: Dict[str, Any] = {}):
    """Count all scholarship providers"""
    collection = get_scholarship_providers_collection()
    return count(collection, filters)
