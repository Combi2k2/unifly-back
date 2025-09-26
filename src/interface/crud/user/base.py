"""
CRUD operations for User and UserSession models
"""

import logging
from typing import Optional, List, Dict, Any
from pymongo.collection import Collection
from src.integrations.internal.mongodb import (
    get_mongodb_database,
    insert,
    get_one,
    get_many,
    update,
    delete,
    count
)
from src.config import MONGODB_USER_BASE
from src.models.user.base import (
    UserBase,
    UserSessionBase
)

# Configure logging
logger = logging.getLogger(__name__)

# =====================
# User CRUD Functions
# =====================

def get_users_collection() -> Collection:
    """Get the users collection"""
    db = get_mongodb_database()
    return db[MONGODB_USER_BASE]

def create_user(user: UserBase) -> Any:
    """
    Create a new user
    
    Args:
        user: UserBase model instance
        
    Returns:
        ID of the created user
    """
    collection = get_users_collection()
    return insert(collection, user)

def get_user_by_id(userid: int) -> Optional[UserBase]:
    """
    Read a user by their ID
    
    Args:
        user_id: ID of the user
        
    Returns:
        User data if found, None otherwise
    """
    try:
        collection = get_users_collection()
        result = get_one(collection, {"userid": userid})
        result = UserBase(**result) if result else None
        return result
    except Exception as e:
        logger.error(f"Error getting user by ID {userid}: {e}")
        return None

def get_user_by_email(email: str) -> Optional[UserBase]:
    """
    Read a user by their email address
    
    Args:
        email: Email address of the user
        
    Returns:
        User data if found, None otherwise
    """
    try:
        collection = get_users_collection()
        result = get_one(collection, {"email": email})
        result = UserBase(**result) if result else None
        return result
    except Exception as e:
        logger.error(f"Error getting user by email {email}: {e}")
        return None

