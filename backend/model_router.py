"""Model router that selects backend based on config/model.yaml."""
from __future__ import annotations

import yaml
from pathlib import Path
from typing import List, Dict, Any

from .backends.ollama_client import OllamaClient
from .backends.llamacpp_client import LlamaCppClient
from .backends.vllm_client import VLLMClient

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "model.yaml"

class ModelRouter:
    def __init__(self) -> None:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.current = cfg.get("current", "20B")
        self.backends = cfg.get("backends", {})

    def _client(self):
        cfg = self.backends[self.current]
        engine = cfg["engine"]
        if engine == "ollama":
            return OllamaClient()
        if engine == "llamacpp":
            return LlamaCppClient()
        if engine == "vllm":
            return VLLMClient()
        raise ValueError(f"Unknown engine {engine}")

    async def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        client = self._client()
        cfg = self.backends[self.current]
        return await client.chat(messages, model=cfg.get("model"), **kwargs)
