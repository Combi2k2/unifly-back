"""
Test suite for LangChain integration functions
Tests all LangChain operations including embeddings, LLM, and vectorstore operations
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Import the functions to test
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.integrations.internal.langchain import (
    get_langchain_embedding,
    get_langchain_qdrant,
    get_langchain_llm,
    insert_vecdb,
    delete_vecdb,
    update_vecdb
)


class TestLangChainEmbedding:
    """Test LangChain embedding functions"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Reset global embedding
        import src.integrations.internal.langchain as langchain_module
        langchain_module._embedding = None
    
    @patch('src.integrations.internal.langchain.GoogleGenerativeAIEmbeddings')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_PROVIDER', 'google_gemini')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_MODEL', 'gemini-embedding-001')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_KWARGS', {'api_key': 'test_key'})
    def test_get_langchain_embedding_google_gemini_success(self, mock_google_embeddings):
        """Test successful Google Gemini embedding creation"""
        # Mock embedding instance
        mock_embedding = Mock(spec=Embeddings)
        mock_google_embeddings.return_value = mock_embedding
        
        # Test embedding creation
        result = get_langchain_embedding()
        
        # Assertions
        assert result == mock_embedding
        mock_google_embeddings.assert_called_once_with(
            model='gemini-embedding-001',
            api_key='test_key'
        )
    
    @patch('src.integrations.internal.langchain.init_embeddings')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_PROVIDER', 'openai')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_MODEL', 'text-embedding-ada-002')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_KWARGS', {'api_key': 'test_key'})
    def test_get_langchain_embedding_other_provider_success(self, mock_init_embeddings):
        """Test successful embedding creation with other provider"""
        # Mock embedding instance
        mock_embedding = Mock(spec=Embeddings)
        mock_init_embeddings.return_value = mock_embedding
        
        # Test embedding creation
        result = get_langchain_embedding()
        
        # Assertions
        assert result == mock_embedding
        mock_init_embeddings.assert_called_once_with(
            provider='openai',
            model='text-embedding-ada-002',
            api_key='test_key'
        )
    
    @patch('src.integrations.internal.langchain.GoogleGenerativeAIEmbeddings')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_PROVIDER', 'google_gemini')
    def test_get_langchain_embedding_failure(self, mock_google_embeddings):
        """Test embedding creation failure"""
        # Mock embedding creation failure
        mock_google_embeddings.side_effect = Exception("Embedding failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Embedding failed"):
            get_langchain_embedding()
    
    @patch('src.integrations.internal.langchain.GoogleGenerativeAIEmbeddings')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_PROVIDER', 'google_gemini')
    def test_get_langchain_embedding_caching(self, mock_google_embeddings):
        """Test embedding instance caching"""
        # Mock embedding instance
        mock_embedding = Mock(spec=Embeddings)
        mock_google_embeddings.return_value = mock_embedding
        
        # Test multiple calls
        result1 = get_langchain_embedding()
        result2 = get_langchain_embedding()
        
        # Assertions
        assert result1 == result2 == mock_embedding
        # Should only be called once due to caching
        mock_google_embeddings.assert_called_once()


