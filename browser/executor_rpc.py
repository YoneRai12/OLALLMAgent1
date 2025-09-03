"""FastAPI RPC server exposing browser controls."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from .playwright_helper import BrowserSession

app = FastAPI()

@app.post('/browse')
async def browse(url: str):
    async with BrowserSession() as b:
        await b.browse(url)
    return {"status": "ok"}

@app.post('/scroll')
async def scroll(to: str | None = None, pixels: int | None = None):
    async with BrowserSession() as b:
        await b.scroll(pixels=pixels, to=to)
    return {"status": "ok"}

@app.post('/click')
async def click(selector: str | None = None, x: float | None = None, y: float | None = None):
    async with BrowserSession() as b:
        await b.click(selector=selector, x=x, y=y)
    return {"status": "ok"}

@app.post('/type')
async def type_(selector: str, text: str, submit: bool = False):
    async with BrowserSession() as b:
        await b.type(selector, text, submit)
    return {"status": "ok"}

@app.post('/wait_for')
async def wait_for(selector: str | None = None, milliseconds: int | None = None):
    async with BrowserSession() as b:
        await b.wait_for(selector, milliseconds)
    return {"status": "ok"}

@app.post('/screenshot')
async def screenshot(path: str):
    async with BrowserSession() as b:
        await b.screenshot(path)
    return {"status": "ok"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8070)
