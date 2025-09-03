"""Utility to load tool schema JSON."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any

TOOLS_PATH = Path(__file__).with_name("tools_schema.json")

def load_tools() -> List[Dict[str, Any]]:
    with TOOLS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
