"""
NovaMind AI - High-Performance URL & Website Intelligence Engine
===============================================================
"""

from __future__ import annotations

import asyncio
import re
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup

try:
    import trafilatura
    HAS_TRAFILATURA = True
except ImportError:
    HAS_TRAFILATURA = False

from services.ai.url_service import URLService, WebsiteDiscoveryService


class URLEngine:
    """
    Website parsing and intelligence engine for NovaMind-AI.
    """

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )

    @staticmethod
    def normalize_url(url: str) -> str:
        return WebsiteDiscoveryService.normalize_url(url)

    @staticmethod
    def is_safe_url(url: str) -> bool:
        if not url:
            return False
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        hostname = (parsed.hostname or "").lower()
        if not hostname:
            return False
        return True

    @classmethod
    def extract_main_content(cls, html: str) -> Tuple[str, str]:
        if not html:
            return "", ""

        text = ""
        if HAS_TRAFILATURA:
            try:
                text = trafilatura.extract(
                    html,
                    include_links=True,
                    include_tables=True,
                    output_format="markdown",
                ) or ""
            except Exception:
                text = ""

        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""

        if not text:
            for tag in soup.find_all(["script", "style", "noscript", "svg"]):
                tag.decompose()
            body_elem = soup.find("main") or soup.find("article") or soup.body or soup
            text = body_elem.get_text("\n", strip=True)

        return title, text

    async def analyze_website_async(self, root_url: str, query: str = "") -> dict:
        """
        Scrapes and analyzes website context asynchronously.
        Delegates to URLService to ensure complete sub-link discovery and robust extraction.
        """
        norm_url = self.normalize_url(root_url)
        if not self.is_safe_url(norm_url):
            return {"success": False, "error": "Invalid or restricted URL."}

        loop = asyncio.get_event_loop()
        discovery_res = await loop.run_in_executor(
            None, URLService.analyze, norm_url, query
        )

        if not discovery_res or not discovery_res.get("success"):
            return {
                "success": False,
                "error": discovery_res.get("error", "Could not access website root page."),
            }

        resources = discovery_res.get("resources", []) or []
        combined_markdown: List[str] = []
        sources: List[Dict[str, Any]] = []

        for r in resources:
            body = r.get("content", "") or ""
            url = r.get("url", "")
            title = r.get("title", "")
            cat = r.get("category", "🌐 General")
            if body:
                combined_markdown.append(
                    f"### Resource: {title} [{cat}]\nURL: {url}\n\n{body}\n"
                )
            if url:
                sources.append({
                    "url": url,
                    "title": title,
                    "category": cat,
                    "resource_type": r.get("resource_type", "HTML"),
                })

        combined_text = "\n\n".join(combined_markdown)
        primary_content = discovery_res.get("content", "") or combined_text

        return {
            "success": True,
            "root_url": discovery_res.get("root_url", norm_url),
            "final_url": discovery_res.get("final_url", norm_url),
            "domain": discovery_res.get("domain", ""),
            "title": discovery_res.get("title", ""),
            "description": discovery_res.get("description", ""),
            "total_pages_crawled": len(resources),
            "sources": sources,
            "resources": resources,
            "combined_content": combined_text or primary_content,
            "content": primary_content,
            "headings": discovery_res.get("headings", []),
            "website_resources": discovery_res.get("website_resources", []),
        }

    def analyze_website(self, root_url: str, query: str = "") -> dict:
        """
        Synchronous wrapper for analyze_website_async.
        """
        try:
            return asyncio.run(self.analyze_website_async(root_url, query))
        except RuntimeError:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.analyze_website_async(root_url, query))


# =========================================================
# Backward Compatibility Aliases for Orchestrator
# =========================================================
SafeAsyncURLEngine = URLEngine
SafeURLEngine = URLEngine
url_engine = URLEngine()