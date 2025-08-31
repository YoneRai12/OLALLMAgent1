"""Simple retriever for ChromaDB."""
from __future__ import annotations

from typing import List
from sentence_transformers import SentenceTransformer
import chromadb

MODEL_NAME = "BAAI/bge-base-en-v1.5"
_client = chromadb.PersistentClient(path="chroma")
_collection = _client.get_or_create_collection("docs")
_embedder = SentenceTransformer(MODEL_NAME)

class Retriever:
    async def retrieve(self, query: str, k: int = 4) -> List[str]:
        q_emb = _embedder.encode([query])[0]
        res = _collection.query(query_embeddings=[q_emb], n_results=k)
        return res.get("documents", [[]])[0]
