"""
CRUD operations for Student models
"""

import logging
from typing import Optional, List
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
from src.config import (
    MONGODB_STUDENT_PROFILES,
    MONGODB_STUDENT_PREFERENCES
)
from src.models.user.usrStudent import (
    StudentProfile,
    StudentPreference
)

# Configure logging
logger = logging.getLogger(__name__)

# =====================
# Student Profile CRUD Functions
# =====================

def get_student_profiles_collection() -> Collection:
    """Get the student profiles collection"""
    db = get_mongodb_database()
    return db[MONGODB_STUDENT_PROFILES]

def create_student_profile(profile: StudentProfile) -> any:
    """
    Create a new student profile
    
    Args:
        profile: StudentProfile model instance
        
    Returns:
        ID of the created profile
    """
    collection = get_student_profiles_collection()
    return insert(collection, profile)

def get_student_profile_by_userid(userid: int) -> Optional[StudentProfile]:
    """
    Read a student profile by userid
    
    Args:
        userid: ID of the user
        
    Returns:
        StudentProfile data if found, None otherwise
    """
    try:
        collection = get_student_profiles_collection()
        result = get_one(collection, {"userid": userid})
        result = StudentProfile(**result) if result else None
        
        return result
    except Exception as e:
        logger.error(f"Error getting student profile by userid {userid}: {e}")
        return None

def get_all_student_profiles(offset: int = 0, limit: int = 100) -> List[StudentProfile]:
    """
    Read all student profiles with pagination
    
    Args:
        offset: Number of profiles to skip (for pagination)
        limit: Maximum number of profiles to return
        
    Returns:
        List of StudentProfile objects
    """
    try:
        collection = get_student_profiles_collection()
        results = get_many(collection, {}, offset=offset, limit=limit)
        results = [StudentProfile(**result) for result in results]
        
        return results
    except Exception as e:
        logger.error(f"Error getting all student profiles: {e}")
        return []

def update_student_profile(userid: int, profile: StudentProfile) -> bool:
    """
    Update a student profile by userid
    
    Args:
        userid: ID of the user to update
        profile: Updated StudentProfile model instance
        
    Returns:
        True if profile was updated, False otherwise
    """
    collection = get_student_profiles_collection()
    return update(collection, {"userid": userid}, profile)

def delete_student_profile(userid: int) -> bool:
    """
    Delete a student profile by userid
    
    Args:
        userid: ID of the user to delete
        
    Returns:
        True if profile was deleted, False otherwise
    """
    collection = get_student_profiles_collection()
    return delete(collection, {"userid": userid})

def count_student_profiles() -> int:
    """
    Count total number of student profiles
    
    Returns:
        Total count of student profiles
    """
    collection = get_student_profiles_collection()
    return count(collection)

# =====================
# Student Preference CRUD Functions
# =====================

def get_student_preferences_collection() -> Collection:
    """Get the student preferences collection"""
    db = get_mongodb_database()
    return db[MONGODB_STUDENT_PREFERENCES]

def create_student_preference(preference: StudentPreference) -> any:
    """
    Create a new student preference
    
    Args:
        preference: StudentPreference model instance
        
    Returns:
        ID of the created preference
    """
    collection = get_student_preferences_collection()
    return insert(collection, preference)

def get_student_preference_by_userid(userid: int) -> Optional[StudentPreference]:
    """
    Read a student preference by userid
    
    Args:
        userid: ID of the user
        
    Returns:
        StudentPreference data if found, None otherwise
    """
    try:
        collection = get_student_preferences_collection()
        result = get_one(collection, {"userid": userid})
        result = StudentPreference(**result) if result else None
        
        return result
    except Exception as e:
        logger.error(f"Error getting student preference by userid {userid}: {e}")
        return None

def get_all_student_preferences(offset: int = 0, limit: int = 100) -> List[StudentPreference]:
    """
    Read all student preferences with pagination
    
    Args:
        offset: Number of preferences to skip (for pagination)
        limit: Maximum number of preferences to return
        
    Returns:
        List of StudentPreference objects
    """
    try:
        collection = get_student_preferences_collection()
        results = get_many(collection, {}, offset=offset, limit=limit)
        results = [StudentPreference(**result) for result in results]
        
        return results
    except Exception as e:
        logger.error(f"Error getting all student preferences: {e}")
        return []

def update_student_preference(userid: int, preference: StudentPreference) -> bool:
    """
    Update a student preference by userid
    
    Args:
        userid: ID of the user to update
        preference: Updated StudentPreference model instance
        
    Returns:
        True if preference was updated, False otherwise
    """
    collection = get_student_preferences_collection()
    return update(collection, {"userid": userid}, preference)

def delete_student_preference(userid: int) -> bool:
    """
    Delete a student preference by userid
    
    Args:
        userid: ID of the user to delete
        
    Returns:
        True if preference was deleted, False otherwise
    """
    collection = get_student_preferences_collection()
    return delete(collection, {"userid": userid})

def count_student_preferences() -> int:
    """
    Count total number of student preferences
    
    Returns:
        Total count of student preferences
    """
    collection = get_student_preferences_collection()
    return count(collection)
