"""
Test suite for MongoDB integration functions
Tests all CRUD operations and MongoDB client functionality
"""

import pytest
import os
import time
from unittest.mock import Mock, patch
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from bson import ObjectId

from src.integrations.internal.mongodb import (
    get_mongodb_client,
    get_mongodb_database,
    get_mongodb_collection,
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
    
    def test_insert_success(self):
        """Test successful document insertion"""
        # Mock collection response
        mock_result = Mock(spec=InsertOneResult)
        mock_result.inserted_id = "test_id_123"
        mock_result.acknowledged = True
        self.mock_collection.insert_one.return_value = mock_result
        
        # Test data
        test_data = {"name": "Test Document", "value": 42}
        
        # Test insert operation
        result = insert(self.mock_collection, test_data)
        
        # Assertions
        assert result == mock_result
        assert result.inserted_id == "test_id_123"
        assert result.acknowledged is True
        self.mock_collection.insert_one.assert_called_once_with(test_data)
    
    def test_insert_with_pydantic_model(self):
        """Test document insertion with Pydantic model"""
        # Mock Pydantic model
        mock_model = Mock()
        mock_model.model_dump.return_value = {"name": "Test", "id": 1}
        
        # Mock collection response
        mock_result = Mock(spec=InsertOneResult)
        mock_result.inserted_id = "test_id_456"
        mock_result.acknowledged = True
        self.mock_collection.insert_one.return_value = mock_result
        
        # Test insert operation
        result = insert(self.mock_collection, mock_model)
        
        # Assertions
        assert result == mock_result
        assert result.inserted_id == "test_id_456"
        assert result.acknowledged is True
        mock_model.model_dump.assert_called_once()
        self.mock_collection.insert_one.assert_called_once_with({"name": "Test", "id": 1})
    
    def test_insert_failure(self):
        """Test document insertion failure"""
        # Mock collection failure
        self.mock_collection.insert_one.side_effect = Exception("Insert failed")
        
        # Test data
        test_data = {"name": "Test Document"}
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Insert failed"):
            insert(self.mock_collection, test_data)
        
        self.mock_collection.insert_one.assert_called_once_with(test_data)
    
    def test_get_one_success(self):
        """Test successful document get by filters"""
        # Mock collection response
        mock_document = {"_id": "test_id", "name": "Test Document", "value": 42}
        self.mock_collection.find_one.return_value = mock_document
        
        # Test get operation
        filters = {"_id": "test_id"}
        result = get_one(self.mock_collection, filters)
        
        # Assertions
        expected = {"name": "Test Document", "value": 42}  # _id removed
        assert result == expected
        self.mock_collection.find_one.assert_called_once_with(filters)
    
    def test_get_one_not_found(self):
        """Test document get when not found"""
        # Mock collection response
        self.mock_collection.find_one.return_value = None
        
        # Test get operation
        filters = {"_id": "nonexistent_id"}
        result = get_one(self.mock_collection, filters)
        
        # Assertions
        assert result is None
        self.mock_collection.find_one.assert_called_once_with(filters)
    
    def test_get_one_failure(self):
        """Test document get failure"""
        # Mock collection failure
        self.mock_collection.find_one.side_effect = Exception("Find failed")
        
        # Test get operation
        filters = {"_id": "test_id"}
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Find failed"):
            get_one(self.mock_collection, filters)
    
    def test_get_many_success(self):
        """Test successful multiple document get"""
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
        
        # Test get operation
        filters = {"status": "active"}
        result = get_many(self.mock_collection, filters, offset=0, limit=10)
        
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
    
    def test_get_many_no_offset(self):
        """Test get many without offset"""
        # Mock collection response
        mock_documents = [{"_id": "id1", "name": "Doc1"}]
        mock_cursor = Mock()
        mock_cursor.limit.return_value = mock_cursor
        mock_cursor.__iter__ = Mock(return_value=iter(mock_documents))
        self.mock_collection.find.return_value = mock_cursor
        
        # Test get operation
        result = get_many(self.mock_collection, {}, offset=0, limit=5)
        
        # Assertions
        expected = [{"name": "Doc1"}]  # _id removed
        assert result == expected
        mock_cursor.skip.assert_not_called()
        mock_cursor.limit.assert_called_once_with(5)
    
    def test_get_many_failure(self):
        """Test get many failure"""
        # Mock collection failure
        self.mock_collection.find.side_effect = Exception("Find failed")
        
        # Test get operation
        with pytest.raises(Exception, match="Find failed"):
            get_many(self.mock_collection, {}, offset=0, limit=10)
    
    def test_update_success(self):
        """Test successful document update"""
        # Mock collection response
        mock_result = Mock(spec=UpdateResult)
        mock_result.modified_count = 1
        mock_result.matched_count = 1
        mock_result.acknowledged = True
        self.mock_collection.update_one.return_value = mock_result
        
        # Test data
        test_data = {"name": "Updated Document", "value": 100}
        filters = {"_id": "test_id"}
        
        # Test update operation
        result = update(self.mock_collection, filters, test_data)
        
        # Assertions
        assert result == mock_result
        assert result.modified_count == 1
        assert result.matched_count == 1
        assert result.acknowledged is True
        self.mock_collection.update_one.assert_called_once_with(
            filters,
            {"$set": test_data}
        )
    
    def test_update_with_pydantic_model(self):
        """Test document update with Pydantic model"""
        # Mock Pydantic model
        mock_model = Mock()
        mock_model.model_dump.return_value = {"name": "Updated", "id": 1}
        
        # Mock collection response
        mock_result = Mock(spec=UpdateResult)
        mock_result.modified_count = 1
        mock_result.matched_count = 1
        mock_result.acknowledged = True
        self.mock_collection.update_one.return_value = mock_result
        
        # Test update operation
        filters = {"_id": "test_id"}
        result = update(self.mock_collection, filters, mock_model)
        
        # Assertions
        assert result == mock_result
        assert result.modified_count == 1
        assert result.matched_count == 1
        assert result.acknowledged is True
        mock_model.model_dump.assert_called_once()
        self.mock_collection.update_one.assert_called_once_with(
            filters,
            {"$set": {"name": "Updated", "id": 1}}
        )
    
    def test_update_not_found(self):
        """Test document update when not found"""
        # Mock collection response
        mock_result = Mock(spec=UpdateResult)
        mock_result.modified_count = 0
        mock_result.matched_count = 0
        mock_result.acknowledged = True
        self.mock_collection.update_one.return_value = mock_result
        
        # Test data
        test_data = {"name": "Updated Document"}
        filters = {"_id": "nonexistent_id"}
        
        # Test update operation
        result = update(self.mock_collection, filters, test_data)
        
        # Assertions
        assert result == mock_result
        assert result.modified_count == 0
        assert result.matched_count == 0
        assert result.acknowledged is True
    
    def test_update_failure(self):
        """Test document update failure"""
        # Mock collection failure
        self.mock_collection.update_one.side_effect = Exception("Update failed")
        
        # Test data
        test_data = {"name": "Updated Document"}
        filters = {"_id": "test_id"}
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Update failed"):
            update(self.mock_collection, filters, test_data)
    
    def test_delete_success(self):
        """Test successful document deletion with filters"""
        # Mock collection response
        mock_result = Mock(spec=DeleteResult)
        mock_result.deleted_count = 1
        mock_result.acknowledged = True
        self.mock_collection.delete_one.return_value = mock_result
        
        # Test delete operation with filters
        filters = {"userid": 12345}
        result = delete(self.mock_collection, filters)
        
        # Assertions
        assert result == mock_result
        assert result.deleted_count == 1
        assert result.acknowledged is True
        self.mock_collection.delete_one.assert_called_once_with(filters)
    
    def test_delete_not_found(self):
        """Test document deletion when not found"""
        # Mock collection response
        mock_result = Mock(spec=DeleteResult)
        mock_result.deleted_count = 0
        mock_result.acknowledged = True
        self.mock_collection.delete_one.return_value = mock_result
        
        # Test delete operation with filters
        filters = {"userid": 99999}
        result = delete(self.mock_collection, filters)
        
        # Assertions
        assert result == mock_result
        assert result.deleted_count == 0
        assert result.acknowledged is True
        self.mock_collection.delete_one.assert_called_once_with(filters)
    
    def test_delete_failure(self):
        """Test document deletion failure"""
        # Mock collection failure
        self.mock_collection.delete_one.side_effect = Exception("Delete failed")
        
        # Test delete operation with filters
        filters = {"userid": 12345}
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Delete failed"):
            delete(self.mock_collection, filters)
        
        self.mock_collection.delete_one.assert_called_once_with(filters)
    
    def test_count_success(self):
        """Test successful document count without filters"""
        # Mock collection response
        self.mock_collection.count_documents.return_value = 42
        
        # Test count operation without filters
        result = count(self.mock_collection)
        
        # Assertions
        assert result == 42
        self.mock_collection.count_documents.assert_called_once_with({})
    
    def test_count_with_filters_success(self):
        """Test successful document count with filters"""
        # Mock collection response
        self.mock_collection.count_documents.return_value = 5
        
        # Test count operation with filters
        filters = {"status": "active"}
        result = count(self.mock_collection, filters)
        
        # Assertions
        assert result == 5
        self.mock_collection.count_documents.assert_called_once_with(filters)
    
    def test_count_failure(self):
        """Test document count failure"""
        # Mock collection failure
        self.mock_collection.count_documents.side_effect = Exception("Count failed")
        
        # Test count operation
        with pytest.raises(Exception, match="Count failed"):
            count(self.mock_collection)
        
        self.mock_collection.count_documents.assert_called_once_with({})
    
    def test_count_with_filters_failure(self):
        """Test document count with filters failure"""
        # Mock collection failure
        self.mock_collection.count_documents.side_effect = Exception("Count failed")
        
        # Test count operation with filters
        filters = {"role": "student"}
        
        with pytest.raises(Exception, match="Count failed"):
            count(self.mock_collection, filters)
        
        self.mock_collection.count_documents.assert_called_once_with(filters)


class TestFilterOperations:
    """Test the new filter-based operations"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Create mock collection
        self.mock_collection = Mock(spec=Collection)
        self.mock_collection.name = "test_collection"
    
    def test_delete_with_complex_filters(self):
        """Test delete with complex filter conditions"""
        # Mock collection response
        mock_result = Mock(spec=DeleteResult)
        mock_result.deleted_count = 1
        mock_result.acknowledged = True
        self.mock_collection.delete_one.return_value = mock_result
        
        # Test delete with complex filters
        filters = {
            "userid": 12345,
            "status": "inactive",
            "role": "student"
        }
        result = delete(self.mock_collection, filters)
        
        # Assertions
        assert result == mock_result
        assert result.deleted_count == 1
        assert result.acknowledged is True
        self.mock_collection.delete_one.assert_called_once_with(filters)
    
    def test_delete_with_empty_filters(self):
        """Test delete with empty filters (should not delete anything)"""
        # Mock collection response
        mock_result = Mock(spec=DeleteResult)
        mock_result.deleted_count = 0
        mock_result.acknowledged = True
        self.mock_collection.delete_one.return_value = mock_result
        
        # Test delete with empty filters
        filters = {}
        result = delete(self.mock_collection, filters)
        
        # Assertions
        assert result == mock_result
        assert result.deleted_count == 0
        assert result.acknowledged is True
        self.mock_collection.delete_one.assert_called_once_with(filters)
    
    def test_count_with_multiple_filters(self):
        """Test count with multiple filter conditions"""
        # Mock collection response
        self.mock_collection.count_documents.return_value = 3
        
        # Test count with multiple filters
        filters = {
            "status": "active",
            "role": "student",
            "age": {"$gte": 18}
        }
        result = count(self.mock_collection, filters)
        
        # Assertions
        assert result == 3
        self.mock_collection.count_documents.assert_called_once_with(filters)
    
    def test_count_with_regex_filter(self):
        """Test count with regex filter"""
        # Mock collection response
        self.mock_collection.count_documents.return_value = 2
        
        # Test count with regex filter
        filters = {
            "name": {"$regex": "John", "$options": "i"}
        }
        result = count(self.mock_collection, filters)
        
        # Assertions
        assert result == 2
        self.mock_collection.count_documents.assert_called_once_with(filters)
    
    def test_count_with_range_filter(self):
        """Test count with range filter"""
        # Mock collection response
        self.mock_collection.count_documents.return_value = 7
        
        # Test count with range filter
        filters = {
            "score": {"$gte": 80, "$lte": 100}
        }
        result = count(self.mock_collection, filters)
        
        # Assertions
        assert result == 7
        self.mock_collection.count_documents.assert_called_once_with(filters)
    
    def test_delete_with_objectid_filter(self):
        """Test delete with ObjectId filter"""
        from bson import ObjectId
        
        # Mock collection response
        mock_result = Mock(spec=DeleteResult)
        mock_result.deleted_count = 1
        mock_result.acknowledged = True
        self.mock_collection.delete_one.return_value = mock_result
        
        # Test delete with ObjectId filter
        object_id = ObjectId()
        filters = {"_id": object_id}
        result = delete(self.mock_collection, filters)
        
        # Assertions
        assert result == mock_result
        assert result.deleted_count == 1
        assert result.acknowledged is True
        self.mock_collection.delete_one.assert_called_once_with(filters)


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
        mock_insert_result = Mock(spec=InsertOneResult)
        mock_insert_result.inserted_id = "test_id_123"
        mock_insert_result.acknowledged = True
        mock_collection.insert_one.return_value = mock_insert_result
        
        mock_document = {"_id": "test_id_123", "name": "Test Document", "value": 42}
        mock_collection.find_one.return_value = mock_document
        
        mock_update_result = Mock(spec=UpdateResult)
        mock_update_result.modified_count = 1
        mock_update_result.matched_count = 1
        mock_update_result.acknowledged = True
        mock_collection.update_one.return_value = mock_update_result
        
        mock_delete_result = Mock(spec=DeleteResult)
        mock_delete_result.deleted_count = 1
        mock_delete_result.acknowledged = True
        mock_collection.delete_one.return_value = mock_delete_result
        
        mock_collection.count_documents.return_value = 1
        
        # Test workflow
        test_data = {"name": "Test Document", "value": 42}
        
        # Insert
        insert_result = insert(mock_collection, test_data)
        assert insert_result == mock_insert_result
        assert insert_result.inserted_id == "test_id_123"
        assert insert_result.acknowledged is True
        
        # Get
        doc = get_one(mock_collection, {"_id": "test_id_123"})
        assert doc == {"name": "Test Document", "value": 42}
        
        # Update
        updated_data = {"name": "Updated Document", "value": 100}
        update_result = update(mock_collection, {"_id": "test_id_123"}, updated_data)
        assert update_result == mock_update_result
        assert update_result.modified_count == 1
        assert update_result.matched_count == 1
        assert update_result.acknowledged is True
        
        # Count
        doc_count = count(mock_collection)
        assert doc_count == 1
        
        # Delete with filter
        delete_result = delete(mock_collection, {"_id": "test_id_123"})
        assert delete_result == mock_delete_result
        assert delete_result.deleted_count == 1
        assert delete_result.acknowledged is True
        
        # Count with filters
        filtered_count = count(mock_collection, {"name": "Updated Document"})
        assert filtered_count == 1


class TestRealMongoDBIntegration:
    """Integration tests with real MongoDB database"""
    
    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        """Setup and cleanup for each test"""
        # Setup: Create test collection
        self.test_collection_name = f"test_integration_{int(time.time())}"
        self.test_collection = get_mongodb_collection(
            database_name="unifly_test", 
            collection_name=self.test_collection_name
        )
        
        # Clean up any existing data
        self.test_collection.delete_many({})
        
        yield
        
        # Cleanup: Remove all test data
        try:
            self.test_collection.delete_many({})
            # Drop the test collection
            self.test_collection.drop()
        except Exception as e:
            print(f"Cleanup warning: {e}")
    
    def test_real_database_connection(self):
        """Test real database connection"""
        # Test connection
        client = get_mongodb_client()
        assert client is not None
        
        # Test database access
        database = get_mongodb_database("unifly_test")
        assert database is not None
        
        # Test collection access
        collection = get_mongodb_collection("unifly_test", self.test_collection_name)
        assert collection is not None
        assert collection.name == self.test_collection_name
    
    def test_real_insert_operation(self):
        """Test real insert operation"""
        # Test data
        test_document = {
            "name": "Test Document",
            "value": 42,
            "status": "active",
            "created_at": time.time()
        }
        
        # Insert document
        insert_result = insert(self.test_collection, test_document)
        
        # Verify insertion
        assert insert_result is not None
        assert isinstance(insert_result, InsertOneResult)
        assert insert_result.inserted_id is not None
        assert isinstance(insert_result.inserted_id, ObjectId)
        assert insert_result.acknowledged is True
        
        # Verify document exists in database
        result = self.test_collection.find_one({"_id": insert_result.inserted_id})
        assert result is not None
        assert result["name"] == "Test Document"
        assert result["value"] == 42
    
    def test_real_get_one_operation(self):
        """Test real get_one operation"""
        # Insert test data
        test_document = {
            "userid": 12345,
            "name": "John Doe",
            "email": "john@example.com",
            "status": "active"
        }
        
        insert_result = insert(self.test_collection, test_document)
        assert insert_result is not None
        
        # Test get_one with filters
        result = get_one(self.test_collection, {"userid": 12345})
        
        # Verify result
        assert result is not None
        assert result["userid"] == 12345
        assert result["name"] == "John Doe"
        assert result["email"] == "john@example.com"
        assert "_id" not in result  # Should be removed by get_one
    
    def test_real_get_many_operation(self):
        """Test real get_many operation"""
        # Insert multiple test documents
        test_documents = [
            {"userid": 1, "name": "Alice", "status": "active"},
            {"userid": 2, "name": "Bob", "status": "inactive"},
            {"userid": 3, "name": "Charlie", "status": "active"},
            {"userid": 4, "name": "David", "status": "active"}
        ]
        
        for doc in test_documents:
            insert_result = insert(self.test_collection, doc)
            assert insert_result is not None
        
        # Test get_many with filters
        active_users = get_many(self.test_collection, {"status": "active"})
        
        # Verify results
        assert len(active_users) == 3
        assert all(user["status"] == "active" for user in active_users)
        assert all("_id" not in user for user in active_users)
        
        # Test pagination
        paginated_users = get_many(self.test_collection, {}, offset=1, limit=2)
        assert len(paginated_users) == 2
    
    def test_real_update_operation(self):
        """Test real update operation"""
        # Insert test document
        test_document = {
            "userid": 12345,
            "name": "John Doe",
            "status": "inactive"
        }
        
        insert_result = insert(self.test_collection, test_document)
        assert insert_result is not None
        
        # Update document
        updated_data = {
            "userid": 12345,
            "name": "John Smith",
            "status": "active",
            "updated_at": time.time()
        }
        
        update_result = update(self.test_collection, {"userid": 12345}, updated_data)
        
        # Verify update
        assert update_result is not None
        assert isinstance(update_result, UpdateResult)
        assert update_result.modified_count == 1
        assert update_result.matched_count == 1
        assert update_result.acknowledged is True
        
        # Verify updated document
        result = get_one(self.test_collection, {"userid": 12345})
        assert result["name"] == "John Smith"
        assert result["status"] == "active"
        assert "updated_at" in result
    
    def test_real_delete_operation(self):
        """Test real delete operation with filters"""
        # Insert test documents
        test_documents = [
            {"userid": 1, "name": "Alice", "status": "active"},
            {"userid": 2, "name": "Bob", "status": "inactive"},
            {"userid": 3, "name": "Charlie", "status": "active"}
        ]
        
        for doc in test_documents:
            insert_result = insert(self.test_collection, doc)
            assert insert_result is not None
        
        # Delete inactive users
        delete_result = delete(self.test_collection, {"status": "inactive"})
        
        # Verify deletion
        assert delete_result is not None
        assert isinstance(delete_result, DeleteResult)
        assert delete_result.deleted_count == 1
        assert delete_result.acknowledged is True
        
        # Verify only active users remain
        remaining_users = get_many(self.test_collection, {})
        assert len(remaining_users) == 2
        assert all(user["status"] == "active" for user in remaining_users)
    
    def test_real_count_operation(self):
        """Test real count operation with filters"""
        # Insert test documents
        test_documents = [
            {"userid": 1, "name": "Alice", "status": "active", "role": "student"},
            {"userid": 2, "name": "Bob", "status": "inactive", "role": "student"},
            {"userid": 3, "name": "Charlie", "status": "active", "role": "teacher"},
            {"userid": 4, "name": "David", "status": "active", "role": "student"}
        ]
        
        for doc in test_documents:
            insert_result = insert(self.test_collection, doc)
            assert insert_result is not None
        
        # Test count without filters
        total_count = count(self.test_collection)
        assert total_count == 4
        
        # Test count with filters
        active_count = count(self.test_collection, {"status": "active"})
        assert active_count == 3
        
        student_count = count(self.test_collection, {"role": "student"})
        assert student_count == 3
        
        active_student_count = count(self.test_collection, {"status": "active", "role": "student"})
        assert active_student_count == 2
    
    def test_real_complex_filter_operations(self):
        """Test real complex filter operations"""
        # Insert test documents with various data
        test_documents = [
            {"userid": 1, "name": "Alice Johnson", "age": 25, "score": 85, "status": "active"},
            {"userid": 2, "name": "Bob Smith", "age": 30, "score": 92, "status": "active"},
            {"userid": 3, "name": "Charlie Brown", "age": 22, "score": 78, "status": "inactive"},
            {"userid": 4, "name": "David Wilson", "age": 28, "score": 95, "status": "active"},
            {"userid": 5, "name": "Eve Davis", "age": 35, "score": 88, "status": "active"}
        ]
        
        for doc in test_documents:
            insert_result = insert(self.test_collection, doc)
            assert insert_result is not None
        
        # Test simple filters first
        active_users = get_many(self.test_collection, {"status": "active"})
        assert len(active_users) == 4
        
        # Test exact match filters
        bob_user = get_one(self.test_collection, {"name": "Bob Smith"})
        assert bob_user is not None
        assert bob_user["score"] == 92
        
        # Test multiple conditions
        active_adults = count(self.test_collection, {
            "status": "active",
            "age": {"$gt": 25}
        })
        assert active_adults == 3
        
        # Test update operations
        update_result = update(
            self.test_collection, 
            {"userid": 2}, 
            {"honor_roll": True}
        )
        assert update_result is not None
        assert isinstance(update_result, UpdateResult)
        assert update_result.modified_count == 1
        assert update_result.matched_count == 1
        assert update_result.acknowledged is True
        
        # Verify update worked
        honor_roll_count = count(self.test_collection, {"honor_roll": True})
        assert honor_roll_count == 1
        
        # Test delete with filters
        delete_result = delete(self.test_collection, {"status": "inactive"})
        assert delete_result is not None
        assert isinstance(delete_result, DeleteResult)
        assert delete_result.deleted_count == 1
        assert delete_result.acknowledged is True
        
        # Verify deletion
        remaining_count = count(self.test_collection, {})
        assert remaining_count == 4
    
    def test_real_error_handling(self):
        """Test real error handling scenarios"""
        # Test get_one with non-existent document
        result = get_one(self.test_collection, {"userid": 99999})
        assert result is None
        
        # Test update with non-existent document
        update_result = update(
            self.test_collection, 
            {"userid": 99999}, 
            {"status": "active"}
        )
        assert update_result is not None
        assert isinstance(update_result, UpdateResult)
        assert update_result.modified_count == 0
        assert update_result.matched_count == 0
        assert update_result.acknowledged is True
        
        # Test delete with non-existent document
        delete_result = delete(self.test_collection, {"userid": 99999})
        assert delete_result is not None
        assert isinstance(delete_result, DeleteResult)
        assert delete_result.deleted_count == 0
        assert delete_result.acknowledged is True
    
    def test_real_performance_operations(self):
        """Test real performance with larger datasets"""
        # Insert multiple documents
        documents = []
        for i in range(100):
            documents.append({
                "userid": i,
                "name": f"User {i}",
                "status": "active" if i % 2 == 0 else "inactive",
                "score": i * 10,
                "created_at": time.time()
            })
        
        # Insert all documents
        start_time = time.time()
        for doc in documents:
            insert_result = insert(self.test_collection, doc)
            assert insert_result is not None
        insert_time = time.time() - start_time
        
        # Test bulk operations
        start_time = time.time()
        all_users = get_many(self.test_collection, {})
        query_time = time.time() - start_time
        
        # Test filtered operations
        start_time = time.time()
        active_users = get_many(self.test_collection, {"status": "active"})
        filter_time = time.time() - start_time
        
        # Verify results
        assert len(all_users) == 100
        assert len(active_users) == 50
        
        # Performance assertions (basic checks)
        assert insert_time < 20.0  # Should insert 100 docs in less than 20 seconds
        assert query_time < 5.0   # Should query 100 docs in less than 5 seconds
        assert filter_time < 3.0  # Should filter 100 docs in less than 3 seconds
        
        print(f"Performance metrics:")
        print(f"  Insert 100 docs: {insert_time:.3f}s")
        print(f"  Query 100 docs: {query_time:.3f}s")
        print(f"  Filter 100 docs: {filter_time:.3f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
