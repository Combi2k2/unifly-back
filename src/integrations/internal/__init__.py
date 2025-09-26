"""
Clients package for Unifly Backend
Contains client initialization and management modules
"""

from .mongodb import (
    get_mongodb_client,
    get_mongodb_database,
    close_mongodb_connection,
    check_mongodb_connection,
    reconnect_mongodb
)

from .qdrant import (
    get_qdrant_client,
    create_collection,
    delete_collection,
    get_collection_info,
    close_qdrant_connection,
    check_qdrant_connection,
    reconnect_qdrant
)

__all__ = [
    "get_mongodb_client", 
    "get_mongodb_database",
    "close_mongodb_connection",
    "check_mongodb_connection",
    "reconnect_mongodb",
    "get_qdrant_client",
    "create_collection",
    "delete_collection",
    "get_collection_info",
    "close_qdrant_connection",
    "check_qdrant_connection",
    "reconnect_qdrant"
]