def get_users_by_role(role: str, offset: int = 0, limit: int = 100) -> List[UserBase]:
    """
    Read users by their role
    
    Args:
        role: User role to filter by
        offset: Number of users to skip (for pagination)
        limit: Maximum number of users to return
        
    Returns:
        List of UserBase objects
    """
    try:
        collection = get_users_collection()
        results = get_many(collection, {"role": role}, offset=offset, limit=limit)
        results = [UserBase(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting users by role {role}: {e}")
        return []

def get_users_by_status(status: str, offset: int = 0, limit: int = 100) -> List[UserBase]:
    """
    Read users by their status
    
    Args:
        status: User status to filter by
        offset: Number of users to skip (for pagination)
        limit: Maximum number of users to return
        
    Returns:
        List of UserBase objects
    """
    try:
        collection = get_users_collection()
        results = get_many(collection, {"status": status}, offset=offset, limit=limit)
        results = [UserBase(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting users by status {status}: {e}")
        return []

def get_all_users(offset: int = 0, limit: int = 100) -> List[UserBase]:
    """
    Read all users with pagination
    
    Args:
        offset: Number of users to skip (for pagination)
        limit: Maximum number of users to return
        
    Returns:
        List of UserBase objects
    """
    try:
        collection = get_users_collection()
        results = get_many(collection, {}, offset=offset, limit=limit)
        results = [UserBase(**result) for result in results]
        return results
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []

def update_user(userid: int, user: UserBase) -> bool:
    """
    Update a user by their ID
    
    Args:
        userid: ID of the user to update
        user: Updated UserBase model instance
        
    Returns:
        True if user was updated, False otherwise
    """
    collection = get_users_collection()
    return update(collection, {"userid": userid}, user)

def update_user_status(userid: int, status: str) -> bool:
    """
    Update only the status of a user
    
    Args:
        userid: ID of the user to update
        status: New status value
        
    Returns:
        True if user was updated, False otherwise
    """
    collection = get_users_collection()
    return update(collection, {"userid": userid}, {"status": status})

def delete_user(userid: int) -> bool:
    """
    Delete a user by their ID
    
    Args:
        userid: ID of the user to delete
        
    Returns:
        True if user was deleted, False otherwise
    """
    collection = get_users_collection()
    return delete(collection, {"userid": userid})

def count_users() -> int:
    """
    Count total number of users
    
    Returns:
        Total count of users
    """
    collection = get_users_collection()
    return count(collection)

def count_users_by_role(role: str) -> int:
    """
    Count users by role
    
    Args:
        role: User role to count
        
    Returns:
        Count of users with the specified role
    """
    collection = get_users_collection()
    return collection.count_documents({"role": role})

def count_users_by_status(status: str) -> int:
    """
    Count users by status
    
    Args:
        status: User status to count
        
    Returns:
        Count of users with the specified status
    """
    collection = get_users_collection()
    return collection.count_documents({"status": status})

# # =====================
# # User Session CRUD Functions
# # =====================

# def get_user_sessions_collection() -> Collection:
#     """Get the user sessions collection"""
#     db = get_mongodb_database()
#     return db[f"{MONGODB_USER_BASE}_sessions"]

# def create_user_session(user_session: UserSessionBase, user_id: int) -> Any:
#     """
#     Create a new user session
    
#     Args:
#         user_session: UserSessionBase model instance
#         user_id: ID of the user this session belongs to
        
#     Returns:
#         ID of the created session
#     """
#     collection = get_user_sessions_collection()
#     session_data = user_session.model_dump()
#     session_data["user_id"] = user_id
#     return create(collection, session_data)

# def read_user_session_by_id(sessionid: str) -> Optional[Dict[str, Any]]:
#     """
#     Read a user session by its ID
    
#     Args:
#         sessionid: ID of the session
        
#     Returns:
#         Session data if found, None otherwise
#     """
#     collection = get_user_sessions_collection()
#     return get_one(collection, sessionid)

# def read_user_sessions_by_user_id(userid: int, offset: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
#     """
#     Read all sessions for a specific user
    
#     Args:
#         userid: ID of the user
#         offset: Number of sessions to skip (for pagination)
#         limit: Maximum number of sessions to return
        
#     Returns:
#         List of session data dictionaries
#     """
#     collection = get_user_sessions_collection()
#     return get_many(collection, {"user_id": userid}, offset=offset, limit=limit)

# def read_active_user_sessions(user_id: int) -> List[Dict[str, Any]]:
#     """
#     Read active sessions for a specific user
    
#     Args:
#         userid: ID of the user
        
#     Returns:
#         List of active session data dictionaries
#     """
#     collection = get_user_sessions_collection()
#     return get_many(collection, {"user_id": userid, "active": True})

# def update_user_session(sessionid: str, session_data: Dict[str, Any]) -> bool:
#     """
#     Update a user session
    
#     Args:
#         session_id: ID of the session to update
#         session_data: Dictionary containing session fields to update
        
#     Returns:
#         True if session was updated, False otherwise
#     """
#     collection = get_user_sessions_collection()
#     return update(collection, session_id, session_data)

# def delete_user_session(session_id: str) -> bool:
#     """
#     Delete a user session by its ID
    
#     Args:
#         session_id: ID of the session to delete
        
#     Returns:
#         True if session was deleted, False otherwise
#     """
#     collection = get_user_sessions_collection()
#     return delete(collection, session_id)

# def delete_user_sessions_by_user_id(user_id: int) -> int:
#     """
#     Delete all sessions for a specific user
    
#     Args:
#         user_id: ID of the user
        
#     Returns:
#         Number of sessions deleted
#     """
#     collection = get_user_sessions_collection()
#     result = collection.delete_many({"user_id": user_id})
#     logger.info(f"Deleted {result.deleted_count} sessions for user {user_id}")
#     return result.deleted_count

# def count_user_sessions(user_id: int) -> int:
#     """
#     Count sessions for a specific user
    
#     Args:
#         user_id: ID of the user
        
#     Returns:
#         Count of sessions for the user
#     """
#     collection = get_user_sessions_collection()
#     return collection.count_documents({"user_id": user_id})

# # =====================
# # Utility Functions
# # =====================

# def search_users(search_term: str, offset: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
#     """
#     Search users by name or email
    
#     Args:
#         search_term: Term to search for in names or email
#         offset: Number of users to skip (for pagination)
#         limit: Maximum number of users to return
        
#     Returns:
#         List of matching user data dictionaries
#     """
#     collection = get_users_collection()
#     # Create regex pattern for case-insensitive search
#     search_pattern = {"$regex": search_term, "$options": "i"}
#     filters = {
#         "$or": [
#             {"first_name": search_pattern},
#             {"last_name": search_pattern},
#             {"email": search_pattern}
#         ]
#     }
#     return get_many(collection, filters, offset=offset, limit=limit)

# def get_user_statistics() -> Dict[str, int]:
#     """
#     Get user statistics by role and status
    
#     Returns:
#         Dictionary containing counts by role and status
#     """
#     collection = get_users_collection()
    
#     stats = {
#         "total_users": count_users(),
#         "by_role": {},
#         "by_status": {}
#     }
    
#     # Count by role
#     for role in ["student", "advisor", "parent", "admin"]:
#         stats["by_role"][role] = count_users_by_role(role)
    
#     # Count by status
#     for status in ["active", "inactive", "suspended", "verifying"]:
#         stats["by_status"][status] = count_users_by_status(status)
    
#     return stats