class TestLangChainLLM:
    """Test LangChain LLM functions"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Reset global LLM
        import src.integrations.internal.langchain as langchain_module
        langchain_module._llm = None
    
    @patch('src.integrations.internal.langchain.init_chat_model')
    @patch('src.integrations.internal.langchain.LANGCHAIN_LLM_PROVIDER', 'google_genai')
    @patch('src.integrations.internal.langchain.LANGCHAIN_LLM_MODEL', 'gemini-2.5-flash')
    @patch('src.integrations.internal.langchain.LANGCHAIN_LLM_KWARGS', {'api_key': 'test_key'})
    def test_get_langchain_llm_success(self, mock_init_chat_model):
        """Test successful LLM creation"""
        # Mock LLM instance
        mock_llm = Mock(spec=BaseChatModel)
        mock_init_chat_model.return_value = mock_llm
        
        # Test LLM creation
        result = get_langchain_llm()
        
        # Assertions
        assert result == mock_llm
        mock_init_chat_model.assert_called_once_with(
            model='gemini-2.5-flash',
            model_provider='google_genai',
            api_key='test_key'
        )
    
    @patch('src.integrations.internal.langchain.init_chat_model')
    def test_get_langchain_llm_failure(self, mock_init_chat_model):
        """Test LLM creation failure"""
        # Mock LLM creation failure
        mock_init_chat_model.side_effect = Exception("LLM failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="LLM failed"):
            get_langchain_llm()
    
    @patch('src.integrations.internal.langchain.init_chat_model')
    def test_get_langchain_llm_caching(self, mock_init_chat_model):
        """Test LLM instance caching"""
        # Mock LLM instance
        mock_llm = Mock(spec=BaseChatModel)
        mock_init_chat_model.return_value = mock_llm
        
        # Test multiple calls
        result1 = get_langchain_llm()
        result2 = get_langchain_llm()
        
        # Assertions
        assert result1 == result2 == mock_llm
        # Should only be called once due to caching
        mock_init_chat_model.assert_called_once()


class TestLangChainQdrant:
    """Test LangChain Qdrant functions"""
    
    @patch('src.integrations.internal.langchain.get_langchain_embedding')
    @patch('src.integrations.internal.langchain.create_collection')
    @patch('src.integrations.internal.langchain.exists_collection')
    @patch('src.integrations.internal.langchain.get_qdrant_client')
    @patch('src.integrations.internal.langchain.QdrantVectorStore')
    @patch('src.integrations.internal.langchain._joiner')
    def test_get_langchain_qdrant_success(self, mock_joiner, mock_qdrant, mock_get_client, mock_exists_collection, mock_create_collection, mock_get_embedding):
        """Test successful Qdrant vectorstore creation"""
        # Mock dependencies
        mock_embedding = Mock(spec=Embeddings)
        mock_get_embedding.return_value = mock_embedding
        
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_vectorstore = Mock(spec=QdrantVectorStore)
        mock_qdrant.return_value = mock_vectorstore
        
        # Mock collection doesn't exist initially
        mock_exists_collection.return_value = False
        
        # Mock joiner collection
        mock_collection = Mock()
        mock_joiner.__getitem__.return_value = mock_collection
        
        # Test Qdrant creation
        result = get_langchain_qdrant("test_collection")
        
        # Assertions
        assert result == mock_vectorstore
        mock_get_embedding.assert_called_once()
        mock_exists_collection.assert_called_once_with("test_collection")
        mock_create_collection.assert_called_once_with("test_collection", 3072)  # LANGCHAIN_EMBEDDING_SIZE
        mock_get_client.assert_called_once()
        mock_qdrant.assert_called_once_with(
            client=mock_client,
            collection_name="test_collection",
            embedding=mock_embedding
        )
    
    @patch('src.integrations.internal.langchain.get_langchain_embedding')
    def test_get_langchain_qdrant_embedding_failure(self, mock_get_embedding):
        """Test Qdrant creation with embedding failure"""
        # Mock embedding failure
        mock_get_embedding.side_effect = Exception("Embedding failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Embedding failed"):
            get_langchain_qdrant("test_collection")


class TestInsertVecDB:
    """Test insert_vecdb function"""
    
    @patch('src.integrations.internal.langchain.get_langchain_qdrant')
    @patch('src.integrations.internal.langchain._splitter')
    def test_insert_vecdb_success(self, mock_splitter, mock_get_qdrant):
        """Test successful text insertion"""
        # Mock dependencies
        mock_splitter.split_text.return_value = ["chunk1", "chunk2"]
        
        mock_vectorstore = Mock(spec=QdrantVectorStore)
        mock_vectorstore.add_texts.return_value = ["id1", "id2"]
        mock_get_qdrant.return_value = mock_vectorstore
        
        # Test data
        collection_name = "test_collection"
        text = "This is a test text that will be split into chunks."
        metadata = {"source": "test", "category": "example"}
        
        # Test insertion
        result = insert_vecdb(collection_name, text, metadata)
        
        # Assertions
        assert result == ["id1", "id2"]
        mock_splitter.split_text.assert_called_once_with(text)
        mock_get_qdrant.assert_called_once_with(collection_name)
        mock_vectorstore.add_texts.assert_called_once_with(
            ["chunk1", "chunk2"], 
            [metadata, metadata]
        )
    
    @patch('src.integrations.internal.langchain.get_langchain_qdrant')
    @patch('src.integrations.internal.langchain._splitter')
    def test_insert_vecdb_failure(self, mock_splitter, mock_get_qdrant):
        """Test insertion failure"""
        # Mock dependencies
        mock_splitter.split_text.return_value = ["chunk1"]
        mock_get_qdrant.side_effect = Exception("Qdrant failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Qdrant failed"):
            insert_vecdb("test_collection", "test text", {"test": "data"})
    
    @patch('src.integrations.internal.langchain.get_langchain_qdrant')
    @patch('src.integrations.internal.langchain._splitter')
    def test_insert_vecdb_vectorstore_failure(self, mock_splitter, mock_get_qdrant):
        """Test insertion with vectorstore failure"""
        # Mock dependencies
        mock_splitter.split_text.return_value = ["chunk1"]
        
        mock_vectorstore = Mock(spec=QdrantVectorStore)
        mock_vectorstore.add_texts.side_effect = Exception("Add texts failed")
        mock_get_qdrant.return_value = mock_vectorstore
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Add texts failed"):
            insert_vecdb("test_collection", "test text", {"test": "data"})


class TestDeleteVecDB:
    """Test delete_vecdb function"""
    
    @patch('src.integrations.internal.langchain.get_langchain_qdrant')
    @patch('src.integrations.internal.langchain._joiner')
    def test_delete_vecdb_success(self, mock_joiner, mock_get_qdrant):
        """Test successful text deletion"""
        # Mock joiner collection
        mock_collection = Mock()
        mock_joiner.__getitem__.return_value = mock_collection
        mock_collection.find.return_value = [
            {"qids": ["qid1", "qid2"], "category": "test"},
            {"qids": ["qid3"], "source": "example"}
        ]
        
        # Mock vectorstore
        mock_vectorstore = Mock(spec=QdrantVectorStore)
        mock_get_qdrant.return_value = mock_vectorstore
        
        # Test data
        collection_name = "test_collection"
        filters = {"category": "test", "source": "example"}
        
        # Test deletion
        result = delete_vecdb(collection_name, filters)
        
        # Assertions
        assert result is True
        assert mock_joiner.__getitem__.call_count == 2  # Called twice: once for find, once for delete_many
        mock_collection.find.assert_called_once_with(filters)
        mock_vectorstore.delete.assert_called_once_with(["qid1", "qid2", "qid3"])
        mock_collection.delete_many.assert_called_once_with(filters)
    
    @patch('src.integrations.internal.langchain._joiner')
    def test_delete_vecdb_empty_filters(self, mock_joiner):
        """Test delete with empty filters"""
        # Mock joiner collection with no results
        mock_collection = Mock()
        mock_joiner.__getitem__.return_value = mock_collection
        mock_collection.find.return_value = []
        
        # Test delete with empty filters
        result = delete_vecdb("test_collection", {})
        
        # Should return False when no documents found
        assert result is False
        mock_joiner.__getitem__.assert_called_once_with("test_collection")
        mock_collection.find.assert_called_once_with({})
    
    @patch('src.integrations.internal.langchain.get_langchain_qdrant')
    @patch('src.integrations.internal.langchain._joiner')
    def test_delete_vecdb_with_none_values(self, mock_joiner, mock_get_qdrant):
        """Test delete with None values in filters"""
        # Mock joiner collection
        mock_collection = Mock()
        mock_joiner.__getitem__.return_value = mock_collection
        mock_collection.find.return_value = [{"qids": ["qid1"], "category": "test"}]
        
        # Mock vectorstore
        mock_vectorstore = Mock(spec=QdrantVectorStore)
        mock_get_qdrant.return_value = mock_vectorstore
        
        # Test data with None values
        collection_name = "test_collection"
        filters = {"category": "test", "source": None, "value": 100}
        
        # Test delete
        result = delete_vecdb(collection_name, filters)
        
        # Assertions
        assert result is True
        mock_collection.find.assert_called_once_with(filters)
        mock_vectorstore.delete.assert_called_once_with(["qid1"])
        mock_collection.delete_many.assert_called_once_with(filters)
    
    @patch('src.integrations.internal.langchain._joiner')
    def test_delete_vecdb_failure(self, mock_joiner):
        """Test delete failure"""
        # Mock joiner failure
        mock_joiner.__getitem__.side_effect = Exception("Joiner failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Joiner failed"):
            delete_vecdb("test_collection", {"test": "data"})
    
    @patch('src.integrations.internal.langchain.get_langchain_qdrant')
    @patch('src.integrations.internal.langchain._joiner')
    def test_delete_vecdb_vectorstore_failure(self, mock_joiner, mock_get_qdrant):
        """Test delete with vectorstore failure"""
        # Mock joiner collection
        mock_collection = Mock()
        mock_joiner.__getitem__.return_value = mock_collection
        mock_collection.find.return_value = [{"qids": ["qid1"], "category": "test"}]
        
        # Mock vectorstore failure
        mock_get_qdrant.side_effect = Exception("Vectorstore failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Vectorstore failed"):
            delete_vecdb("test_collection", {"test": "data"})


class TestUpdateVecDB:
    """Test update_vecdb function"""
    
    @patch('src.integrations.internal.langchain.insert_vecdb')
    @patch('src.integrations.internal.langchain.delete_vecdb')
    def test_update_vecdb_success(self, mock_delete, mock_insert):
        """Test successful text update"""
        # Mock dependencies
        mock_delete.return_value = True
        mock_insert.return_value = ["id1", "id2"]
        
        # Test data
        collection_name = "test_collection"
        filters = {"category": "test"}
        text = "Updated text content"
        metadata = {"source": "updated", "category": "test"}
        
        # Test update
        result = update_vecdb(collection_name, filters, text, metadata)
        
        # Assertions
        assert result == ["id1", "id2"]
        mock_delete.assert_called_once_with(collection_name, filters)
        mock_insert.assert_called_once_with(collection_name, text, metadata)
    
    @patch('src.integrations.internal.langchain.insert_vecdb')
    @patch('src.integrations.internal.langchain.delete_vecdb')
    def test_update_vecdb_delete_failure(self, mock_delete, mock_insert):
        """Test update with delete failure"""
        # Mock delete failure
        mock_delete.side_effect = Exception("Delete failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Delete failed"):
            update_vecdb("test_collection", {"category": "test"}, "text", {"test": "data"})
    
    @patch('src.integrations.internal.langchain.insert_vecdb')
    @patch('src.integrations.internal.langchain.delete_vecdb')
    def test_update_vecdb_insert_failure(self, mock_delete, mock_insert):
        """Test update with insert failure"""
        # Mock dependencies
        mock_delete.return_value = True
        mock_insert.side_effect = Exception("Insert failed")
        
        # Test that exception is raised
        with pytest.raises(Exception, match="Insert failed"):
            update_vecdb("test_collection", {"category": "test"}, "text", {"test": "data"})


class TestLangChainIntegration:
    """Integration tests for LangChain functions"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Reset global variables
        import src.integrations.internal.langchain as langchain_module
        langchain_module._embedding = None
        langchain_module._llm = None
    
    @patch('src.integrations.internal.langchain.get_langchain_qdrant')
    @patch('src.integrations.internal.langchain._splitter')
    @patch('src.integrations.internal.langchain._joiner')
    def test_insert_and_delete_workflow(self, mock_joiner, mock_splitter, mock_get_qdrant):
        """Test complete insert and delete workflow"""
        # Mock dependencies
        mock_splitter.split_text.return_value = ["chunk1", "chunk2"]
        
        mock_vectorstore = Mock(spec=QdrantVectorStore)
        mock_vectorstore.add_texts.return_value = ["id1", "id2"]
        mock_vectorstore.delete.return_value = True
        mock_get_qdrant.return_value = mock_vectorstore
        
        # Mock joiner collection
        mock_collection = Mock()
        mock_joiner.__getitem__.return_value = mock_collection
        mock_collection.find.return_value = [{"qids": ["id1", "id2"], "category": "integration"}]
        
        # Test data
        collection_name = "test_workflow_collection"
        text = "This is a test text for workflow testing."
        metadata = {"source": "workflow_test", "category": "integration"}
        filters = {"category": "integration"}
        
        # Test insert
        insert_result = insert_vecdb(collection_name, text, metadata)
        assert insert_result == ["id1", "id2"]
        
        # Test delete
        delete_result = delete_vecdb(collection_name, filters)
        assert delete_result is True
        
        # Verify both operations were called
        mock_vectorstore.add_texts.assert_called_once()
        mock_vectorstore.delete.assert_called_once_with(["id1", "id2"])
        mock_collection.delete_many.assert_called_once_with(filters)
    
    @patch('src.integrations.internal.langchain.GoogleGenerativeAIEmbeddings')
    @patch('src.integrations.internal.langchain.init_chat_model')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_PROVIDER', 'google_gemini')
    @patch('src.integrations.internal.langchain.LANGCHAIN_LLM_PROVIDER', 'google_genai')
    def test_embedding_and_llm_workflow(self, mock_init_chat_model, mock_google_embeddings):
        """Test embedding and LLM workflow"""
        # Mock instances
        mock_embedding = Mock(spec=Embeddings)
        mock_llm = Mock(spec=BaseChatModel)
        
        mock_google_embeddings.return_value = mock_embedding
        mock_init_chat_model.return_value = mock_llm
        
        # Test both functions
        embedding_result = get_langchain_embedding()
        llm_result = get_langchain_llm()
        
        # Assertions - check that the functions were called and returned instances
        assert embedding_result is not None
        assert llm_result is not None
        assert isinstance(embedding_result, Mock)
        assert isinstance(llm_result, Mock)
        mock_google_embeddings.assert_called_once()
        mock_init_chat_model.assert_called_once()
    
    @patch('src.integrations.internal.langchain.get_langchain_qdrant')
    @patch('src.integrations.internal.langchain._splitter')
    @patch('src.integrations.internal.langchain._joiner')
    def test_full_crud_workflow(self, mock_joiner, mock_splitter, mock_get_qdrant):
        """Test complete CRUD workflow"""
        # Mock dependencies for insert
        mock_splitter.split_text.return_value = ["chunk1", "chunk2"]
        
        mock_vectorstore = Mock(spec=QdrantVectorStore)
        mock_vectorstore.add_texts.return_value = ["id1", "id2"]
        mock_vectorstore.delete.return_value = True
        mock_get_qdrant.return_value = mock_vectorstore
        
        # Mock joiner collection
        mock_collection = Mock()
        mock_joiner.__getitem__.return_value = mock_collection
        mock_collection.find.return_value = [{"qids": ["id1", "id2"], "category": "integration"}]
        
        # Test data
        collection_name = "test_crud_collection"
        text = "Test text for CRUD operations"
        metadata = {"source": "crud_test", "category": "integration"}
        filters = {"category": "integration"}
        query = "test query"
        
        # Test CRUD operations
        # Create
        insert_result = insert_vecdb(collection_name, text, metadata)
        assert insert_result == ["id1", "id2"]
        
        # Delete
        delete_result = delete_vecdb(collection_name, filters)
        assert delete_result is True
        
        # Verify all operations were called
        mock_vectorstore.add_texts.assert_called_once()
        mock_vectorstore.delete.assert_called_once_with(["id1", "id2"])
        mock_collection.delete_many.assert_called_once_with(filters)


