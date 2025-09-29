"""
People CRUD API Router

This module handles people CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging
import pprint

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

# Import vector database operations
from src.integrations.internal.langchain import (
    insert_vecdb,
    delete_vecdb,
    update_vecdb
)

from src.config import MONGODB_UNIVERSITY_PEOPLE, QDRANT_UNIVERSITY_PEOPLE

# Configure logging
logger = logging.getLogger(__name__)

people_router = APIRouter()

# Helper functions
def get_people_collection():
    """Get the people collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_PEOPLE]

# Person endpoints
@people_router.post("/filter", response_model=List[Person])
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

@people_router.get("/{id}", response_model=Person)
async def get_person(id: int):
    """Get a specific person by ID"""
    try:
        collection = get_people_collection()
        result = get_one(collection, {"person_id": id})
        result = Person(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid person ID format"
        )
    except Exception as e:
        logger.error(f"Error getting person by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving person: {str(e)}"
        )

@people_router.post("/")
async def create_person(data: Person):
    """Create a new person"""
    try:
        collection = get_people_collection()

        result = insert(collection, data)
        data = data.model_dump()
        metadata = {
            "person_id": data.pop("person_id"),
            "university_id": data.pop("university_id"),
            "reference": data.pop("contact")
        }
        insert_vecdb(QDRANT_UNIVERSITY_PEOPLE, pprint.pformat(data), metadata)
        
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

@people_router.put("/")
async def update_people(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple people based on filters"""
    try:
        collection = get_people_collection()
        result = update(collection, filters, data)
        
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                id = doc.get("person_id")
                metadata = {
                    "person_id": doc.pop("person_id"),
                    "university_id": doc.pop("university_id"),
                    "reference": doc.pop("contact")
                }
                update_vecdb(QDRANT_UNIVERSITY_PEOPLE, {"person_id": id}, pprint.pformat(doc), metadata)
        
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

@people_router.delete("/")
async def delete_people(filters: Dict[str, Any]):
    """Delete multiple people based on filters"""
    try:
        collection = get_people_collection()
        
        # Delete from MongoDB
        result = delete(collection, filters)
        
        # Delete from vector database
        if result.deleted_count > 0:
            delete_vecdb(QDRANT_UNIVERSITY_PEOPLE, filters)
        
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

@people_router.post("/count")
async def count_people(filters: Dict[str, Any] = {}):
    """Count all people"""
    collection = get_people_collection()
    return count(collection, filters)
