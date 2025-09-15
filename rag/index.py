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
    texts_list = list(texts)
    if not texts_list:
        return

    embeddings = _embedder.encode(texts_list)
    start = _collection.count()
    ids = [str(i) for i in range(start, start + len(texts_list))]
    _collection.add(ids=ids, embeddings=embeddings, documents=texts_list)
