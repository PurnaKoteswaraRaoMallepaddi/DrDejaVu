"""ChromaDB vector store for consultation embeddings."""

import chromadb
from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2

from app.config import settings

_client = None
_collection = None


def get_chroma_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return _client


def _get_embedding_function() -> ONNXMiniLM_L6_V2:
    """Create embedding function using CPU-only ONNX provider to avoid compiler errors."""
    return ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])


def get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name="consultations",
            metadata={"hnsw:space": "cosine"},
            embedding_function=_get_embedding_function(),
        )
    return _collection
