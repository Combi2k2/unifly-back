"""
Research CRUD API Router

This module handles research CRUD operations.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
import logging
import pprint

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

# Import vector database operations
from src.integrations.internal.langchain import (
    insert_vecdb,
    delete_vecdb,
    update_vecdb
)

from src.config import MONGODB_UNIVERSITY_RESEARCH, QDRANT_UNIVERSITY_RESEARCH

# Configure logging
logger = logging.getLogger(__name__)

research_router = APIRouter()

# Helper functions
def get_research_labs_collection():
    """Get the research labs collection"""
    db = get_mongodb_database()
    return db[MONGODB_UNIVERSITY_RESEARCH]

# Research Lab endpoints
@research_router.post("/labs/filter", response_model=List[ResearchLab])
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

@research_router.get("/labs/{id}", response_model=ResearchLab)
async def get_research_lab(id: int):
    """Get a specific research lab by ID"""
    try:
        collection = get_research_labs_collection()
        result = get_one(collection, {"lab_id": id})
        result = ResearchLab(**result) if result else None
        return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid research lab ID format"
        )
    except Exception as e:
        logger.error(f"Error getting research lab by ID {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving research lab: {str(e)}"
        )

@research_router.post("/labs")
async def create_research_lab(data: ResearchLab):
    """Create a new research lab"""
    try:
        collection = get_research_labs_collection()

        result = insert(collection, data)
        data = data.model_dump()
        metadata = {
            "lab_id": data.pop("lab_id"),
            "department_id": data.pop("department_id"),
            "university_id": data.pop("university_id"),
            "reference": data.pop("contact")
        }
        insert_vecdb(QDRANT_UNIVERSITY_RESEARCH, pprint.pformat(data), metadata)
        
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

@research_router.put("/labs")
async def update_research_labs(
    filters: Dict[str, Any],
    data: Dict[str, Any]
):
    """Update multiple research labs based on filters"""
    try:
        collection = get_research_labs_collection()
        result = update(collection, filters, data)
        
        if result.modified_count > 0:
            updated_docs = get_many(collection, filters)
            for doc in updated_docs:
                id = doc.get("lab_id")
                metadata = {
                    "lab_id": doc.pop("lab_id"),
                    "department_id": doc.pop("department_id"),
                    "university_id": doc.pop("university_id"),
                    "reference": doc.pop("contact")
                }
                update_vecdb(QDRANT_UNIVERSITY_RESEARCH, {"lab_id": id}, pprint.pformat(doc), metadata)
        
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

@research_router.delete("/labs")
async def delete_research_labs(filters: Dict[str, Any]):
    """Delete multiple research labs based on filters"""
    try:
        collection = get_research_labs_collection()
        
        # Delete from MongoDB
        result = delete(collection, filters)
        
        # Delete from vector database
        if result.deleted_count > 0:
            delete_vecdb(QDRANT_UNIVERSITY_RESEARCH, filters)
        
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

@research_router.post("/labs/count")
async def count_research_labs(filters: Dict[str, Any] = {}):
    """Count all research labs"""
    collection = get_research_labs_collection()
    return count(collection, filters)
