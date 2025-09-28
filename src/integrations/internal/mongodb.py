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

def insert(collection: Collection, obj: Any) -> Any:
    """
    Insert a new document in the collection
    
    Args:
        collection: MongoDB collection instance
        obj: Document to insert (dict or object with model_dump method)
        
    Returns:
        ID of the inserted document
    """
    try:
        document = obj.model_dump() if hasattr(obj, 'model_dump') else obj
        result = collection.insert_one(document)
        logger.info(f"Inserted document in {collection.name} with ID: {result.inserted_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to insert document in {collection.name}: {e}")
        raise

def get_one(collection: Collection, filters: Dict[str, Any] = {}) -> Optional[Dict[str, Any]]:
    """
    Get a document by filters
    
    Args:
        collection: MongoDB collection instance
        filters: Dictionary of field-value pairs that the document must satisfy
        
    Returns:
        Document dict if found, None otherwise
    """
    try:
        document = collection.find_one(filters)
        if document:
            document.pop("_id", None)  # Remove MongoDB's _id field
            return document
        return None
    except Exception as e:
        logger.error(f"Failed to get document with filters {filters} from {collection.name}: {e}")
        raise

def get_many(collection: Collection, filters: Dict[str, Any] = {}, offset: int = 0, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Get multiple documents by attribute filters with pagination support
    
    Args:
        collection: MongoDB collection instance
        filters: Dictionary of field-value pairs that returned documents must satisfy
        offset: Number of documents to skip (for pagination)
        limit: Optional limit on number of documents to return. If limit is 0, all documents will be returned.
        
    Returns:
        List of document dictionaries
    """
    try:
        cursor = collection.find(filters)
        cursor = cursor.skip(offset) if offset > 0 else cursor
        cursor = cursor.limit(limit) if limit > 0 else cursor
        
        documents = []
        for doc in cursor:
            doc.pop("_id", None)  # Remove MongoDB's _id field
            documents.append(doc)
        
        logger.info(f"Retrieved {len(documents)} documents with filters {filters} from {collection.name} (offset: {offset}, limit: {limit})")
        return documents
    except Exception as e:
        logger.error(f"Failed to get documents by filters {filters} from {collection.name}: {e}")
        raise

def update(collection: Collection, filters: Dict[str, Any], data: Any) -> bool:
    """
    Update documents by filters
    
    Args:
        collection: MongoDB collection instance
        filters: Dictionary of field-value pairs that documents must satisfy
        data: Updated document data (dict or object with model_dump method)
        
    Returns:
        True if document was updated, False otherwise
    """
    try:
        document = data.model_dump() if hasattr(data, 'model_dump') else data
        result = collection.update_one(
            filters,
            {"$set": document}
        )
        
        if result.modified_count > 0:
            logger.info(f"Updated document with filters {filters} in {collection.name}")
        else:
            logger.warning(f"No document found with filters {filters} in {collection.name}")
        
        return result
    except Exception as e:
        logger.error(f"Failed to update document with filters {filters} in {collection.name}: {e}")
        raise

def delete(collection: Collection, filters: Dict[str, Any]) -> bool:
    """
    Delete documents by filters
    
    Args:
        collection: MongoDB collection instance
        filters: Dictionary of field-value pairs that documents must satisfy
        
    Returns:
        True if at least one document was deleted, False otherwise
    """
    try:
        result = collection.delete_one(filters)
        
        if result.deleted_count > 0:
            logger.info(f"Deleted document with filters {filters} from {collection.name}")
        else:
            logger.warning(f"No document found with filters {filters} in {collection.name}")
        return result
    except Exception as e:
        logger.error(f"Failed to delete document with filters {filters} from {collection.name}: {e}")
        raise

def count(collection: Collection, filters: Dict[str, Any] = {}) -> int:
    """
    Count documents in the collection with optional filters
    
    Args:
        collection: MongoDB collection instance
        filters: Dictionary of field-value pairs that documents must satisfy (optional)
        
    Returns:
        Count of documents matching the filters
    """
    try:
        count = collection.count_documents(filters)
        logger.info(f"Documents matching filters {filters} in {collection.name}: {count}")
        return count
    except Exception as e:
        logger.error(f"Failed to count documents with filters {filters} in {collection.name}: {e}")
        raise

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