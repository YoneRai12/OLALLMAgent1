"""Client for vLLM server."""
from __future__ import annotations

from typing import List, Dict, Any
import httpx

class VLLMClient:
    def __init__(self, base_url: str = "http://localhost:8002") -> None:
        self.base_url = base_url

    async def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        payload = {"prompt": messages[-1]["content"], "max_tokens": kwargs.get("max_tokens", 128)}
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.post(f"{self.base_url}/generate", json=payload)
            r.raise_for_status()
            return r.json()
