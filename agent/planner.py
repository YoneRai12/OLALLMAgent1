"""Simple LLM-based planner using the unified /chat endpoint."""
from __future__ import annotations

import json
from typing import List, Dict, Any
import httpx

class Planner:
    """Planner sends conversation with tool schemas to backend and
    returns the parsed tool call.
    """

    def __init__(self, api_url: str = "http://localhost:8000/chat") -> None:
        self.api_url = api_url

    async def plan(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Send chat with tool schema and return JSON response.

        The backend is expected to return a JSON object with optional
        `tool_calls` field containing strictly valid JSON arguments.
        """
        async with httpx.AsyncClient(timeout=60) as client:
            payload = {"messages": messages, "tools": tools}
            r = await client.post(self.api_url, json=payload)
            r.raise_for_status()
            data = r.json()
        if "tool_calls" in data:
            # Ensure arguments are valid JSON
            for call in data["tool_calls"]:
                if isinstance(call.get("arguments"), str):
                    call["arguments"] = json.loads(call["arguments"])
        return data
