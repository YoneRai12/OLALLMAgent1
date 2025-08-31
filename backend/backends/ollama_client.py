"""Client for Ollama backend."""
from __future__ import annotations

from typing import List, Dict, Any
import httpx

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url

    async def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        payload = {"model": kwargs.get("model", "gpt-oss-20b-q4_k_m"), "messages": messages}
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.post(f"{self.base_url}/api/chat", json=payload)
            r.raise_for_status()
            return r.json()
