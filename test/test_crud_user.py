"""
Test suite for User CRUD operations
Tests all user-related CRUD functions in interface/crud/user/base.py
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pymongo.collection import Collection

# Import the specific functions we need
from src.interface.crud.user.base import (
    get_users_collection,
    create_user,
    get_user_by_id,
    get_user_by_email,
    get_users_by_role,
    get_users_by_status,
    get_all_users,
    update_user,
    update_user_status,
    delete_user,
    count_users,
    count_users_by_role,
    count_users_by_status
)
from src.integrations.internal.mongodb import get_one, get_many, insert, update, delete, count
from src.models.user.base import UserBase, UserSessionBase, USER_ROLE_STUDENT, USER_STATUS_ACTIVE
from src.models.user.base import UserBase as SrcUserBase


class TestUserCRUD:
    """Test User CRUD operations"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create mock collection
        self.mock_collection = Mock(spec=Collection)
        self.mock_collection.name = "users"
        
        # Sample user data
        self.sample_user_data = {
            "userid": 12345,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "date_of_birth": datetime(1990, 1, 1),
            "nationality": "US",
            "hashed_password": "hashed_password_123",
            "role": USER_ROLE_STUDENT,
            "status": USER_STATUS_ACTIVE,
            "profile_picture_url": "https://example.com/profile.jpg",
            "timezone": "UTC",
            "language_preference": "en"
        }
        
        self.sample_user = UserBase(**self.sample_user_data)
    
    @patch('src.interface.crud.user.base.get_mongodb_database')
    def test_get_users_collection(self, mock_get_database):
        """Test getting users collection"""
        # Mock database
        mock_database = Mock()
        mock_database.__getitem__ = Mock(return_value=self.mock_collection)
        mock_get_database.return_value = mock_database
        
        # Test collection access
        collection = get_users_collection()
        
        # Assertions
        assert collection == self.mock_collection
        mock_get_database.assert_called_once()
        mock_database.__getitem__.assert_called_once_with("unifly_users")
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.insert')
    def test_create_user_success(self, mock_insert, mock_get_collection):
        """Test successful user creation"""
        # Mock collection and insert
        mock_get_collection.return_value = self.mock_collection
        mock_insert.return_value = "user_id_123"
        
        # Test user creation
        result = create_user(self.sample_user)
        
        # Assertions
        assert result == "user_id_123"
        mock_get_collection.assert_called_once()
        mock_insert.assert_called_once_with(self.mock_collection, self.sample_user)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.insert')
    def test_create_user_failure(self, mock_insert, mock_get_collection):
        """Test user creation failure"""
        # Mock collection and insert failure
        mock_get_collection.return_value = self.mock_collection
        mock_insert.side_effect = Exception("Database error")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Database error"):
            create_user(self.sample_user)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_one')
    def test_get_user_by_id_success(self, mock_get_one, mock_get_collection):
        """Test successful user retrieval by ID"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.return_value = self.sample_user_data
        
        # Test user retrieval
        result = get_user_by_id(12345)
        
        # Assertions
        assert isinstance(result, SrcUserBase)
        assert result.userid == self.sample_user_data["userid"]
        assert result.email == self.sample_user_data["email"]
        mock_get_collection.assert_called_once()
        mock_get_one.assert_called_once_with(self.mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_one')
    def test_get_user_by_id_not_found(self, mock_get_one, mock_get_collection):
        """Test user retrieval by ID when not found"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.return_value = None
        
        # Test user retrieval
        result = get_user_by_id(99999)
        
        # Assertions
        assert result is None
        mock_get_one.assert_called_once_with(self.mock_collection, {"userid": 99999})
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_one')
    def test_get_user_by_email_success(self, mock_get_one, mock_get_collection):
        """Test successful user retrieval by email"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.return_value = self.sample_user_data
        
        # Test user retrieval
        result = get_user_by_email("john.doe@example.com")
        
        # Assertions
        assert isinstance(result, SrcUserBase)
        assert result.userid == self.sample_user_data["userid"]
        assert result.email == self.sample_user_data["email"]
        mock_get_collection.assert_called_once()
        mock_get_one.assert_called_once_with(self.mock_collection, {"email": "john.doe@example.com"})
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_one')
    def test_get_user_by_email_not_found(self, mock_get_one, mock_get_collection):
        """Test user retrieval by email when not found"""
        # Mock collection and get_one
        mock_get_collection.return_value = self.mock_collection
        mock_get_one.return_value = None
        
        # Test user retrieval
        result = get_user_by_email("nonexistent@example.com")
        
        # Assertions
        assert result is None
        mock_get_one.assert_called_once_with(self.mock_collection, {"email": "nonexistent@example.com"})
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_many')
    def test_get_users_by_role_success(self, mock_get_many, mock_get_collection):
        """Test successful users retrieval by role"""
        # Mock collection and get_many
        mock_get_collection.return_value = self.mock_collection
        mock_users = [self.sample_user_data, {**self.sample_user_data, "userid": 12346}]
        mock_get_many.return_value = mock_users
        
        # Test users retrieval
        result = get_users_by_role("student", offset=0, limit=10)
        
        # Assertions
        assert len(result) == 2
        assert all(isinstance(user, SrcUserBase) for user in result)
        assert result[0].userid == 12345
        assert result[1].userid == 12346
        mock_get_collection.assert_called_once()
        mock_get_many.assert_called_once_with(self.mock_collection, {"role": "student"}, offset=0, limit=10)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_many')
    def test_get_users_by_status_success(self, mock_get_many, mock_get_collection):
        """Test successful users retrieval by status"""
        # Mock collection and get_many
        mock_get_collection.return_value = self.mock_collection
        mock_users = [self.sample_user_data]
        mock_get_many.return_value = mock_users
        
        # Test users retrieval
        result = get_users_by_status("active", offset=0, limit=10)
        
        # Assertions
        assert len(result) == 1
        assert all(isinstance(user, SrcUserBase) for user in result)
        assert result[0].userid == 12345
        mock_get_collection.assert_called_once()
        mock_get_many.assert_called_once_with(self.mock_collection, {"status": "active"}, offset=0, limit=10)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_many')
    def test_get_all_users_success(self, mock_get_many, mock_get_collection):
        """Test successful retrieval of all users"""
        # Mock collection and get_many
        mock_get_collection.return_value = self.mock_collection
        mock_users = [self.sample_user_data, {**self.sample_user_data, "userid": 12346}]
        mock_get_many.return_value = mock_users
        
        # Test users retrieval
        result = get_all_users(offset=0, limit=10)
        
        # Assertions
        assert len(result) == 2
        assert all(isinstance(user, SrcUserBase) for user in result)
        assert result[0].userid == 12345
        assert result[1].userid == 12346
        mock_get_collection.assert_called_once()
        mock_get_many.assert_called_once_with(self.mock_collection, {}, offset=0, limit=10)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.update')
    def test_update_user_success(self, mock_update, mock_get_collection):
        """Test successful user update"""
        # Mock collection and update
        mock_get_collection.return_value = self.mock_collection
        mock_update.return_value = True
        
        # Test user update
        result = update_user(12345, self.sample_user)
        
        # Assertions
        assert result is True
        mock_get_collection.assert_called_once()
        mock_update.assert_called_once_with(self.mock_collection, {"userid": 12345}, self.sample_user)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.update')
    def test_update_user_failure(self, mock_update, mock_get_collection):
        """Test user update failure"""
        # Mock collection and update
        mock_get_collection.return_value = self.mock_collection
        mock_update.return_value = False
        
        # Test user update
        result = update_user(12345, self.sample_user)
        
        # Assertions
        assert result is False
        mock_update.assert_called_once_with(self.mock_collection, {"userid": 12345}, self.sample_user)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.update')
    def test_update_user_status_success(self, mock_update, mock_get_collection):
        """Test successful user status update"""
        # Mock collection and update
        mock_get_collection.return_value = self.mock_collection
        mock_update.return_value = True
        
        # Test user status update
        result = update_user_status(12345, "inactive")
        
        # Assertions
        assert result is True
        mock_get_collection.assert_called_once()
        mock_update.assert_called_once_with(self.mock_collection, {"userid": 12345}, {"status": "inactive"})
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.delete')
    def test_delete_user_success(self, mock_delete, mock_get_collection):
        """Test successful user deletion"""
        # Mock collection and delete
        mock_get_collection.return_value = self.mock_collection
        mock_delete.return_value = True
        
        # Test user deletion
        result = delete_user(12345)
        
        # Assertions
        assert result is True
        mock_get_collection.assert_called_once()
        mock_delete.assert_called_once_with(self.mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.delete')
    def test_delete_user_failure(self, mock_delete, mock_get_collection):
        """Test user deletion failure"""
        # Mock collection and delete
        mock_get_collection.return_value = self.mock_collection
        mock_delete.return_value = False
        
        # Test user deletion
        result = delete_user(12345)
        
        # Assertions
        assert result is False
        mock_delete.assert_called_once_with(self.mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.count')
    def test_count_users_success(self, mock_count, mock_get_collection):
        """Test successful user count"""
        # Mock collection and count
        mock_get_collection.return_value = self.mock_collection
        mock_count.return_value = 42
        
        # Test user count
        result = count_users()
        
        # Assertions
        assert result == 42
        mock_get_collection.assert_called_once()
        mock_count.assert_called_once_with(self.mock_collection)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    def test_count_users_by_role_success(self, mock_get_collection):
        """Test successful user count by role"""
        # Mock collection and count_documents
        mock_get_collection.return_value = self.mock_collection
        self.mock_collection.count_documents.return_value = 15
        
        # Test user count by role
        result = count_users_by_role("student")
        
        # Assertions
        assert result == 15
        mock_get_collection.assert_called_once()
        self.mock_collection.count_documents.assert_called_once_with({"role": "student"})
    
    @patch('src.interface.crud.user.base.get_users_collection')
    def test_count_users_by_status_success(self, mock_get_collection):
        """Test successful user count by status"""
        # Mock collection and count_documents
        mock_get_collection.return_value = self.mock_collection
        self.mock_collection.count_documents.return_value = 8
        
        # Test user count by status
        result = count_users_by_status("active")
        
        # Assertions
        assert result == 8
        mock_get_collection.assert_called_once()
        self.mock_collection.count_documents.assert_called_once_with({"status": "active"})


class TestUserCRUDIntegration:
    """Integration tests for User CRUD operations"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Sample user data
        self.sample_user_data = {
            "userid": 12345,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "date_of_birth": datetime(1990, 1, 1),
            "nationality": "US",
            "hashed_password": "hashed_password_123",
            "role": USER_ROLE_STUDENT,
            "status": USER_STATUS_ACTIVE,
            "profile_picture_url": "https://example.com/profile.jpg",
            "timezone": "UTC",
            "language_preference": "en"
        }
        
        self.sample_user = UserBase(**self.sample_user_data)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.insert')
    @patch('src.interface.crud.user.base.get_one')
    @patch('src.interface.crud.user.base.update')
    @patch('src.interface.crud.user.base.delete')
    def test_full_user_crud_workflow(self, mock_delete, mock_update, mock_get_one, mock_insert, mock_get_collection):
        """Test complete user CRUD workflow"""
        # Mock collection
        mock_collection = Mock(spec=Collection)
        mock_collection.name = "users"
        mock_get_collection.return_value = mock_collection
        
        # Mock responses
        mock_insert.return_value = "user_id_123"
        mock_get_one.return_value = self.sample_user_data
        mock_update.return_value = True
        mock_delete.return_value = True
        
        # Test workflow
        # 1. Create user
        user_id = create_user(self.sample_user)
        assert user_id == "user_id_123"
        mock_insert.assert_called_once_with(mock_collection, self.sample_user)
        
        # 2. Get user by ID
        user = get_user_by_id(12345)
        assert isinstance(user, SrcUserBase)
        assert user.userid == self.sample_user_data["userid"]
        mock_get_one.assert_called_once_with(mock_collection, {"userid": 12345})
        
        # 3. Update user
        updated_user = UserBase(**{**self.sample_user_data, "first_name": "Jane"})
        update_success = update_user(12345, updated_user)
        assert update_success is True
        mock_update.assert_called_once_with(mock_collection, {"userid": 12345}, updated_user)
        
        # 4. Delete user
        delete_success = delete_user(12345)
        assert delete_success is True
        mock_delete.assert_called_once_with(mock_collection, {"userid": 12345})
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_many')
    def test_user_search_workflow(self, mock_get_many, mock_get_collection):
        """Test user search and filtering workflow"""
        # Mock collection
        mock_collection = Mock(spec=Collection)
        mock_get_collection.return_value = mock_collection
        
        # Mock search results
        mock_users = [
            {**self.sample_user_data, "userid": 12345},
            {**self.sample_user_data, "userid": 12346, "first_name": "Jane"}
        ]
        mock_get_many.return_value = mock_users
        
        # Test search by role
        students = get_users_by_role("student", offset=0, limit=10)
        assert len(students) == 2
        assert all(isinstance(user, SrcUserBase) for user in students)
        mock_get_many.assert_called_with(mock_collection, {"role": "student"}, offset=0, limit=10)
        
        # Test search by status
        active_users = get_users_by_status("active", offset=0, limit=10)
        assert len(active_users) == 2
        assert all(isinstance(user, SrcUserBase) for user in active_users)
        mock_get_many.assert_called_with(mock_collection, {"status": "active"}, offset=0, limit=10)
        
        # Test get all users
        all_users = get_all_users(offset=0, limit=10)
        assert len(all_users) == 2
        assert all(isinstance(user, SrcUserBase) for user in all_users)
        mock_get_many.assert_called_with(mock_collection, {}, offset=0, limit=10)


