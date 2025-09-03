"""Simple latency and throughput benchmark against /chat."""
from __future__ import annotations

import asyncio
import time
import httpx
import json
from pathlib import Path

async def bench(prompt: str, n_tokens: int = 128) -> dict:
    messages = [{"role": "user", "content": prompt}]
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        r = await client.post("http://localhost:8000/chat", json={"messages": messages})
    latency = time.perf_counter() - start
    data = r.json()
    tokens = len(data.get("content", "").split())
    tps = tokens / latency if latency else 0
    return {"latency": latency, "tokens": tokens, "tps": tps}

if __name__ == "__main__":
    result = asyncio.run(bench("Hello"))
    out = Path("benchmarks")
    out.mkdir(exist_ok=True)
    path = out / "latest.json"
    path.write_text(json.dumps(result, indent=2))
    print(result)
