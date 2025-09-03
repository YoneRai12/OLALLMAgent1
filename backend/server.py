"""FastAPI server exposing unified endpoints."""
from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from .model_router import ModelRouter
from .metrics import router as metrics_router
from rag.retriever import Retriever

app = FastAPI()
app.include_router(metrics_router)
router = ModelRouter()
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
retriever = Retriever()

@app.post("/chat")
async def chat(messages: List[Dict[str, str]], tools: List[Dict[str, Any]] | None = None, model: str | None = None):
    result = await router.chat(messages)
    return JSONResponse(result)

@app.post("/file/upload")
async def file_upload(file: UploadFile = File(...)):
    fid = uuid.uuid4().hex
    dest = uploads_dir / fid
    dest.write_bytes(await file.read())
    return {"id": fid}

@app.get("/file/{fid}")
async def file_get(fid: str):
    path = uploads_dir / fid
    if not path.exists():
        raise HTTPException(404, "File not found")
    return FileResponse(path)

@app.post("/rag/query")
async def rag_query(query: str):
    results = await retriever.retrieve(query)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
