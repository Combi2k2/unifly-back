from shlex import join
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings

from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from src.integrations.internal.qdrant import get_qdrant_client, create_collection, exists_collection
from src.integrations.internal.mongodb import get_mongodb_collection
from src.config import (
    LANGCHAIN_EMBEDDING_PROVIDER,
    LANGCHAIN_EMBEDDING_MODEL,
    LANGCHAIN_EMBEDDING_SIZE,
    LANGCHAIN_EMBEDDING_KWARGS,
    LANGCHAIN_LLM_PROVIDER,
    LANGCHAIN_LLM_MODEL,
    LANGCHAIN_LLM_KWARGS,
    LANGCHAIN_CHUNK_SIZE,
    LANGCHAIN_CHUNK_OVERLAP
)
from typing import Optional, Dict, Any, List
import logging

_llm: Optional[BaseChatModel] = None
_embedding: Optional[Embeddings] = None
_splitter = RecursiveCharacterTextSplitter(
    chunk_size=LANGCHAIN_CHUNK_SIZE,
    chunk_overlap=LANGCHAIN_CHUNK_OVERLAP
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_langchain_embedding() -> Embeddings:
    """
    Get LangChain embedding instance
    Creates new instance if not exists
    
    Returns:
        Embeddings instance
    """
    global _embedding

    try:
        if _embedding is None:
            if LANGCHAIN_EMBEDDING_PROVIDER == "google_gemini":
                _embedding = GoogleGenerativeAIEmbeddings(
                    model=LANGCHAIN_EMBEDDING_MODEL,
                    **LANGCHAIN_EMBEDDING_KWARGS
                )
            else:
                _embedding = init_embeddings(
                    provider=LANGCHAIN_EMBEDDING_PROVIDER,
                    model=LANGCHAIN_EMBEDDING_MODEL,
                    **LANGCHAIN_EMBEDDING_KWARGS
                )
    except Exception as e:
        logger.error(f"Failed to get LangChain embedding: {e}")
        _embedding = None
        raise
    return _embedding

def get_langchain_qdrant(collection_name: str) -> QdrantVectorStore:
    """
    Get LangChain Qdrant instance

    Args:
        collection_name: Name of the collection to create

    Returns:
        Qdrant instance
    """
    embedding = get_langchain_embedding()
    embedding_size = LANGCHAIN_EMBEDDING_SIZE

    try:
        if not exists_collection(collection_name):
            create_collection(collection_name, embedding_size)
    except Exception as e:
        logger.debug(f"Collection {collection_name} already exists")
        pass

    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=collection_name,
        embedding=embedding,
    )

def get_langchain_llm() -> BaseChatModel:
    """
    Get LangChain LLM instance
    Creates new instance if not exists
    
    Returns:
        LLM instance
    """
    global _llm

    try:
        if _llm is None:
            _llm = init_chat_model(
                model=LANGCHAIN_LLM_MODEL,
                model_provider=LANGCHAIN_LLM_PROVIDER,
                **LANGCHAIN_LLM_KWARGS
            )
            logger.info(f"LangChain LLM created successfully with model: {LANGCHAIN_LLM_PROVIDER}:{LANGCHAIN_LLM_MODEL}")
    except Exception as e:
        logger.error(f"Failed to get LangChain LLM: {e}")
        _llm = None
        raise
    return _llm

def insert_vecdb(collection_name: str, text: str, metadata: Dict[str, Any]) -> List[str]:
    """
    Add text to Qdrant collection

    Args:
        collection_name: Name of the collection to add text to
        text: Text to add to Qdrant
        metadata: Metadata to add to Qdrant

    Returns:
        List of IDs of the added texts
    """
    texts = _splitter.split_text(text)
    try:
        vectorstore = get_langchain_qdrant(collection_name)
        result = vectorstore.add_texts(texts, [metadata for _ in texts])
        joiner = get_mongodb_collection("joiner", collection_name)
        joiner.insert_one({
            **metadata,
            "qids": result
        })
        logger.info(f"Added text to Qdrant collection: {collection_name}")
        return result
    except Exception as e:
        logger.error(f"Failed to add text to Qdrant: {e}")
        raise

def delete_vecdb(collection_name: str, filters: Dict[str, Any]) -> bool:
    """
    Delete text from Qdrant collection

    Args:
        collection_name: Name of the collection to delete text from
        filters: Filters to delete text from Qdrant

    Returns:
        True if successful, False otherwise
    """
    try:
        joiner = get_mongodb_collection("joiner", collection_name)
        docs = joiner.find(filters)
        qids = [item for doc in docs for item in doc["qids"]]

        if len(qids) > 0:
            vectorstore = get_langchain_qdrant(collection_name)
            vectorstore.delete(qids)
            joiner.delete_many(filters)
            logger.info(f"Deleted texts from Qdrant collection: {collection_name}")
            return True
        else:
            logger.warning(f"No texts found to delete from Qdrant collection: {collection_name}")
            return False
    except Exception as e:
        logger.error(f"Failed to delete text from Qdrant: {e}")
        raise

def update_vecdb(collection_name: str, filters: Dict[str, Any], text: str, metadata: Dict[str, Any]) -> List[str]:
    """
    Update text in Qdrant collection

    Args:
        collection_name: Name of the collection to update text in
        filters: Filters to update text in Qdrant
        text: Text to update in Qdrant
        metadata: Metadata to update in Qdrant
    
    Returns:
        List of IDs of the updated texts
    """
    try:
        delete_vecdb(collection_name, filters)
        result = insert_vecdb(collection_name, text, metadata)
        logger.info(f"Updated text in Qdrant collection: {collection_name}")
        return result
    except Exception as e:
        logger.error(f"Failed to update text in Qdrant: {e}")
        raise
