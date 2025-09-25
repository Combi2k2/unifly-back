"""
Test suite for MongoDB integration functions
Tests all CRUD operations and MongoDB client functionality
"""

import pytest
import os
from unittest.mock import Mock, patch
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Import the functions to test
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.integrations.internal.mongodb import (
    get_mongodb_client,
    get_mongodb_database,
    get_mongodb_collection,
    close_mongodb_connection,
    check_mongodb_connection,
    reconnect_mongodb,
    create,
    read_one,
    read_many,
    update,
    delete,
    count
)

class TestMongoDBClient:
    """Test MongoDB client management functions"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Reset global client
        import src.integrations.internal.mongodb as mongodb_module
        mongodb_module._client = None
    
    def teardown_method(self):
        """Cleanup after each test method"""
        close_mongodb_connection()
    
    @patch('src.integrations.internal.mongodb.MongoClient')
    def test_get_mongodb_client_success(self, mock_mongo_client):
        """Test successful MongoDB client creation"""
        # Mock the client instance
        mock_client_instance = Mock()
        mock_mongo_client.return_value = mock_client_instance
        mock_client_instance.admin.command.return_value = True
        
        # Test client creation
        client = get_mongodb_client()
        
        # Assertions
        assert client == mock_client_instance
        mock_mongo_client.assert_called_once()
        mock_client_instance.admin.command.assert_called_with('ping')
    
    @patch('src.integrations.internal.mongodb.MongoClient')
    def test_get_mongodb_client_connection_failure(self, mock_mongo_client):
        """Test MongoDB client creation with connection failure"""
        # Mock connection failure
        mock_mongo_client.side_effect = ConnectionFailure("Connection failed")
        
        # Test that exception is raised
        with pytest.raises(ConnectionFailure):
            get_mongodb_client()
    
    @patch('src.integrations.internal.mongodb.MongoClient')
    def test_get_mongodb_client_server_timeout(self, mock_mongo_client):
        """Test MongoDB client creation with server timeout"""
        # Mock server timeout
        mock_mongo_client.side_effect = ServerSelectionTimeoutError("Server timeout")
        
        # Test that exception is raised
        with pytest.raises(ServerSelectionTimeoutError):
            get_mongodb_client()
    
    @patch('src.integrations.internal.mongodb.get_mongodb_client')
    def test_get_mongodb_database_success(self, mock_get_client):
        """Test successful database access"""
        # Mock client and database
        mock_client = Mock()
        mock_database = Mock()
        mock_client.__getitem__ = Mock(return_value=mock_database)
        mock_database.command.return_value = True
        mock_get_client.return_value = mock_client
        
        # Test database access
        database = get_mongodb_database("test_db")
        
        # Assertions
        assert database == mock_database
        mock_client.__getitem__.assert_called_once_with("test_db")
        mock_database.command.assert_called_with('ping')
    
    @patch('src.integrations.internal.mongodb.get_mongodb_client')
    def test_get_mongodb_database_failure(self, mock_get_client):
        """Test database access failure"""
        # Mock client failure
        mock_get_client.side_effect = ConnectionFailure("Connection failed")
        
        # Test that exception is raised
        with pytest.raises(ConnectionFailure):
            get_mongodb_database("test_db")
    
    @patch('src.integrations.internal.mongodb.get_mongodb_database')
    def test_get_mongodb_collection_success(self, mock_get_database):
        """Test successful collection access"""
        # Mock database and collection
        mock_database = Mock()
        mock_collection = Mock()
        mock_database.__getitem__ = Mock(return_value=mock_collection)
        mock_get_database.return_value = mock_database
        
        # Test collection access
        collection = get_mongodb_collection("test_db", "test_collection")
        
        # Assertions
        assert collection == mock_collection
        mock_database.__getitem__.assert_called_once_with("test_collection")
    
    def test_get_mongodb_collection_none_name(self):
        """Test collection access with None collection name"""
        with pytest.raises(TypeError, match="name must be an instance of str, not <class 'NoneType'>"):
            get_mongodb_collection("test_db", None)
    
    def test_close_mongodb_connection(self):
        """Test closing MongoDB connection"""
        # Mock client
        mock_client = Mock()
        import src.integrations.internal.mongodb as mongodb_module
        mongodb_module._client = mock_client
        
        # Test connection close
        close_mongodb_connection()
        
        # Assertions
        mock_client.close.assert_called_once()
        assert mongodb_module._client is None
    
    def test_close_mongodb_connection_no_client(self):
        """Test closing connection when no client exists"""
        # Ensure no client
        import src.integrations.internal.mongodb as mongodb_module
        mongodb_module._client = None
        
        # Should not raise exception
        close_mongodb_connection()
    
    @patch('src.integrations.internal.mongodb._client')
    def test_check_mongodb_connection_success(self, mock_client):
        """Test successful connection check"""
        # Mock successful ping
        mock_client.admin.command.return_value = True
        
        # Test connection check
        result = check_mongodb_connection()
        
        # Assertions
        assert result is True
        mock_client.admin.command.assert_called_with('ping')
    
    def test_check_mongodb_connection_failure(self):
        """Test connection check failure"""
        # Mock client as None
        import src.integrations.internal.mongodb as mongodb_module
        mongodb_module._client = None
        
        # Test connection check
        result = check_mongodb_connection()
        
        # Assertions
        assert result is False
    
    @patch('src.integrations.internal.mongodb._client')
    def test_check_mongodb_connection_exception(self, mock_client):
        """Test connection check with exception"""
        # Mock ping failure
        mock_client.admin.command.side_effect = Exception("Ping failed")
        
        # Test connection check
        result = check_mongodb_connection()
        
        # Assertions
        assert result is False
    
    @patch('src.integrations.internal.mongodb.close_mongodb_connection')
    @patch('src.integrations.internal.mongodb.get_mongodb_client')
    def test_reconnect_mongodb(self, mock_get_client, mock_close):
        """Test MongoDB reconnection"""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Test reconnection
        result = reconnect_mongodb()
        
        # Assertions
        assert result == mock_client
        mock_close.assert_called_once()
        mock_get_client.assert_called_once()


class TestCRUDOperations:
    """Test CRUD operations"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create mock collection
        self.mock_collection = Mock(spec=Collection)
        self.mock_collection.name = "test_collection"
    
    def test_create_success(self):
        """Test successful document creation"""
        # Mock collection response
        mock_result = Mock()
        mock_result.inserted_id = "test_id_123"
        self.mock_collection.insert_one.return_value = mock_result
        
        # Test data
        test_data = {"name": "Test Document", "value": 42}
        
        # Test create operation
        result = create(self.mock_collection, test_data)
        
        # Assertions
        assert result == "test_id_123"
        self.mock_collection.insert_one.assert_called_once_with(test_data)
    
    def test_create_with_pydantic_model(self):
        """Test document creation with Pydantic model"""
        # Mock Pydantic model
        mock_model = Mock()
        mock_model.model_dump.return_value = {"name": "Test", "id": 1}
        
        # Mock collection response
        mock_result = Mock()
        mock_result.inserted_id = "test_id_456"
        self.mock_collection.insert_one.return_value = mock_result
        
        # Test create operation
        result = create(self.mock_collection, mock_model)
        
        # Assertions
        assert result == "test_id_456"
        mock_model.model_dump.assert_called_once()
        self.mock_collection.insert_one.assert_called_once_with({"name": "Test", "id": 1})
    
    def test_create_failure(self):
        """Test document creation failure"""
        # Mock collection failure
        self.mock_collection.insert_one.side_effect = Exception("Insert failed")
        
        # Test data
        test_data = {"name": "Test Document"}
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Insert failed"):
            create(self.mock_collection, test_data)
    
    def test_read_one_success(self):
        """Test successful document read by ID"""
        # Mock collection response
        mock_document = {"_id": "test_id", "name": "Test Document", "value": 42}
        self.mock_collection.find_one.return_value = mock_document
        
        # Test read operation
        result = read_one(self.mock_collection, "test_id")
        
        # Assertions
        expected = {"name": "Test Document", "value": 42}  # _id removed
        assert result == expected
        self.mock_collection.find_one.assert_called_once_with({"_id": "test_id"})
    
    def test_read_one_not_found(self):
        """Test document read when not found"""
        # Mock collection response
        self.mock_collection.find_one.return_value = None
        
        # Test read operation
        result = read_one(self.mock_collection, "nonexistent_id")
        
        # Assertions
        assert result is None
        self.mock_collection.find_one.assert_called_once_with({"_id": "nonexistent_id"})
    
    def test_read_one_failure(self):
        """Test document read failure"""
        # Mock collection failure
        self.mock_collection.find_one.side_effect = Exception("Find failed")
        
        # Test read operation
        result = read_one(self.mock_collection, "test_id")
        
        # Assertions
        assert result is None
    
    def test_read_many_success(self):
        """Test successful multiple document read"""
        # Mock collection response
        mock_documents = [
            {"_id": "id1", "name": "Doc1", "value": 1},
            {"_id": "id2", "name": "Doc2", "value": 2}
        ]
        mock_cursor = Mock()
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        # Use side_effect to return the iterator
        mock_cursor.__iter__ = Mock(return_value=iter(mock_documents))
        self.mock_collection.find.return_value = mock_cursor
        
        # Test read operation
        filters = {"status": "active"}
        result = read_many(self.mock_collection, filters, offset=0, limit=10)
        
        # Assertions
        expected = [
            {"name": "Doc1", "value": 1},  # _id removed
            {"name": "Doc2", "value": 2}   # _id removed
        ]
        assert result == expected
        self.mock_collection.find.assert_called_once_with(filters)
        # Skip is not called when offset is 0
        mock_cursor.skip.assert_not_called()
        mock_cursor.limit.assert_called_once_with(10)
    
    def test_read_many_no_offset(self):
        """Test read many without offset"""
        # Mock collection response
        mock_documents = [{"_id": "id1", "name": "Doc1"}]
        mock_cursor = Mock()
        mock_cursor.limit.return_value = mock_cursor
        mock_cursor.__iter__ = Mock(return_value=iter(mock_documents))
        self.mock_collection.find.return_value = mock_cursor
        
        # Test read operation
        result = read_many(self.mock_collection, {}, offset=0, limit=5)
        
        # Assertions
        expected = [{"name": "Doc1"}]  # _id removed
        assert result == expected
        mock_cursor.skip.assert_not_called()
        mock_cursor.limit.assert_called_once_with(5)
    
    def test_read_many_failure(self):
        """Test read many failure"""
        # Mock collection failure
        self.mock_collection.find.side_effect = Exception("Find failed")
        
        # Test read operation
        result = read_many(self.mock_collection, {}, offset=0, limit=10)
        
        # Assertions
        assert result == []
    
    def test_update_success(self):
        """Test successful document update"""
        # Mock collection response
        mock_result = Mock()
        mock_result.modified_count = 1
        self.mock_collection.update_one.return_value = mock_result
        
        # Test data
        test_data = {"name": "Updated Document", "value": 100}
        
        # Test update operation
        result = update(self.mock_collection, "test_id", test_data)
        
        # Assertions
        assert result is True
        self.mock_collection.update_one.assert_called_once_with(
            {"_id": "test_id"},
            {"$set": test_data}
        )
    
    def test_update_with_pydantic_model(self):
        """Test document update with Pydantic model"""
        # Mock Pydantic model
        mock_model = Mock()
        mock_model.model_dump.return_value = {"name": "Updated", "id": 1}
        
        # Mock collection response
        mock_result = Mock()
        mock_result.modified_count = 1
        self.mock_collection.update_one.return_value = mock_result
        
        # Test update operation
        result = update(self.mock_collection, "test_id", mock_model)
        
        # Assertions
        assert result is True
        mock_model.model_dump.assert_called_once()
        self.mock_collection.update_one.assert_called_once_with(
            {"_id": "test_id"},
            {"$set": {"name": "Updated", "id": 1}}
        )
    
    def test_update_not_found(self):
        """Test document update when not found"""
        # Mock collection response
        mock_result = Mock()
        mock_result.modified_count = 0
        self.mock_collection.update_one.return_value = mock_result
        
        # Test data
        test_data = {"name": "Updated Document"}
        
        # Test update operation
        result = update(self.mock_collection, "nonexistent_id", test_data)
        
        # Assertions
        assert result is False
    
    def test_update_failure(self):
        """Test document update failure"""
        # Mock collection failure
        self.mock_collection.update_one.side_effect = Exception("Update failed")
        
        # Test data
        test_data = {"name": "Updated Document"}
        
        # Test update operation
        result = update(self.mock_collection, "test_id", test_data)
        
        # Assertions
        assert result is False
    
    def test_delete_success(self):
        """Test successful document deletion"""
        # Mock collection response
        mock_result = Mock()
        mock_result.deleted_count = 1
        self.mock_collection.delete_one.return_value = mock_result
        
        # Test delete operation
        result = delete(self.mock_collection, "test_id")
        
        # Assertions
        assert result is True
        self.mock_collection.delete_one.assert_called_once_with({"_id": "test_id"})
    
    def test_delete_not_found(self):
        """Test document deletion when not found"""
        # Mock collection response
        mock_result = Mock()
        mock_result.deleted_count = 0
        self.mock_collection.delete_one.return_value = mock_result
        
        # Test delete operation
        result = delete(self.mock_collection, "nonexistent_id")
        
        # Assertions
        assert result is False
    
    def test_delete_failure(self):
        """Test document deletion failure"""
        # Mock collection failure
        self.mock_collection.delete_one.side_effect = Exception("Delete failed")
        
        # Test delete operation
        result = delete(self.mock_collection, "test_id")
        
        # Assertions
        assert result is False
    
    def test_count_success(self):
        """Test successful document count"""
        # Mock collection response
        self.mock_collection.count_documents.return_value = 42
        
        # Test count operation
        result = count(self.mock_collection)
        
        # Assertions
        assert result == 42
        self.mock_collection.count_documents.assert_called_once_with({})
    
    def test_count_failure(self):
        """Test document count failure"""
        # Mock collection failure
        self.mock_collection.count_documents.side_effect = Exception("Count failed")
        
        # Test count operation
        result = count(self.mock_collection)
        
        # Assertions
        assert result == 0


