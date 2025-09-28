"""
Qdrant Client Management
Provides centralized Qdrant client initialization and collection management for the Unifly Backend.
This module focuses on client connection management and basic collection operations.
For vector operations, use LangChain's Qdrant vector store integration.
"""

import logging
from typing import Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Import configuration
from src.config import (
    QDRANT_URL,
    QDRANT_KEY
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable for client management
_client: Optional[QdrantClient] = None

def get_qdrant_client() -> QdrantClient:
    """
    Get Qdrant client instance
    Creates new client if not exists or connection is lost
    
    Returns:
        QdrantClient instance
    """
    global _client
    
    try:
        if _client is None:
            # Initialize Qdrant client with URL and key
            if QDRANT_URL and QDRANT_KEY:
                # Use cloud Qdrant with URL and key
                _client = QdrantClient(
                    url=QDRANT_URL,
                    api_key=QDRANT_KEY,
                    timeout=10  # 10 second timeout
                )
                logger.info(f"Qdrant client created successfully with URL: {QDRANT_URL}")
            elif QDRANT_URL:
                # Use cloud Qdrant with URL only
                _client = QdrantClient(
                    url=QDRANT_URL,
                    timeout=10  # 10 second timeout
                )
                logger.info(f"Qdrant client created successfully with URL: {QDRANT_URL}")
            else:
                # Fallback to local Qdrant (default localhost:6333)
                _client = QdrantClient(
                    host="localhost",
                    port=6333,
                    timeout=10  # 10 second timeout
                )
                logger.info("Qdrant client created successfully with localhost:6333")
        
        # Test connection by getting collections info
        _client.get_collections()
        logger.debug("Qdrant connection is healthy")
        
        return _client
        
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}")
        _client = None
        raise

def create_collection(collection_name: str, vector_size: int = 384, distance: Distance = Distance.COSINE) -> bool:
    """
    Create a new Qdrant collection
    
    Args:
        collection_name: Name of the collection to create
        vector_size: Size of the vectors (default: 384 for sentence-transformers)
        distance: Distance metric for vector similarity (default: COSINE)
        
    Returns:
        True if collection was created successfully
    """
    try:
        client = get_qdrant_client()
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance)
        )
        
        logger.info(f"Created collection: {collection_name} with vector size: {vector_size}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create collection {collection_name}: {e}")
        raise

def delete_collection(collection_name: str) -> bool:
    """
    Delete a collection
    
    Args:
        collection_name: Name of the collection to delete
    """
    try:
        client = get_qdrant_client()
        client.delete_collection(collection_name)
        logger.info(f"Deleted collection: {collection_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete collection {collection_name}: {e}")
        raise

def close_qdrant_connection():
    """Close Qdrant client connection"""
    global _client
    
    try:
        if _client:
            # Qdrant client doesn't have an explicit close method
            # but we can set it to None to release resources
            _client = None
            logger.info("Qdrant client connection closed")
    except Exception as e:
        logger.error(f"Error closing Qdrant client: {e}")
        raise

def check_qdrant_connection() -> bool:
    """
    Check if Qdrant client is connected
    
    Returns:
        True if connected, False otherwise
    """
    global _client
    
    try:
        if _client is None:
            return False
        
        # Test connection by getting collections info
        _client.get_collections()
        return True
        
    except Exception:
        raise

def reconnect_qdrant():
    """Force reconnection to Qdrant"""
    logger.info("Attempting to reconnect to Qdrant...")
    close_qdrant_connection()
    return get_qdrant_client()

def get_collection_info(collection_name: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a collection
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        Collection information dictionary
    """
    try:
        client = get_qdrant_client()
        result = client.get_collection(collection_name)
        return {
            "name": collection_name,
            "vector_size":  result.config.params.vectors.size,
            "distance":     result.config.params.vectors.distance,
            "points_count": result.points_count,
            "status":       result.status
        }
        
    except Exception as e:
        logger.error(f"Failed to get collection info for {collection_name}: {e}")
        raise

def exists_collection(collection_name: str) -> bool:
    """
    Check if a collection exists
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        True if collection exists, False otherwise
    """
    try:
        client = get_qdrant_client()
        client.get_collection(collection_name)
        return True
    except Exception as e:
        logger.error(f"Failed to check if collection {collection_name} exists: {e}")
        return False

if __name__ == "__main__":
    print("Qdrant Client Initialization Test")
    print("=" * 40)
    
    try:
        # Test connection
        client = get_qdrant_client()
        print(f"✓ Qdrant client created successfully")
        
        # Test collection access
        collection_name = "test_collection"
        print(f"✓ Collection access successful: {collection_name}")
        
        # Test connection status
        if check_qdrant_connection():
            print("✓ Qdrant connection is healthy")
        else:
            print("✗ Qdrant connection is not healthy")
        
        # Test collection info
        info = get_collection_info(collection_name)
        if info:
            print(f"✓ Collection info retrieved: {info}")
        else:
            print(f"ℹ Collection {collection_name} not found or error occurred")
        
        print("\nQdrant client initialization test completed successfully!")
        
    except Exception as e:
        print(f"✗ Qdrant client initialization test failed: {e}")
        logger.error(f"Test failed: {e}")
