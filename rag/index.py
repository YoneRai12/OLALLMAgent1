"""Indexing utilities for ChromaDB."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable
from sentence_transformers import SentenceTransformer
import chromadb

MODEL_NAME = "BAAI/bge-base-en-v1.5"
CHROMA_DIR = Path("chroma")
CHROMA_DIR.mkdir(exist_ok=True)

_embedder = SentenceTransformer(MODEL_NAME)
_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
_collection = _client.get_or_create_collection("docs")

async def add_texts(texts: Iterable[str]) -> None:
    embeddings = _embedder.encode(list(texts))
    ids = [str(i) for i in range(_collection.count(), _collection.count() + len(texts))]
    _collection.add(ids=ids, embeddings=embeddings, documents=list(texts))
