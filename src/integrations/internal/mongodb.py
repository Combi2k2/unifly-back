"""
MongoDB Client Initialization
Provides centralized MongoDB client management for the Unifly Backend
"""

import logging
from typing import Optional, List, Dict, Any
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Import configuration
from src.config import (
    MONGODB_CONNECTION_STRING,
    MONGODB_DATABASE_NAME
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable for client management
_client = None


def get_mongodb_client() -> MongoClient:
    """
    Get MongoDB client instance
    Creates new client if not exists or connection is lost
    
    Returns:
        MongoClient instance
    """
    global _client
    
    try:
        if _client is None:
            _client = MongoClient(
                MONGODB_CONNECTION_STRING,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,         # 10 second connection timeout
                socketTimeoutMS=20000,          # 20 second socket timeout
                maxPoolSize=50,                 # Maximum number of connections
                minPoolSize=5,                  # Minimum number of connections
                maxIdleTimeMS=30000,            # Close connections after 30 seconds of inactivity
                retryWrites=True,               # Retry write operations
                retryReads=True                 # Retry read operations
            )
            logger.info(f"MongoDB client created successfully with connection: {MONGODB_CONNECTION_STRING}")
        
        # Test connection
        _client.admin.command('ping')
        logger.debug("MongoDB connection is healthy")
        
        return _client
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        _client = None
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        _client = None
        raise

def get_mongodb_database(database_name: str = MONGODB_DATABASE_NAME) -> Database:
    """
    Get database instance
    
    Args:
        database_name: Name of the database to connect to
        
    Returns:
        Database instance
    """
    try:
        client = get_mongodb_client()
        database = client[database_name]
        
        # Test database access
        database.command('ping')
        logger.debug(f"Successfully connected to database: {database_name}")
        
        return database
        
    except Exception as e:
        logger.error(f"Failed to access database {database_name}: {e}")
        raise

def get_mongodb_collection(database_name: str = MONGODB_DATABASE_NAME, collection_name: str = None) -> Collection:
    """
    Get collection instance

    Args:
        database_name: Name of the database to connect to
        collection_name: Name of the collection to connect to

    Returns:
        Collection instance
    """
    try:
        database = get_mongodb_database(database_name)
        collection = database[collection_name]
        logger.debug(f"Successfully connected to collection: {collection_name}")
        return collection
    except Exception as e:
        logger.error(f"Failed to access collection {collection_name}: {e}")
        raise

def close_mongodb_connection():
    """Close MongoDB client connection"""
    global _client
    
    try:
        if _client:
            _client.close()
            _client = None
            logger.info("MongoDB client connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB client: {e}")

def check_mongodb_connection() -> bool:
    """
    Check if MongoDB client is connected
    
    Returns:
        True if connected, False otherwise
    """
    global _client
    
    try:
        if _client is None:
            return False
        
        # Test connection with a simple ping
        _client.admin.command('ping')
        return True
        
    except Exception:
        return False

def reconnect_mongodb():
    """Force reconnection to MongoDB"""
    logger.info("Attempting to reconnect to MongoDB...")
    close_mongodb_connection()
    return get_mongodb_client()

# =====================
# Base CRUD Operations
# =====================

def create(collection: Collection, obj: Any) -> Any:
    """
    Create a new document in the collection
    
    Args:
        collection: MongoDB collection instance
        obj: Document to create (dict or object with model_dump method)
        
    Returns:
        ID of the created document
    """
    try:
        document = obj.model_dump() if hasattr(obj, 'model_dump') else obj
        result = collection.insert_one(document)
        logger.info(f"Created document in {collection.name} with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        logger.error(f"Failed to create document in {collection.name}: {e}")
        raise

def read_one(collection: Collection, id: Any) -> Optional[Dict[str, Any]]:
    """
    Read a document by its ID
    
    Args:
        collection: MongoDB collection instance
        id: ID of the document to read
        
    Returns:
        Document dict if found, None otherwise
    """
    try:
        document = collection.find_one({"_id": id})
        if document:
            document.pop("_id", None)  # Remove MongoDB's _id field
            return document
        return None
    except Exception as e:
        logger.error(f"Failed to read document by ID {id} from {collection.name}: {e}")
        return None

def read_many(collection: Collection, filters: Dict[str, Any] = {}, offset: int = 0, limit: int = 1) -> List[Dict[str, Any]]:
    """
    Read multiple documents by attribute filters with pagination support
    
    Args:
        collection: MongoDB collection instance
        filters: Dictionary of field-value pairs that returned documents must satisfy
        offset: Number of documents to skip (for pagination)
        limit: Optional limit on number of documents to return
        
    Returns:
        List of document dictionaries
    """
    try:
        cursor = collection.find(filters)
        
        # Apply offset for pagination
        if offset > 0:
            cursor = cursor.skip(offset)
        
        # Apply limit if specified
        if limit:
            cursor = cursor.limit(limit)
        
        documents = []
        for doc in cursor:
            doc.pop("_id", None)  # Remove MongoDB's _id field
            documents.append(doc)
        
        logger.info(f"Retrieved {len(documents)} documents with filters {filters} from {collection.name} (offset: {offset}, limit: {limit})")
        return documents
    except Exception as e:
        logger.error(f"Failed to read documents by filters {filters} from {collection.name}: {e}")
        return []

def update(collection: Collection, id: Any, obj: Any) -> bool:
    """
    Update a document by its ID
    
    Args:
        collection: MongoDB collection instance
        id: ID of the document to update
        obj: Updated document (dict or object with model_dump method)
        
    Returns:
        True if document was updated, False otherwise
    """
    try:
        document = obj.model_dump() if hasattr(obj, 'model_dump') else obj
        result = collection.update_one(
            {"_id": id},
            {"$set": document}
        )
        
        if result.modified_count > 0:
            logger.info(f"Updated document with ID {id} in {collection.name}")
            return True
        else:
            logger.warning(f"No document found with ID {id} in {collection.name}")
            return False
    except Exception as e:
        logger.error(f"Failed to update document with ID {id} in {collection.name}: {e}")
        return False

def delete(collection: Collection, id: Any) -> bool:
    """
    Delete a document by its ID
    
    Args:
        collection: MongoDB collection instance
        id: ID of the document to delete
        
    Returns:
        True if document was deleted, False otherwise
    """
    try:
        result = collection.delete_one({"_id": id})
        
        if result.deleted_count > 0:
            logger.info(f"Deleted document with ID {id} from {collection.name}")
            return True
        else:
            logger.warning(f"No document found with ID {id} in {collection.name}")
            return False
    except Exception as e:
        logger.error(f"Failed to delete document with ID {id} from {collection.name}: {e}")
        return False

def count(collection: Collection) -> int:
    """
    Count total number of documents in the collection
    
    Args:
        collection: MongoDB collection instance
        
    Returns:
        Total count of documents
    """
    try:
        count = collection.count_documents({})
        logger.info(f"Total documents in {collection.name}: {count}")
        return count
    except Exception as e:
        logger.error(f"Failed to count documents in {collection.name}: {e}")
        return 0

if __name__ == "__main__":
    print("MongoDB Client Initialization Test")
    print("=" * 40)
    
    try:
        # Test connection
        client = get_mongodb_client()
        print(f"✓ MongoDB client created successfully")
        
        # Test database access
        db = get_mongodb_database("test_db")
        print(f"✓ Database access successful")
        
        # Test connection status
        if check_mongodb_connection():
            print("✓ MongoDB connection is healthy")
        else:
            print("✗ MongoDB connection is not healthy")
        
        print("\nMongoDB client initialization test completed successfully!")
        
    except Exception as e:
        print(f"✗ MongoDB client initialization test failed: {e}")
        logger.error(f"Test failed: {e}")