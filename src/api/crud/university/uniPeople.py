"""
People CRUD API Router

This module handles people-specific CRUD operations (Person).
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging

# Import actual university models
from src.models.university import Person

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
from src.config import MONGODB_UNIVERSITY_PEOPLE

# Configure logging
logger = logging.getLogger(__name__)

people_router = APIRouter()

# Helper functions
def get_people_collection():
    """Get the people collection"""
    db = get_mongodb_database()
    return db[MONGODB_PEOPLE]

# Health check endpoint
@people_router.get("/health")
async def health_check():
    """Health check for people CRUD operations"""
    return {"status": "healthy", "service": "people-crud"}

# Person endpoints
@people_router.get("/people", response_model=List[Person])
async def get_people(
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = {}
):
    """Get all people with pagination and filtering"""
    try:
        collection = get_people_collection()
        
        results = get_many(collection, filters, offset=skip, limit=limit)
        results = [Person(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting people: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving people: {str(e)}"
        )

@people_router.get("/people/{person_id}", response_model=Person)
async def get_person(person_id: str):
    """Get a specific person by ID"""
    try:
        collection = get_people_collection()
        result = get_one(collection, {"person_id": person_id})
        result = Person(**result) if result else None
        return result
    except Exception as e:
        logger.error(f"Error getting person by ID {person_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving person: {str(e)}"
        )

@people_router.post("/people")
async def create_person(person_data: Person):
    """Create a new person"""
    try:
        collection = get_people_collection()
        result = insert(collection, person_data)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error creating person: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating person: {str(e)}"
        )

@people_router.put("/people/{person_id}")
async def update_person(person_id: str, person_data: Person):
    """Update a person"""
    # Validate that the person_id in the data matches the URL parameter
    if person_data.person_id != person_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Person ID mismatch: URL parameter ({person_id}) does not match data person_id ({person_data.person_id})"
        )
    
    try:
        collection = get_people_collection()
        result = update(collection, {"person_id": person_id}, person_data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error updating person {person_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating person: {str(e)}"
        )

@people_router.delete("/people/{person_id}")
async def delete_person(person_id: str):
    """Delete a person"""
    try:
        collection = get_people_collection()
        result = delete(collection, {"person_id": person_id})
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error deleting person {person_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting person: {str(e)}"
        )

@people_router.put("/people")
async def update_people_bulk(
    filters: Dict[str, Any],
    update_data: Dict[str, Any]
):
    """Update multiple people based on filters"""
    try:
        collection = get_people_collection()
        result = update(collection, filters, update_data)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk updating people: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating people: {str(e)}"
        )

@people_router.delete("/people")
async def delete_people_bulk(filters: Dict[str, Any]):
    """Delete multiple people based on filters"""
    try:
        collection = get_people_collection()
        result = delete(collection, filters)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count,
            "acknowledged": result.acknowledged
        }
    except Exception as e:
        logger.error(f"Error bulk deleting people: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk deleting people: {str(e)}"
        )
