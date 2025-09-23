"""
MongoDB Repository for University Data
Handles interactions with MongoDB database for university information and rankings
"""

import logging
from typing import Optional, List
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError

from models.university import UniInfo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversityRepository:
    """Repository class to handle interactions with the MongoDB database for university data"""
    
    def __init__(self, connection_string: str, database_name: str = "unifly"):
        """
        Initialize the repository with MongoDB connection parameters
        
        Args:
            connection_string: MongoDB connection string (e.g., "mongodb://localhost:27017")
            database_name: Name of the database to use (default: "unifly")
        """
        try:
            self.database_name = database_name
            
            self.client = MongoClient(connection_string)
            self.db = self.client[self.database_name]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB database: {self.database_name}")
            
            self._initialize_collections()
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _initialize_collections(self):
        """Initialize collections and create basic indexes"""
        try:
            existing_collections = self.db.list_collection_names()
            
            # Initialize university-info collection
            if "university-info" not in existing_collections:
                self.db.create_collection("university-info")
                logger.info("Created university-info collection")
            
            # Create basic index for unique university IDs
            self.db["university-info"].create_index([("id", ASCENDING)], unique=True)
            
            self.university_collection = self.db["university-info"]
            
            logger.info("Collections and indexes initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize collections: {e}")
            raise
    
    def close(self):
        """Close the MongoDB connection"""
        try:
            if self.client:
                self.client.close()
                logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
    
    def _prepare_document_for_model(self, doc: dict) -> dict:
        """Prepare MongoDB document for UniInfo model creation"""
        try:
            # Remove MongoDB's _id field
            doc.pop("_id", None)
            return doc
        except Exception as e:
            logger.error(f"Error preparing document for model: {e}")
            return doc
    
    # ==================== University CRUD Methods ====================
    
    def upsert(self, university: UniInfo) -> int:
        """
        Insert or update a university
        
        Args:
            university: UniInfo object to upsert
            
        Returns:
            id of the upserted university
            
        Raises:
            Exception: If upsert operation fails
        """
        try:
            # Convert to dict for MongoDB storage
            university_dict = university.model_dump()
            
            result = self.university_collection.update_one(
                {"id": university.id},
                {"$set": university_dict},
                upsert=True
            )
            
            if result.upserted_id or result.modified_count > 0:
                logger.info(f"Successfully upserted university: {university.name} (id: {university.id})")
                return university.id
            else:
                logger.warning(f"No changes made to university: {university.name} (id: {university.id})")
                return university.id
                
        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error for university id {university.id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to upsert university id {university.id}: {e}")
            raise
    
    def remove(self, university_id: int) -> bool:
        """
        Remove a university
        
        Args:
            university_id: ID of the university to remove
            
        Returns:
            True if university was removed, False otherwise
        """
        try:
            result = self.university_collection.delete_one({"id": university_id})
            success = result.deleted_count > 0
            
            if success:
                logger.info(f"Successfully removed university with id: {university_id}")
            else:
                logger.warning(f"No university found to remove with id: {university_id}")
                
            return success
            
        except Exception as e:
            logger.error(f"Failed to remove university id {university_id}: {e}")
            return False
    
    def get_by_id(self, university_id: int) -> Optional[UniInfo]:
        """
        Get a university by ID
        
        Args:
            university_id: University ID to search for
            
        Returns:
            UniInfo object if found, None otherwise
        """
        try:
            result = self.university_collection.find_one({"id": university_id})
            
            if result:
                try:
                    prepared_doc = self._prepare_document_for_model(result)
                    return UniInfo(**prepared_doc)
                except Exception as validation_error:
                    logger.error(f"Validation error when creating UniInfo from document: {validation_error}")
                    logger.error(f"Document data: {result}")
                    return None
            
            logger.info(f"No university found with id: {university_id}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get university id {university_id}: {e}")
            return None
    
    def get_by_name(self, name: str) -> Optional[UniInfo]:
        """
        Get a university by name
        
        Args:
            name: University name to search for
            
        Returns:
            UniInfo object if found, None otherwise
        """
        try:
            result = self.university_collection.find_one({"name": name})
            
            if result:
                try:
                    prepared_doc = self._prepare_document_for_model(result)
                    return UniInfo(**prepared_doc)
                except Exception as validation_error:
                    logger.error(f"Validation error when creating UniInfo from document: {validation_error}")
                    logger.error(f"Document data: {result}")
                    return None
            
            logger.info(f"No university found with name: {name}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get university {name}: {e}")
            return None
    
    def get_all(self) -> List[UniInfo]:
        """
        Get all universities
        
        Returns:
            List of UniInfo objects
        """
        try:
            universities = []
            for university_dict in self.university_collection.find():
                try:
                    prepared_doc = self._prepare_document_for_model(university_dict)
                    universities.append(UniInfo(**prepared_doc))
                except Exception as validation_error:
                    logger.error(f"Validation error when creating UniInfo from document: {validation_error}")
                    logger.error(f"Document data: {university_dict}")
                    continue  # Skip invalid documents
            
            logger.info(f"Retrieved {len(universities)} universities")
            return universities
            
        except Exception as e:
            logger.error(f"Failed to get all universities: {e}")
            return []
