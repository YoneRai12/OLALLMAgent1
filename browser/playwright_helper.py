"""Helpers for Playwright interactions."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright

class BrowserSession:
    def __init__(self) -> None:
        self.browser = None
        self.page = None

    async def __aenter__(self):
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.browser.close()
        await self.pw.stop()

    async def browse(self, url: str):
        await self.page.goto(url)

    async def scroll(self, pixels: Optional[int] = None, to: Optional[str] = None):
        if to == "top":
            await self.page.evaluate("window.scrollTo(0,0)")
        elif to == "bottom":
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        elif pixels:
            await self.page.evaluate(f"window.scrollBy(0, {pixels})")

    async def click(self, selector: Optional[str] = None, x: float | None = None, y: float | None = None):
        if selector:
            await self.page.click(selector)
        elif x is not None and y is not None:
            await self.page.mouse.click(x, y)

    async def type(self, selector: str, text: str, submit: bool = False):
        await self.page.fill(selector, text)
        if submit:
            await self.page.press(selector, "Enter")

    async def wait_for(self, selector: Optional[str] = None, milliseconds: Optional[int] = None):
        if selector:
            await self.page.wait_for_selector(selector)
        elif milliseconds:
            await asyncio.sleep(milliseconds / 1000)

    async def screenshot(self, path: str):
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        await self.page.screenshot(path=str(p))
