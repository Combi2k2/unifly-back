"""
Test suite for Qdrant integration functions
Tests all client management and collection operations
"""

import pytest
import os
from unittest.mock import Mock, patch
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.exceptions import UnexpectedResponse

# Import the functions to test
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.integrations.internal.qdrant import (
    get_qdrant_client,
    create_collection,
    delete_collection,
    close_qdrant_connection,
    check_qdrant_connection,
    reconnect_qdrant,
    get_collection_info
)

class TestQdrantClient:
    """Test Qdrant client management functions"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Reset global client
        import src.integrations.internal.qdrant as qdrant_module
        qdrant_module._client = None
    
    def teardown_method(self):
        """Cleanup after each test method"""
        close_qdrant_connection()
    
    @patch('src.integrations.internal.qdrant.QdrantClient')
    def test_get_qdrant_client_success_with_url_and_key(self, mock_qdrant_client):
        """Test successful Qdrant client creation with URL and key"""
        # Mock the client instance
        mock_client_instance = Mock()
        mock_qdrant_client.return_value = mock_client_instance
        mock_client_instance.get_collections.return_value = Mock()
        
        # Mock config values
        with patch('src.integrations.internal.qdrant.QDRANT_URL', 'https://test.qdrant.io'):
            with patch('src.integrations.internal.qdrant.QDRANT_KEY', 'test_key'):
                # Test client creation
                client = get_qdrant_client()
                
                # Assertions
                assert client == mock_client_instance
                mock_qdrant_client.assert_called_once_with(
                    url='https://test.qdrant.io',
                    api_key='test_key',
                    timeout=10
                )
                mock_client_instance.get_collections.assert_called_once()
    
    @patch('src.integrations.internal.qdrant.QdrantClient')
    def test_get_qdrant_client_success_with_url_only(self, mock_qdrant_client):
        """Test successful Qdrant client creation with URL only"""
        # Mock the client instance
        mock_client_instance = Mock()
        mock_qdrant_client.return_value = mock_client_instance
        mock_client_instance.get_collections.return_value = Mock()
        
        # Mock config values
        with patch('src.integrations.internal.qdrant.QDRANT_URL', 'https://test.qdrant.io'):
            with patch('src.integrations.internal.qdrant.QDRANT_KEY', None):
                # Test client creation
                client = get_qdrant_client()
                
                # Assertions
                assert client == mock_client_instance
                mock_qdrant_client.assert_called_once_with(
                    url='https://test.qdrant.io',
                    timeout=10
                )
    
    @patch('src.integrations.internal.qdrant.QdrantClient')
    def test_get_qdrant_client_success_localhost(self, mock_qdrant_client):
        """Test successful Qdrant client creation with localhost fallback"""
        # Mock the client instance
        mock_client_instance = Mock()
        mock_qdrant_client.return_value = mock_client_instance
        mock_client_instance.get_collections.return_value = Mock()
        
        # Mock config values (no URL)
        with patch('src.integrations.internal.qdrant.QDRANT_URL', None):
            with patch('src.integrations.internal.qdrant.QDRANT_KEY', None):
                # Test client creation
                client = get_qdrant_client()
                
                # Assertions
                assert client == mock_client_instance
                mock_qdrant_client.assert_called_once_with(
                    host="localhost",
                    port=6333,
                    timeout=10
                )
    
    @patch('src.integrations.internal.qdrant.QdrantClient')
    def test_get_qdrant_client_connection_failure(self, mock_qdrant_client):
        """Test Qdrant client creation with connection failure"""
        # Mock connection failure
        mock_qdrant_client.side_effect = Exception("Connection failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Connection failed"):
            get_qdrant_client()
    
    @patch('src.integrations.internal.qdrant.QdrantClient')
    def test_get_qdrant_client_get_collections_failure(self, mock_qdrant_client):
        """Test Qdrant client creation with get_collections failure"""
        # Mock client instance
        mock_client_instance = Mock()
        mock_qdrant_client.return_value = mock_client_instance
        mock_client_instance.get_collections.side_effect = Exception("Collections failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Collections failed"):
            get_qdrant_client()
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_create_collection_success(self, mock_get_client):
        """Test successful collection creation"""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Test collection creation
        result = create_collection("test_collection", vector_size=384, distance=Distance.COSINE)
        
        # Assertions
        assert result is True
        mock_client.create_collection.assert_called_once()
        call_args = mock_client.create_collection.call_args
        assert call_args[1]['collection_name'] == "test_collection"
        assert call_args[1]['vectors_config'].size == 384
        assert call_args[1]['vectors_config'].distance == Distance.COSINE
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_create_collection_failure(self, mock_get_client):
        """Test collection creation failure"""
        # Mock client failure
        mock_get_client.side_effect = Exception("Client failed")
        
        # Test collection creation
        result = create_collection("test_collection")
        
        # Assertions
        assert result is False
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_delete_collection_success(self, mock_get_client):
        """Test successful collection deletion"""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Test collection deletion
        result = delete_collection("test_collection")
        
        # Assertions
        assert result is True
        mock_client.delete_collection.assert_called_once_with("test_collection")
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_delete_collection_failure(self, mock_get_client):
        """Test collection deletion failure"""
        # Mock client failure
        mock_get_client.side_effect = Exception("Client failed")
        
        # Test collection deletion
        result = delete_collection("test_collection")
        
        # Assertions
        assert result is False
    
    def test_close_qdrant_connection(self):
        """Test closing Qdrant connection"""
        # Mock client
        mock_client = Mock()
        import src.integrations.internal.qdrant as qdrant_module
        qdrant_module._client = mock_client
        
        # Test connection close
        close_qdrant_connection()
        
        # Assertions
        assert qdrant_module._client is None
    
    def test_close_qdrant_connection_no_client(self):
        """Test closing connection when no client exists"""
        # Ensure no client
        import src.integrations.internal.qdrant as qdrant_module
        qdrant_module._client = None
        
        # Should not raise exception
        close_qdrant_connection()
    
    @patch('src.integrations.internal.qdrant._client')
    def test_check_qdrant_connection_success(self, mock_client):
        """Test successful connection check"""
        # Mock successful get_collections
        mock_client.get_collections.return_value = Mock()
        
        # Test connection check
        result = check_qdrant_connection()
        
        # Assertions
        assert result is True
        mock_client.get_collections.assert_called_once()
    
    def test_check_qdrant_connection_no_client(self):
        """Test connection check when no client exists"""
        # Mock client as None
        import src.integrations.internal.qdrant as qdrant_module
        qdrant_module._client = None
        
        # Test connection check
        result = check_qdrant_connection()
        
        # Assertions
        assert result is False
    
    @patch('src.integrations.internal.qdrant._client')
    def test_check_qdrant_connection_exception(self, mock_client):
        """Test connection check with exception"""
        # Mock get_collections failure
        mock_client.get_collections.side_effect = Exception("Collections failed")
        
        # Test connection check
        result = check_qdrant_connection()
        
        # Assertions
        assert result is False
    
    @patch('src.integrations.internal.qdrant.close_qdrant_connection')
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_reconnect_qdrant(self, mock_get_client, mock_close):
        """Test Qdrant reconnection"""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Test reconnection
        result = reconnect_qdrant()
        
        # Assertions
        assert result == mock_client
        mock_close.assert_called_once()
        mock_get_client.assert_called_once()


class TestCollectionOperations:
    """Test collection operations"""
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_get_collection_info_success(self, mock_get_client):
        """Test successful collection info retrieval"""
        # Mock client and collection info
        mock_client = Mock()
        mock_collection_info = Mock()
        mock_collection_info.config.params.vectors.size = 384
        mock_collection_info.config.params.vectors.distance = Distance.COSINE
        mock_collection_info.points_count = 100
        mock_collection_info.status = "green"
        mock_client.get_collection.return_value = mock_collection_info
        mock_get_client.return_value = mock_client
        
        # Test collection info
        result = get_collection_info("test_collection")
        
        # Assertions
        expected = {
            "name": "test_collection",
            "vector_size": 384,
            "distance": Distance.COSINE,
            "points_count": 100,
            "status": "green"
        }
        assert result == expected
        mock_client.get_collection.assert_called_once_with("test_collection")
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_get_collection_info_failure(self, mock_get_client):
        """Test collection info retrieval failure"""
        # Mock client failure
        mock_get_client.side_effect = Exception("Client failed")
        
        # Test collection info
        result = get_collection_info("test_collection")
        
        # Assertions
        assert result is None
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_get_collection_info_collection_not_found(self, mock_get_client):
        """Test collection info when collection doesn't exist"""
        # Mock client with collection not found
        mock_client = Mock()
        mock_client.get_collection.side_effect = Exception("Collection not found")
        mock_get_client.return_value = mock_client
        
        # Test collection info
        result = get_collection_info("nonexistent_collection")
        
        # Assertions
        assert result is None


