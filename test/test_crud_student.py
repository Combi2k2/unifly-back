"""
Test suite for Student CRUD operations
Tests all student-related CRUD functions in interface/crud/user/usrStudent.py
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pymongo.collection import Collection

# Import the specific functions we need
from src.interface.crud.user.usrStudent import (
    get_student_profiles_collection,
    create_student_profile,
    get_student_profile_by_userid,
    get_all_student_profiles,
    update_student_profile,
    delete_student_profile,
    count_student_profiles,
    get_student_preferences_collection,
    create_student_preference,
    get_student_preference_by_userid,
    get_all_student_preferences,
    update_student_preference,
    delete_student_preference,
    count_student_preferences
)
from src.integrations.internal.mongodb import get_one, get_many, insert, update, delete, count
from src.models.user.usrStudent import (
    StudentProfile,
    StudentPreference,
    Education,
    Experience,
    Award,
    ExtraCurricular,
    StandardizedTest
)


class TestStudentProfileCRUD:
    """Test Student Profile CRUD operations"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create mock collection
        self.mock_collection = Mock(spec=Collection)
        self.mock_collection.name = "student_profiles"
        
        # Sample education data
        self.sample_education = Education(
            name="Harvard University",
            period="09/18-06/22",
            gpa=3.8,
            degree="Bachelor of Science",
            major="Computer Science"
        )
        
        # Sample experience data
        self.sample_experience = Experience(
            name="Software Engineer Intern at Google",
            period="06/21-08/21",
            desc="Developed web applications using React and Node.js"
        )
        
        # Sample award data
        self.sample_award = Award(
            name="National Science Olympiad",
            desc="First place in Computer Science category",
            date="03/22"
        )
        
        # Sample extracurricular data
        self.sample_activity = ExtraCurricular(
            name="President of Computer Science Club",
            period="09/20-06/22",
            desc="Led weekly meetings and organized coding competitions"
        )
        
        # Sample standardized test data
        self.sample_test = StandardizedTest(
            name="SAT",
            score=1450,
            date="12/20"
        )
        
        # Sample student profile data
        self.sample_profile_data = {
            "userid": 12345,
            "gender": "Male",
            "overview": "Passionate computer science student with strong programming skills",
            "educations": [self.sample_education.model_dump()],
            "experience": [self.sample_experience.model_dump()],
            "activities": [self.sample_activity.model_dump()],
            "standardized_tests": [self.sample_test.model_dump()],
            "awards": [self.sample_award.model_dump()],
            "others": "Additional information about the student"
        }
        
        self.sample_profile = StudentProfile(**self.sample_profile_data)
    
    @patch('src.interface.crud.user.usrStudent.get_mongodb_database')
    def test_get_student_profiles_collection(self, mock_get_database):
        """Test getting student profiles collection"""
        # Mock database
        mock_database = Mock()
        mock_database.__getitem__ = Mock(return_value=self.mock_collection)
        mock_get_database.return_value = mock_database
        
        # Test collection access
        collection = get_student_profiles_collection()
        
        # Assertions
        assert collection == self.mock_collection
        mock_get_database.assert_called_once()
        mock_database.__getitem__.assert_called_once_with("unifly_student_profiles")
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.insert')
    def test_create_student_profile_success(self, mock_insert, mock_get_collection):
        """Test successful student profile creation"""
        # Mock collection and insert
        mock_get_collection.return_value = self.mock_collection
        mock_insert.return_value = "profile_id_123"
        
        # Test profile creation
        result = create_student_profile(self.sample_profile)
        
        # Assertions
        assert result == "profile_id_123"
        mock_get_collection.assert_called_once()
        mock_insert.assert_called_once_with(self.mock_collection, self.sample_profile)
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.insert')
    def test_create_student_profile_failure(self, mock_insert, mock_get_collection):
        """Test student profile creation failure"""
        # Mock collection and insert failure
        mock_get_collection.return_value = self.mock_collection
        mock_insert.side_effect = Exception("Database error")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Database error"):
            create_student_profile(self.sample_profile)
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.get_one')
    def test_get_student_profile_by_userid_success(self, mock_get_one, mock_get_collection):
        """Test successful student profile retrieval by userid"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.return_value = self.sample_profile_data
        
        # Test profile retrieval
        result = get_student_profile_by_userid(12345)
        
        # Assertions
        assert isinstance(result, StudentProfile)
        assert result.userid == self.sample_profile_data["userid"]
        assert result.gender == self.sample_profile_data["gender"]
        assert result.overview == self.sample_profile_data["overview"]
        mock_get_collection.assert_called_once()
        mock_get_one.assert_called_once_with(self.mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.get_one')
    def test_get_student_profile_by_userid_not_found(self, mock_get_one, mock_get_collection):
        """Test student profile retrieval by userid when not found"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.return_value = None
        
        # Test profile retrieval
        result = get_student_profile_by_userid(99999)
        
        # Assertions
        assert result is None
        mock_get_one.assert_called_once_with(self.mock_collection, {"userid": 99999})
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.get_one')
    def test_get_student_profile_by_userid_exception(self, mock_get_one, mock_get_collection):
        """Test student profile retrieval by userid with exception"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.side_effect = Exception("Database error")
        
        # Test profile retrieval
        result = get_student_profile_by_userid(12345)
        
        # Assertions
        assert result is None
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.get_many')
    def test_get_all_student_profiles_success(self, mock_get_many, mock_get_collection):
        """Test successful retrieval of all student profiles"""
        # Mock collection and get_many
        mock_get_collection.return_value = self.mock_collection
        mock_profiles = [self.sample_profile_data, {**self.sample_profile_data, "userid": 12346}]
        mock_get_many.return_value = mock_profiles
        
        # Test profiles retrieval
        result = get_all_student_profiles(offset=0, limit=10)
        
        # Assertions
        assert len(result) == 2
        assert all(isinstance(profile, StudentProfile) for profile in result)
        assert result[0].userid == 12345
        assert result[1].userid == 12346
        mock_get_collection.assert_called_once()
        mock_get_many.assert_called_once_with(self.mock_collection, {}, offset=0, limit=10)
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.get_many')
    def test_get_all_student_profiles_exception(self, mock_get_many, mock_get_collection):
        """Test retrieval of all student profiles with exception"""
        # Mock collection and get_many
        mock_get_collection.return_value = self.mock_collection
        mock_get_many.side_effect = Exception("Database error")
        
        # Test profiles retrieval
        result = get_all_student_profiles(offset=0, limit=10)
        
        # Assertions
        assert result == []
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.update')
    def test_update_student_profile_success(self, mock_update, mock_get_collection):
        """Test successful student profile update"""
        # Mock collection and update
        mock_get_collection.return_value = self.mock_collection
        mock_update.return_value = True
        
        # Test profile update
        result = update_student_profile(12345, self.sample_profile)
        
        # Assertions
        assert result is True
        mock_get_collection.assert_called_once()
        mock_update.assert_called_once_with(self.mock_collection, {"userid": 12345}, self.sample_profile)
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.update')
    def test_update_student_profile_failure(self, mock_update, mock_get_collection):
        """Test student profile update failure"""
        # Mock collection and update
        mock_get_collection.return_value = self.mock_collection
        mock_update.return_value = False
        
        # Test profile update
        result = update_student_profile(12345, self.sample_profile)
        
        # Assertions
        assert result is False
        mock_update.assert_called_once_with(self.mock_collection, {"userid": 12345}, self.sample_profile)
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.delete')
    def test_delete_student_profile_success(self, mock_delete, mock_get_collection):
        """Test successful student profile deletion"""
        # Mock collection and delete
        mock_get_collection.return_value = self.mock_collection
        mock_delete.return_value = True
        
        # Test profile deletion
        result = delete_student_profile(12345)
        
        # Assertions
        assert result is True
        mock_get_collection.assert_called_once()
        mock_delete.assert_called_once_with(self.mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.delete')
    def test_delete_student_profile_failure(self, mock_delete, mock_get_collection):
        """Test student profile deletion failure"""
        # Mock collection and delete
        mock_get_collection.return_value = self.mock_collection
        mock_delete.return_value = False
        
        # Test profile deletion
        result = delete_student_profile(12345)
        
        # Assertions
        assert result is False
        mock_delete.assert_called_once_with(self.mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.count')
    def test_count_student_profiles_success(self, mock_count, mock_get_collection):
        """Test successful student profile count"""
        # Mock collection and count
        mock_get_collection.return_value = self.mock_collection
        mock_count.return_value = 25
        
        # Test profile count
        result = count_student_profiles()
        
        # Assertions
        assert result == 25
        mock_get_collection.assert_called_once()
        mock_count.assert_called_once_with(self.mock_collection)


class TestStudentPreferenceCRUD:
    """Test Student Preference CRUD operations"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create mock collection
        self.mock_collection = Mock(spec=Collection)
        self.mock_collection.name = "student_preferences"
        
        # Sample student preference data
        self.sample_preference_data = {
            "userid": 12345,
            "intended_major": ["Computer Science", "Data Science"],
            "intended_degree": ["Bachelor of Science", "Master of Science"],
            "preferred_countries": ["United States", "Canada"],
            "preferred_cities": ["San Francisco", "New York"],
            "budget_min": 20000,
            "budget_max": 50000,
            "others": "Looking for universities with strong research programs"
        }
        
        self.sample_preference = StudentPreference(**self.sample_preference_data)
    
    @patch('src.interface.crud.user.usrStudent.get_mongodb_database')
    def test_get_student_preferences_collection(self, mock_get_database):
        """Test getting student preferences collection"""
        # Mock database
        mock_database = Mock()
        mock_database.__getitem__ = Mock(return_value=self.mock_collection)
        mock_get_database.return_value = mock_database
        
        # Test collection access
        collection = get_student_preferences_collection()
        
        # Assertions
        assert collection == self.mock_collection
        mock_get_database.assert_called_once()
        mock_database.__getitem__.assert_called_once_with("unifly_student_preferences")
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.insert')
    def test_create_student_preference_success(self, mock_insert, mock_get_collection):
        """Test successful student preference creation"""
        # Mock collection and insert
        mock_get_collection.return_value = self.mock_collection
        mock_insert.return_value = "preference_id_123"
        
        # Test preference creation
        result = create_student_preference(self.sample_preference)
        
        # Assertions
        assert result == "preference_id_123"
        mock_get_collection.assert_called_once()
        mock_insert.assert_called_once_with(self.mock_collection, self.sample_preference)
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.insert')
    def test_create_student_preference_failure(self, mock_insert, mock_get_collection):
        """Test student preference creation failure"""
        # Mock collection and insert failure
        mock_get_collection.return_value = self.mock_collection
        mock_insert.side_effect = Exception("Database error")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Database error"):
            create_student_preference(self.sample_preference)
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.get_one')
    def test_get_student_preference_by_userid_success(self, mock_get_one, mock_get_collection):
        """Test successful student preference retrieval by userid"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.return_value = self.sample_preference_data
        
        # Test preference retrieval
        result = get_student_preference_by_userid(12345)
        
        # Assertions
        assert isinstance(result, StudentPreference)
        assert result.userid == self.sample_preference_data["userid"]
        assert result.intended_major == self.sample_preference_data["intended_major"]
        assert result.budget_min == self.sample_preference_data["budget_min"]
        mock_get_collection.assert_called_once()
        mock_get_one.assert_called_once_with(self.mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.get_one')
    def test_get_student_preference_by_userid_not_found(self, mock_get_one, mock_get_collection):
        """Test student preference retrieval by userid when not found"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.return_value = None
        
        # Test preference retrieval
        result = get_student_preference_by_userid(99999)
        
        # Assertions
        assert result is None
        mock_get_one.assert_called_once_with(self.mock_collection, {"userid": 99999})
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.get_one')
    def test_get_student_preference_by_userid_exception(self, mock_get_one, mock_get_collection):
        """Test student preference retrieval by userid with exception"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.side_effect = Exception("Database error")
        
        # Test preference retrieval
        result = get_student_preference_by_userid(12345)
        
        # Assertions
        assert result is None
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.get_many')
    def test_get_all_student_preferences_success(self, mock_get_many, mock_get_collection):
        """Test successful retrieval of all student preferences"""
        # Mock collection and get_many
        mock_get_collection.return_value = self.mock_collection
        mock_preferences = [self.sample_preference_data, {**self.sample_preference_data, "userid": 12346}]
        mock_get_many.return_value = mock_preferences
        
        # Test preferences retrieval
        result = get_all_student_preferences(offset=0, limit=10)
        
        # Assertions
        assert len(result) == 2
        assert all(isinstance(preference, StudentPreference) for preference in result)
        assert result[0].userid == 12345
        assert result[1].userid == 12346
        mock_get_collection.assert_called_once()
        mock_get_many.assert_called_once_with(self.mock_collection, {}, offset=0, limit=10)
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.get_many')
    def test_get_all_student_preferences_exception(self, mock_get_many, mock_get_collection):
        """Test retrieval of all student preferences with exception"""
        # Mock collection and get_many
        mock_get_collection.return_value = self.mock_collection
        mock_get_many.side_effect = Exception("Database error")
        
        # Test preferences retrieval
        result = get_all_student_preferences(offset=0, limit=10)
        
        # Assertions
        assert result == []
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.update')
    def test_update_student_preference_success(self, mock_update, mock_get_collection):
        """Test successful student preference update"""
        # Mock collection and update
        mock_get_collection.return_value = self.mock_collection
        mock_update.return_value = True
        
        # Test preference update
        result = update_student_preference(12345, self.sample_preference)
        
        # Assertions
        assert result is True
        mock_get_collection.assert_called_once()
        mock_update.assert_called_once_with(self.mock_collection, {"userid": 12345}, self.sample_preference)
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.update')
    def test_update_student_preference_failure(self, mock_update, mock_get_collection):
        """Test student preference update failure"""
        # Mock collection and update
        mock_get_collection.return_value = self.mock_collection
        mock_update.return_value = False
        
        # Test preference update
        result = update_student_preference(12345, self.sample_preference)
        
        # Assertions
        assert result is False
        mock_update.assert_called_once_with(self.mock_collection, {"userid": 12345}, self.sample_preference)
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.delete')
    def test_delete_student_preference_success(self, mock_delete, mock_get_collection):
        """Test successful student preference deletion"""
        # Mock collection and delete
        mock_get_collection.return_value = self.mock_collection
        mock_delete.return_value = True
        
        # Test preference deletion
        result = delete_student_preference(12345)
        
        # Assertions
        assert result is True
        mock_get_collection.assert_called_once()
        mock_delete.assert_called_once_with(self.mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.delete')
    def test_delete_student_preference_failure(self, mock_delete, mock_get_collection):
        """Test student preference deletion failure"""
        # Mock collection and delete
        mock_get_collection.return_value = self.mock_collection
        mock_delete.return_value = False
        
        # Test preference deletion
        result = delete_student_preference(12345)
        
        # Assertions
        assert result is False
        mock_delete.assert_called_once_with(self.mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.count')
    def test_count_student_preferences_success(self, mock_count, mock_get_collection):
        """Test successful student preference count"""
        # Mock collection and count
        mock_get_collection.return_value = self.mock_collection
        mock_count.return_value = 15
        
        # Test preference count
        result = count_student_preferences()
        
        # Assertions
        assert result == 15
        mock_get_collection.assert_called_once()
        mock_count.assert_called_once_with(self.mock_collection)


class TestStudentCRUDIntegration:
    """Integration tests for Student CRUD operations"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Sample education data
        self.sample_education = Education(
            name="MIT",
            period="09/20-06/24",
            gpa=3.9,
            degree="Bachelor of Science",
            major="Computer Science"
        )
        
        # Sample student profile data
        self.sample_profile_data = {
            "userid": 12345,
            "gender": "Female",
            "overview": "Aspiring data scientist with passion for machine learning",
            "educations": [self.sample_education.model_dump()],
            "experience": [],
            "activities": [],
            "standardized_tests": [],
            "awards": [],
            "others": "Research experience in AI"
        }
        
        # Sample student preference data
        self.sample_preference_data = {
            "userid": 12345,
            "intended_major": ["Data Science", "Machine Learning"],
            "intended_degree": ["Master of Science", "PhD"],
            "preferred_countries": ["United States"],
            "preferred_cities": ["Boston", "San Francisco"],
            "budget_min": 30000,
            "budget_max": 60000,
            "others": "Looking for research-focused programs"
        }
        
        self.sample_profile = StudentProfile(**self.sample_profile_data)
        self.sample_preference = StudentPreference(**self.sample_preference_data)
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.insert')
    @patch('src.interface.crud.user.usrStudent.get_one')
    @patch('src.interface.crud.user.usrStudent.update')
    @patch('src.interface.crud.user.usrStudent.delete')
    def test_full_student_profile_crud_workflow(self, mock_delete, mock_update, mock_get_one, mock_insert, mock_get_collection):
        """Test complete student profile CRUD workflow"""
        # Mock collection
        mock_collection = Mock(spec=Collection)
        mock_collection.name = "student_profiles"
        mock_get_collection.return_value = mock_collection
        
        # Mock responses
        mock_insert.return_value = "profile_id_123"
        mock_get_one.return_value = self.sample_profile_data
        mock_update.return_value = True
        mock_delete.return_value = True
        
        # Test workflow
        # 1. Create profile
        profile_id = create_student_profile(self.sample_profile)
        assert profile_id == "profile_id_123"
        mock_insert.assert_called_once_with(mock_collection, self.sample_profile)
        
        # 2. Get profile by userid
        profile = get_student_profile_by_userid(12345)
        assert isinstance(profile, StudentProfile)
        assert profile.userid == self.sample_profile_data["userid"]
        mock_get_one.assert_called_once_with(mock_collection, {"userid": 12345})
        
        # 3. Update profile
        updated_profile = StudentProfile(**{**self.sample_profile_data, "overview": "Updated overview"})
        update_success = update_student_profile(12345, updated_profile)
        assert update_success is True
        mock_update.assert_called_once_with(mock_collection, {"userid": 12345}, updated_profile)
        
        # 4. Delete profile
        delete_success = delete_student_profile(12345)
        assert delete_success is True
        mock_delete.assert_called_once_with(mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.insert')
    @patch('src.interface.crud.user.usrStudent.get_one')
    @patch('src.interface.crud.user.usrStudent.update')
    @patch('src.interface.crud.user.usrStudent.delete')
    def test_full_student_preference_crud_workflow(self, mock_delete, mock_update, mock_get_one, mock_insert, mock_get_collection):
        """Test complete student preference CRUD workflow"""
        # Mock collection
        mock_collection = Mock(spec=Collection)
        mock_collection.name = "student_preferences"
        mock_get_collection.return_value = mock_collection
        
        # Mock responses
        mock_insert.return_value = "preference_id_123"
        mock_get_one.return_value = self.sample_preference_data
        mock_update.return_value = True
        mock_delete.return_value = True
        
        # Test workflow
        # 1. Create preference
        preference_id = create_student_preference(self.sample_preference)
        assert preference_id == "preference_id_123"
        mock_insert.assert_called_once_with(mock_collection, self.sample_preference)
        
        # 2. Get preference by userid
        preference = get_student_preference_by_userid(12345)
        assert isinstance(preference, StudentPreference)
        assert preference.userid == self.sample_preference_data["userid"]
        mock_get_one.assert_called_once_with(mock_collection, {"userid": 12345})
        
        # 3. Update preference
        updated_preference = StudentPreference(**{**self.sample_preference_data, "budget_max": 70000})
        update_success = update_student_preference(12345, updated_preference)
        assert update_success is True
        mock_update.assert_called_once_with(mock_collection, {"userid": 12345}, updated_preference)
        
        # 4. Delete preference
        delete_success = delete_student_preference(12345)
        assert delete_success is True
        mock_delete.assert_called_once_with(mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.get_many')
    def test_student_profile_search_workflow(self, mock_get_many, mock_get_collection):
        """Test student profile search and filtering workflow"""
        # Mock collection
        mock_collection = Mock(spec=Collection)
        mock_get_collection.return_value = mock_collection
        
        # Mock search results
        mock_profiles = [
            {**self.sample_profile_data, "userid": 12345},
            {**self.sample_profile_data, "userid": 12346, "gender": "Male"}
        ]
        mock_get_many.return_value = mock_profiles
        
        # Test get all profiles
        all_profiles = get_all_student_profiles(offset=0, limit=10)
        assert len(all_profiles) == 2
        assert all(isinstance(profile, StudentProfile) for profile in all_profiles)
        mock_get_many.assert_called_with(mock_collection, {}, offset=0, limit=10)
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.get_many')
    def test_student_preference_search_workflow(self, mock_get_many, mock_get_collection):
        """Test student preference search and filtering workflow"""
        # Mock collection
        mock_collection = Mock(spec=Collection)
        mock_get_collection.return_value = mock_collection
        
        # Mock search results
        mock_preferences = [
            {**self.sample_preference_data, "userid": 12345},
            {**self.sample_preference_data, "userid": 12346, "budget_max": 80000}
        ]
        mock_get_many.return_value = mock_preferences
        
        # Test get all preferences
        all_preferences = get_all_student_preferences(offset=0, limit=10)
        assert len(all_preferences) == 2
        assert all(isinstance(preference, StudentPreference) for preference in all_preferences)
        mock_get_many.assert_called_with(mock_collection, {}, offset=0, limit=10)


class TestStudentCRUDErrorHandling:
    """Test error handling in Student CRUD operations"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Sample education data
        self.sample_education = Education(
            name="Stanford University",
            period="09/19-06/23",
            gpa=3.7,
            degree="Bachelor of Arts",
            major="Psychology"
        )
        
        # Sample student profile data
        self.sample_profile_data = {
            "userid": 12345,
            "gender": "Non-binary",
            "overview": "Psychology student interested in cognitive science",
            "educations": [self.sample_education.model_dump()],
            "experience": [],
            "activities": [],
            "standardized_tests": [],
            "awards": [],
            "others": "Volunteer work in mental health"
        }
        
        # Sample student preference data
        self.sample_preference_data = {
            "userid": 12345,
            "intended_major": ["Psychology", "Cognitive Science"],
            "intended_degree": ["Master of Arts", "PhD"],
            "preferred_countries": ["United States", "United Kingdom"],
            "preferred_cities": ["New York", "London"],
            "budget_min": 25000,
            "budget_max": 45000,
            "others": "Interested in research programs"
        }
        
        self.sample_profile = StudentProfile(**self.sample_profile_data)
        self.sample_preference = StudentPreference(**self.sample_preference_data)
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    def test_database_connection_error_profile(self, mock_get_collection):
        """Test handling of database connection errors for profiles"""
        # Mock database connection error
        mock_get_collection.side_effect = Exception("Database connection failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Database connection failed"):
            create_student_profile(self.sample_profile)
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    def test_database_connection_error_preference(self, mock_get_collection):
        """Test handling of database connection errors for preferences"""
        # Mock database connection error
        mock_get_collection.side_effect = Exception("Database connection failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Database connection failed"):
            create_student_preference(self.sample_preference)
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.get_one')
    def test_get_profile_database_error(self, mock_get_one, mock_get_collection):
        """Test handling of database errors in get profile operations"""
        # Mock collection and database error
        mock_collection = Mock(spec=Collection)
        mock_get_collection.return_value = mock_collection
        mock_get_one.side_effect = Exception("Query failed")
        
        # Test that None is returned on error
        result = get_student_profile_by_userid(12345)
        assert result is None
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.get_one')
    def test_get_preference_database_error(self, mock_get_one, mock_get_collection):
        """Test handling of database errors in get preference operations"""
        # Mock collection and database error
        mock_collection = Mock(spec=Collection)
        mock_get_collection.return_value = mock_collection
        mock_get_one.side_effect = Exception("Query failed")
        
        # Test that None is returned on error
        result = get_student_preference_by_userid(12345)
        assert result is None
    
    @patch('src.interface.crud.user.usrStudent.get_student_profiles_collection')
    @patch('src.interface.crud.user.usrStudent.get_many')
    def test_get_profiles_database_error(self, mock_get_many, mock_get_collection):
        """Test handling of database errors in get many profile operations"""
        # Mock collection and database error
        mock_collection = Mock(spec=Collection)
        mock_get_collection.return_value = mock_collection
        mock_get_many.side_effect = Exception("Query failed")
        
        # Test that empty list is returned on error
        result = get_all_student_profiles()
        assert result == []
    
    @patch('src.interface.crud.user.usrStudent.get_student_preferences_collection')
    @patch('src.interface.crud.user.usrStudent.get_many')
    def test_get_preferences_database_error(self, mock_get_many, mock_get_collection):
        """Test handling of database errors in get many preference operations"""
        # Mock collection and database error
        mock_collection = Mock(spec=Collection)
        mock_get_collection.return_value = mock_collection
        mock_get_many.side_effect = Exception("Query failed")
        
        # Test that empty list is returned on error
        result = get_all_student_preferences()
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