class TestUserCRUDErrorHandling:
    """Test error handling in User CRUD operations"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.sample_user_data = {
            "userid": 12345,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "date_of_birth": datetime(1990, 1, 1),
            "nationality": "US",
            "hashed_password": "hashed_password_123",
            "role": USER_ROLE_STUDENT,
            "status": USER_STATUS_ACTIVE,
            "profile_picture_url": "https://example.com/profile.jpg",
            "timezone": "UTC",
            "language_preference": "en"
        }
        
        self.sample_user = UserBase(**self.sample_user_data)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    def test_database_connection_error(self, mock_get_collection):
        """Test handling of database connection errors"""
        # Mock database connection error
        mock_get_collection.side_effect = Exception("Database connection failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Database connection failed"):
            create_user(self.sample_user)
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_one')
    def test_get_user_database_error(self, mock_get_one, mock_get_collection):
        """Test handling of database errors in get operations"""
        # Mock collection and database error
        mock_collection = Mock(spec=Collection)
        mock_get_collection.return_value = mock_collection
        mock_get_one.side_effect = Exception("Query failed")
        
        # Test that None is returned on error
        result = get_user_by_id(12345)
        assert result is None
    
    @patch('src.interface.crud.user.base.get_users_collection')
    @patch('src.interface.crud.user.base.get_many')
    def test_get_users_database_error(self, mock_get_many, mock_get_collection):
        """Test handling of database errors in get many operations"""
        # Mock collection and database error
        mock_collection = Mock(spec=Collection)
        mock_get_collection.return_value = mock_collection
        mock_get_many.side_effect = Exception("Query failed")
        
        # Test that empty list is returned on error
        result = get_users_by_role("student")
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
