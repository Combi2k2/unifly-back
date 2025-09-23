"""
MongoDB Repository for Student Data
Handles interactions with MongoDB database for student profiles and preferences
"""

import logging
from typing import Optional, List
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError

from models.student import (
    StudentProfile,
    StudentPreference
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StudentRepository:
    """Repository class to handle interactions with the MongoDB database for student data"""
    
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
            
            # Initialize student-profile collection
            if "student-profile" not in existing_collections:
                self.db.create_collection("student-profile")
                logger.info("Created student-profile collection")
            
            # Initialize student-preference collection
            if "student-preference" not in existing_collections:
                self.db.create_collection("student-preference")
                logger.info("Created student-preference collection")
            
            # Create basic indexes
            self.db["student-profile"].create_index([("userid", ASCENDING)], unique=True)
            self.db["student-preference"].create_index([("userid", ASCENDING)], unique=True)
            
            self.profile_collection = self.db["student-profile"]
            self.preference_collection = self.db["student-preference"]
            
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
    
    # ==================== Student Profile Methods ====================
    
    def upsert_student_profile(self, profile: StudentProfile) -> int:
        """
        Insert or update a student profile
        
        Args:
            profile: StudentProfile object to upsert
            
        Returns:
            userid of the upserted profile
            
        Raises:
            Exception: If upsert operation fails
        """
        try:
            result = self.profile_collection.update_one(
                {"userid": profile.userid},
                {"$set": profile.model_dump()},
                upsert=True
            )
            
            if result.upserted_id or result.modified_count > 0:
                logger.info(f"Successfully upserted profile for userid: {profile.userid}")
                return profile.userid
            else:
                logger.warning(f"No changes made to profile for userid: {profile.userid}")
                return profile.userid
                
        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error for userid {profile.userid}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to upsert profile for userid {profile.userid}: {e}")
            raise
    
    def remove_student_profile(self, userid: int) -> bool:
        """
        Remove a student profile
        
        Args:
            userid: User ID of the profile to remove
            
        Returns:
            True if profile was removed, False otherwise
        """
        try:
            result = self.profile_collection.delete_one({"userid": userid})
            success = result.deleted_count > 0
            
            if success:
                logger.info(f"Successfully removed profile for userid: {userid}")
            else:
                logger.warning(f"No profile found to remove for userid: {userid}")
                
            return success
            
        except Exception as e:
            logger.error(f"Failed to remove profile for userid {userid}: {e}")
            return False
    
    def get_student_profile(self, userid: int) -> Optional[StudentProfile]:
        """
        Get a student profile by userid
        
        Args:
            userid: User ID to search for
            
        Returns:
            StudentProfile object if found, None otherwise
        """
        try:
            result = self.profile_collection.find_one({"userid": userid})
            
            if result:
                result.pop("_id", None)  # Remove MongoDB's _id field
                return StudentProfile(**result)
            
            logger.info(f"No profile found for userid: {userid}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get profile for userid {userid}: {e}")
            return None
    
    def get_all_student_profiles(self) -> List[StudentProfile]:
        """
        Get all student profiles
        
        Returns:
            List of StudentProfile objects
        """
        try:
            profiles = []
            for profile_dict in self.profile_collection.find():
                profile_dict.pop("_id", None)
                profiles.append(StudentProfile(**profile_dict))
            
            logger.info(f"Retrieved {len(profiles)} student profiles")
            return profiles
            
        except Exception as e:
            logger.error(f"Failed to get all profiles: {e}")
            return []
    
    # ==================== Student Preference Methods ====================
    
    def upsert_student_preference(self, preference: StudentPreference) -> int:
        """
        Insert or update a student preference
        
        Args:
            preference: StudentPreference object to upsert
            
        Returns:
            userid of the upserted preference
            
        Raises:
            Exception: If upsert operation fails
        """
        try:
            result = self.preference_collection.update_one(
                {"userid": preference.userid},
                {"$set": preference.model_dump()},
                upsert=True
            )
            
            if result.upserted_id or result.modified_count > 0:
                logger.info(f"Successfully upserted preference for userid: {preference.userid}")
                return preference.userid
            else:
                logger.warning(f"No changes made to preference for userid: {preference.userid}")
                return preference.userid
                
        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error for userid {preference.userid}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to upsert preference for userid {preference.userid}: {e}")
            raise
    
    def remove_student_preference(self, userid: int) -> bool:
        """
        Remove a student preference
        
        Args:
            userid: User ID of the preference to remove
            
        Returns:
            True if preference was removed, False otherwise
        """
        try:
            result = self.preference_collection.delete_one({"userid": userid})
            success = result.deleted_count > 0
            
            if success:
                logger.info(f"Successfully removed preference for userid: {userid}")
            else:
                logger.warning(f"No preference found to remove for userid: {userid}")
                
            return success
            
        except Exception as e:
            logger.error(f"Failed to remove preference for userid {userid}: {e}")
            return False
    
    def get_student_preference(self, userid: int) -> Optional[StudentPreference]:
        """
        Get a student preference by userid
        
        Args:
            userid: User ID to search for
            
        Returns:
            StudentPreference object if found, None otherwise
        """
        try:
            result = self.preference_collection.find_one({"userid": userid})
            
            if result:
                result.pop("_id", None)  # Remove MongoDB's _id field
                return StudentPreference(**result)
            
            logger.info(f"No preference found for userid: {userid}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get preference for userid {userid}: {e}")
            return None
    
    def get_all_student_preferences(self) -> List[StudentPreference]:
        """
        Get all student preferences
        
        Returns:
            List of StudentPreference objects
        """
        try:
            preferences = []
            for preference_dict in self.preference_collection.find():
                preference_dict.pop("_id", None)
                preferences.append(StudentPreference(**preference_dict))
            
            logger.info(f"Retrieved {len(preferences)} student preferences")
            return preferences
            
        except Exception as e:
            logger.error(f"Failed to get all preferences: {e}")
            return []
    
    # ==================== Combined Methods ====================
    
    def get_complete_student_data(self, userid: int):
        """
        Get both profile and preference data for a student
        
        Args:
            userid: User ID to search for
            
        Returns:
            Tuple of (profile, preference) or (None, None) if not found
        """
        try:
            profile = self.get_student_profile(userid)
            preference = self.get_student_preference(userid)
            return profile, preference
            
        except Exception as e:
            logger.error(f"Failed to get complete student data for userid {userid}: {e}")
            return None, None
    
    def remove_complete_student_data(self, userid: int) -> bool:
        """
        Remove both profile and preference data for a student
        
        Args:
            userid: User ID of the data to remove
            
        Returns:
            True if both removals were successful, False otherwise
        """
        try:
            profile_removed = self.remove_student_profile(userid)
            preference_removed = self.remove_student_preference(userid)
            
            success = profile_removed and preference_removed
            logger.info(f"Complete removal for userid {userid}: {success}")
            return success
            
        except Exception as e:
            logger.error(f"Failed to remove complete student data for userid {userid}: {e}")
            return False
