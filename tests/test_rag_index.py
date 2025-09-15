"""Tests for rag.index utilities."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

import sys
import types


class _StubSentenceTransformer:
    def __init__(self, _name: str) -> None:  # pragma: no cover - simple stub
        pass

    def encode(self, texts: List[str]) -> List[str]:  # pragma: no cover - simple stub
        return list(texts)


sentence_transformers_stub = types.ModuleType("sentence_transformers")
sentence_transformers_stub.SentenceTransformer = _StubSentenceTransformer
sys.modules.setdefault("sentence_transformers", sentence_transformers_stub)


class _StubCollection:
    def count(self) -> int:  # pragma: no cover - simple stub
        return 0

    def add(self, *args, **kwargs) -> None:  # pragma: no cover - simple stub
        raise NotImplementedError


class _StubClient:
    def __init__(self, *_, **__) -> None:  # pragma: no cover - simple stub
        pass

    def get_or_create_collection(self, _name: str) -> _StubCollection:  # pragma: no cover - simple stub
        return _StubCollection()


chromadb_stub = types.ModuleType("chromadb")
chromadb_stub.PersistentClient = lambda *args, **kwargs: _StubClient()  # pragma: no cover - simple stub
sys.modules.setdefault("chromadb", chromadb_stub)


sys.path.append(str(Path(__file__).resolve().parents[1]))

from rag import index


class DummyEmbedder:
    def __init__(self) -> None:
        self.recorded: List[str] | None = None

    def encode(self, texts: List[str]) -> List[str]:
        self.recorded = list(texts)
        return [f"emb:{t}" for t in texts]


class DummyCollection:
    def __init__(self) -> None:
        self.documents: List[str] = []
        self.calls: List[tuple[List[str], List[str], List[str]]] = []

    def count(self) -> int:
        return len(self.documents)

    def add(self, ids: List[str], embeddings: List[str], documents: List[str]) -> None:
        # Simulate the behaviour of ChromaDB where lengths must match.
        if not (len(ids) == len(embeddings) == len(documents)):
            raise ValueError("Length mismatch")
        self.calls.append((ids, embeddings, documents))
        self.documents.extend(documents)


def test_add_texts_consumes_iterables(monkeypatch) -> None:
    embedder = DummyEmbedder()
    collection = DummyCollection()
    monkeypatch.setattr(index, "_embedder", embedder)
    monkeypatch.setattr(index, "_collection", collection)

    asyncio.run(index.add_texts(doc for doc in ["foo", "bar"]))

    assert embedder.recorded == ["foo", "bar"]
    assert collection.calls
    ids, embeddings, documents = collection.calls[0]
    assert ids == ["0", "1"]
    assert documents == ["foo", "bar"]
    assert embeddings == ["emb:foo", "emb:bar"]


def test_add_texts_ignores_empty_iterables(monkeypatch) -> None:
    embedder = DummyEmbedder()
    collection = DummyCollection()
    monkeypatch.setattr(index, "_embedder", embedder)
    monkeypatch.setattr(index, "_collection", collection)

    asyncio.run(index.add_texts([]))

    assert embedder.recorded is None
    assert not collection.calls