class TestIntegration:
    """Integration tests for Qdrant functions"""
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_full_collection_workflow(self, mock_get_client):
        """Test complete collection management workflow"""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock collection info
        mock_collection_info = Mock()
        mock_collection_info.config.params.vectors.size = 384
        mock_collection_info.config.params.vectors.distance = Distance.COSINE
        mock_collection_info.points_count = 0
        mock_collection_info.status = "green"
        mock_client.get_collection.return_value = mock_collection_info
        
        # Test workflow
        collection_name = "test_workflow_collection"
        
        # Create collection
        create_result = create_collection(collection_name, vector_size=384)
        assert create_result is True
        mock_client.create_collection.assert_called_once()
        
        # Get collection info
        info = get_collection_info(collection_name)
        assert info is not None
        assert info["name"] == collection_name
        assert info["vector_size"] == 384
        assert info["distance"] == Distance.COSINE
        
        # Delete collection
        delete_result = delete_collection(collection_name)
        assert delete_result is True
        mock_client.delete_collection.assert_called_once_with(collection_name)
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_client_reconnection_workflow(self, mock_get_client):
        """Test client reconnection workflow"""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Test reconnection
        result = reconnect_qdrant()
        
        # Assertions
        assert result == mock_client
        mock_get_client.assert_called_once()
    
    @patch('src.integrations.internal.qdrant._client')
    def test_connection_health_check_workflow(self, mock_client):
        """Test connection health check workflow"""
        # Mock successful connection
        mock_client.get_collections.return_value = Mock()
        
        # Test connection check
        result = check_qdrant_connection()
        assert result is True
        
        # Test with connection failure
        mock_client.get_collections.side_effect = Exception("Connection lost")
        result = check_qdrant_connection()
        assert result is False


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @patch('src.integrations.internal.qdrant.QdrantClient')
    def test_client_creation_with_unexpected_response(self, mock_qdrant_client):
        """Test client creation with unexpected response error"""
        # Mock unexpected response error
        mock_qdrant_client.side_effect = UnexpectedResponse("Unexpected response", 500, "content", {})
        
        # Test that exception is raised
        with pytest.raises(UnexpectedResponse):
            get_qdrant_client()
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_create_collection_with_invalid_parameters(self, mock_get_client):
        """Test collection creation with invalid parameters"""
        # Mock client
        mock_client = Mock()
        mock_client.create_collection.side_effect = Exception("Invalid parameters")
        mock_get_client.return_value = mock_client
        
        # Test collection creation
        result = create_collection("test_collection", vector_size=-1)
        
        # Assertions
        assert result is False
    
    @patch('src.integrations.internal.qdrant.get_qdrant_client')
    def test_delete_nonexistent_collection(self, mock_get_client):
        """Test deletion of nonexistent collection"""
        # Mock client
        mock_client = Mock()
        mock_client.delete_collection.side_effect = Exception("Collection not found")
        mock_get_client.return_value = mock_client
        
        # Test collection deletion
        result = delete_collection("nonexistent_collection")
        
        # Assertions
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