class TestIntegration:
    """Integration tests for MongoDB functions"""
    
    @patch('src.integrations.internal.mongodb.get_mongodb_collection')
    def test_full_crud_workflow(self, mock_get_collection):
        """Test complete CRUD workflow"""
        # Mock collection
        mock_collection = Mock(spec=Collection)
        mock_collection.name = "test_collection"
        mock_get_collection.return_value = mock_collection
        
        # Mock responses
        mock_insert_result = Mock()
        mock_insert_result.inserted_id = "test_id_123"
        mock_collection.insert_one.return_value = mock_insert_result
        
        mock_document = {"_id": "test_id_123", "name": "Test Document", "value": 42}
        mock_collection.find_one.return_value = mock_document
        
        mock_update_result = Mock()
        mock_update_result.modified_count = 1
        mock_collection.update_one.return_value = mock_update_result
        
        mock_delete_result = Mock()
        mock_delete_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_delete_result
        
        mock_collection.count_documents.return_value = 1
        
        # Test workflow
        test_data = {"name": "Test Document", "value": 42}
        
        # Create
        doc_id = create(mock_collection, test_data)
        assert doc_id == "test_id_123"
        
        # Read
        doc = read_one(mock_collection, doc_id)
        assert doc == {"name": "Test Document", "value": 42}
        
        # Update
        updated_data = {"name": "Updated Document", "value": 100}
        update_success = update(mock_collection, doc_id, updated_data)
        assert update_success is True
        
        # Count
        doc_count = count(mock_collection)
        assert doc_count == 1
        
        # Delete
        delete_success = delete(mock_collection, doc_id)
        assert delete_success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