class TestLangChainErrorHandling:
    """Test error handling scenarios"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Reset global variables
        import src.integrations.internal.langchain as langchain_module
        langchain_module._embedding = None
        langchain_module._llm = None
    
    @patch('src.integrations.internal.langchain.GoogleGenerativeAIEmbeddings')
    @patch('src.integrations.internal.langchain.LANGCHAIN_EMBEDDING_PROVIDER', 'google_gemini')
    def test_embedding_initialization_error(self, mock_google_embeddings):
        """Test embedding initialization error"""
        # Mock initialization error
        mock_google_embeddings.side_effect = Exception("Initialization failed")
        
        # Test that exception is raised and global is reset
        with pytest.raises(Exception, match="Initialization failed"):
            get_langchain_embedding()
        
        # Verify global embedding is reset to None
        import src.integrations.internal.langchain as langchain_module
        assert langchain_module._embedding is None
    
    @patch('src.integrations.internal.langchain.init_chat_model')
    def test_llm_initialization_error(self, mock_init_chat_model):
        """Test LLM initialization error"""
        # Mock initialization error
        mock_init_chat_model.side_effect = Exception("LLM initialization failed")
        
        # Test that exception is raised and global is reset
        with pytest.raises(Exception, match="LLM initialization failed"):
            get_langchain_llm()
        
        # Verify global LLM is reset to None
        import src.integrations.internal.langchain as langchain_module
        assert langchain_module._llm is None
    
    @patch('src.integrations.internal.langchain.get_langchain_qdrant')
    @patch('src.integrations.internal.langchain._splitter')
    def test_insert_vecdb_comprehensive_error_handling(self, mock_splitter, mock_get_qdrant):
        """Test comprehensive error handling in insert_vecdb"""
        # Test text splitting error
        mock_splitter.split_text.side_effect = Exception("Text splitting failed")
        
        with pytest.raises(Exception, match="Text splitting failed"):
            insert_vecdb("test_collection", "test text", {"test": "data"})
        
        # Reset and test vectorstore error
        mock_splitter.split_text.side_effect = None
        mock_splitter.split_text.return_value = ["chunk1"]
        mock_get_qdrant.side_effect = Exception("Vectorstore creation failed")
        
        with pytest.raises(Exception, match="Vectorstore creation failed"):
            insert_vecdb("test_collection", "test text", {"test": "data"})


if __name__ == "__main__":
    pytest.main([__file__, "-v"])