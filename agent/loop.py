"""Planner-Executor loop."""
from __future__ import annotations

import asyncio
import json
from typing import List, Dict, Any

from .planner import Planner
from .executor_client import ExecutorClient
from .tools_schema import load_tools

async def run_conversation(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    tools = load_tools()
    planner = Planner()
    executor = ExecutorClient()
    response = await planner.plan(messages, tools)
    for call in response.get("tool_calls", []):
        result = await executor.call(call["name"], call["arguments"])
        call["result"] = result
    return response

if __name__ == "__main__":
    messages = [{"role": "user", "content": "Open example.com and screenshot"}]
    out = asyncio.run(run_conversation(messages))
    print(json.dumps(out, indent=2))
