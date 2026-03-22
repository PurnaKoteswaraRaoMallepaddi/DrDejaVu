"""ChromaDB vector store for consultation embeddings."""

import chromadb

from app.config import settings

_client = None
_collection = None


def get_chroma_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return _client


def get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name="consultations",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection
