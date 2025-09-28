"""
Clients package for Unifly Backend
Contains client initialization and management modules
"""

from .mongodb import (
    get_mongodb_client,
    get_mongodb_database,
    close_mongodb_connection,
    check_mongodb_connection,
    reconnect_mongodb,
    insert,
    get_one,
    get_many,
    update,
    delete,
    count
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

from .langchain import (
    get_langchain_embedding,
    get_langchain_qdrant,
    get_langchain_llm,
    insert_vecdb,
    delete_vecdb,
    update_vecdb
)

__all__ = [
    "get_mongodb_client", 
    "get_mongodb_database",
    "close_mongodb_connection",
    "check_mongodb_connection",
    "reconnect_mongodb",
    "insert",
    "get_one",
    "get_many",
    "update",
    "delete",
    "count",
    "get_qdrant_client",
    "create_collection",
    "delete_collection",
    "get_collection_info",
    "close_qdrant_connection",
    "check_qdrant_connection",
    "reconnect_qdrant",
    "get_langchain_embedding",
    "get_langchain_qdrant",
    "get_langchain_llm",
    "insert_vecdb",
    "delete_vecdb",
    "update_vecdb"
]
