"""Context packer to fit retrieved docs into model window."""
from __future__ import annotations

from typing import List

TOKEN_PER_CHAR = 0.25  # rough estimate

def pack(docs: List[str], max_tokens: int) -> str:
    out = []
    used = 0
    for doc in docs:
        tokens = int(len(doc) * TOKEN_PER_CHAR)
        if used + tokens > max_tokens:
            break
        out.append(doc)
        used += tokens
    return "\n\n".join(out)
