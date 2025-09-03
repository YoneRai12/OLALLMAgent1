"""Client for Browser Executor RPC server."""
from __future__ import annotations

from typing import Any, Dict
import httpx

class ExecutorClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8070") -> None:
        self.base_url = base_url

    async def call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/{method}"
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, json=params)
            r.raise_for_status()
            return r.json()
