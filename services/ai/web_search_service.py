"""
=========================================
NovaMind AI - Web Search Service
=========================================

Provides clean, relevant, recent and
source-aware web search results.

Supports:
    - General web search & News queries
    - Graceful fallback when over-filtered
    - Duplicate removal & domain prioritization
    - Source metadata & formatted AI context
"""

import warnings
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None


class WebSearchService:
    """
    Web Search Service for NovaMind AI.
    """

    PRIORITY_DOMAINS = {
        "reuters.com",
        "apnews.com",
        "bbc.com",
        "bbc.co.uk",
        "theguardian.com",
        "techcrunch.com",
        "arstechnica.com",
        "theverge.com",
        "wired.com",
        "ibm.com",
        "google.com",
        "blog.google",
        "openai.com",
        "anthropic.com",
        "microsoft.com",
        "meta.com",
        "nvidia.com",
        "github.com",
        "python.org",
        "docs.python.org",
        "wikipedia.org",
    }

    NEWS_DOMAINS = {
        "reuters.com",
        "apnews.com",
        "bbc.com",
        "bbc.co.uk",
        "theguardian.com",
        "techcrunch.com",
        "arstechnica.com",
        "theverge.com",
        "wired.com",
        "artificialintelligence-news.com",
        "aiweekly.co",
    }

    NEWS_KEYWORDS = {
        "latest",
        "today",
        "news",
        "breaking",
        "recent",
        "this week",
        "yesterday",
        "developments",
        "announcement",
        "announcements",
        "released",
        "launch",
        "launched",
    }

    @staticmethod
    def _normalize_url(url: str) -> str:
        if not url:
            return ""
        try:
            parsed = urlparse(url.strip())
            scheme = parsed.scheme.lower()
            hostname = (parsed.hostname or "").lower()
            path = parsed.path.rstrip("/")
            if not path:
                path = "/"
            return f"{scheme}://{hostname}{path}"
        except Exception:
            return ""

    @staticmethod
    def _domain(url: str) -> str:
        try:
            return (urlparse(url).hostname or "").lower()
        except Exception:
            return ""

    @classmethod
    def _is_priority_domain(cls, url: str) -> bool:
        domain = cls._domain(url)
        for priority in cls.PRIORITY_DOMAINS:
            if domain == priority or domain.endswith("." + priority):
                return True
        return False

    @classmethod
    def _is_news_domain(cls, url: str) -> bool:
        domain = cls._domain(url)
        for news_domain in cls.NEWS_DOMAINS:
            if domain == news_domain or domain.endswith("." + news_domain):
                return True
        return False

    @classmethod
    def _is_news_query(cls, query: str) -> bool:
        if not query:
            return False
        normalized = query.lower().strip()
        return any(keyword in normalized for keyword in cls.NEWS_KEYWORDS)

    @classmethod
    def _prepare_query(cls, query: str) -> str:
        query = (query or "").strip()
        if not query:
            return ""
        if cls._is_news_query(query):
            return f"{query} latest news"
        return query

    @staticmethod
    def _text_quality(title: str, snippet: str) -> int:
        score = 0
        if title:
            score += 2
        if snippet:
            score += 3
        if len(snippet) >= 100:
            score += 2
        if len(snippet) >= 200:
            score += 1
        return score

    @classmethod
    def _clean_results(cls, results: list, news_query: bool = False) -> List[Dict[str, Any]]:
        cleaned = []
        seen_urls = set()

        for item in results:
            if not isinstance(item, dict):
                continue

            title = (item.get("title", "") or "").strip()
            url = (item.get("href", "") or item.get("url", "") or "").strip()
            snippet = (item.get("body", "") or item.get("snippet", "") or "").strip()

            if not url:
                continue

            normalized_url = cls._normalize_url(url)
            if not normalized_url or normalized_url in seen_urls:
                continue

            seen_urls.add(normalized_url)

            priority = cls._is_priority_domain(url)
            news_domain = cls._is_news_domain(url)
            quality = cls._text_quality(title, snippet)

            score = quality
            if priority:
                score += 5
            if news_query and news_domain:
                score += 6

            cleaned.append({
                "title": title,
                "url": url,
                "snippet": snippet,
                "domain": cls._domain(url),
                "priority": priority,
                "news_source": news_domain,
                "score": score,
            })

        cleaned.sort(
            key=lambda item: (item["score"], item["priority"], item["news_source"]),
            reverse=True,
        )

        formatted = []
        for item in cleaned:
            formatted.append({
                "title": item["title"],
                "url": item["url"],
                "snippet": item["snippet"],
                "domain": item["domain"],
                "news_source": item["news_source"],
            })

        return formatted

    @classmethod
    def search(cls, query: str, max_results: int = 5) -> Dict[str, Any]:
        try:
            if not query or not query.strip():
                return {
                    "success": False,
                    "query": query,
                    "count": 0,
                    "results": [],
                    "combined_context": "",
                    "error": "Search query is empty.",
                }

            if DDGS is None:
                return {
                    "success": False,
                    "query": query,
                    "count": 0,
                    "results": [],
                    "combined_context": "",
                    "error": "DDGS module not installed. Run: pip install ddgs",
                }

            original_query = query.strip()
            news_query = cls._is_news_query(original_query)
            search_query = cls._prepare_query(original_query)

            candidate_count = max(max_results * 3, 10)

            print("=" * 60)
            print("WEB SEARCH")
            print("=" * 60)
            print("Query          :", original_query)
            print("Prepared Query :", search_query)
            print("Candidates     :", candidate_count)

            # Query with prepared query first, fallback to raw user query if empty
            results = []
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(search_query, max_results=candidate_count))
            except Exception:
                results = []

            if not results and search_query != original_query:
                print("⚠️ Fallback to raw query...")
                try:
                    with DDGS() as ddgs:
                        results = list(ddgs.text(original_query, max_results=candidate_count))
                except Exception:
                    results = []

            formatted = cls._clean_results(results, news_query=news_query)
            formatted = formatted[:max_results]

            context_blocks = []
            for idx, r in enumerate(formatted, start=1):
                context_blocks.append(
                    f"[{idx}] {r['title']}\nURL: {r['url']}\nSNIPPET: {r['snippet']}"
                )
            combined_context = "\n\n".join(context_blocks)

            print("Final Results  :", len(formatted))
            print("=" * 60)

            return {
                "success": True,
                "query": original_query,
                "search_query": search_query,
                "is_news_query": news_query,
                "count": len(formatted),
                "results": formatted,
                "combined_context": combined_context,
            }

        except Exception as e:
            print("=" * 60)
            print("WEB SEARCH ERROR:", e)
            print("=" * 60)
            return {
                "success": False,
                "query": query,
                "count": 0,
                "results": [],
                "combined_context": "",
                "error": str(e),
            }
