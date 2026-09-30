"""
NovaMind AI - Deep Website URL Discovery & Intelligence Service
==============================================================
Implements Full Site Document Extraction, Anti-Bot TLS Impersonation (curl_cffi),
Sub-link Tree Mirroring, RAM TTL Caching, MongoDB Persistent Ingestion, and Grounding.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import heapq
import re
import time
from dataclasses import asdict, dataclass
from html import unescape
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

try:
    from curl_cffi import requests as curl_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False
    import requests

from bs4 import BeautifulSoup
import urllib3

from database.url_repository import URLRepository

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_TIMEOUT = 12
DEFAULT_CRAWL_TIMEOUT = 35

MAX_CONCURRENT_FETCHERS = 25
MAX_PAGES_TO_MIRROR = 160
MAX_CONTENT_PER_PAGE = 120_000

# Global In-Memory Discovery Cache (15 min TTL)
_DISCOVERY_CACHE: Dict[str, Tuple[float, dict]] = {}
CACHE_TTL_SECONDS = 900

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

SKIP_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico",
    ".bmp", ".mp3", ".wav", ".mp4", ".zip", ".rar", ".exe", ".css", ".js", ".pdf"
}

@dataclass
class WebsiteResource:
    url: str
    title: str = ""
    description: str = ""
    resource_type: str = "HTML"
    category: str = "🌐 General"
    source: str = "internal-link"
    status_code: int = 200
    word_count: int = 0
    content: str = ""
    headings: List[str] = None
    snippet: str = ""

    def __post_init__(self) -> None:
        if self.headings is None:
            self.headings = []
        if not self.snippet and self.content:
            self.snippet = self.content[:250].replace("\n", " ").strip() + "..."

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class WebsiteDiscoveryResult:
    success: bool
    root_url: str
    final_url: str = ""
    domain: str = ""
    title: str = ""
    description: str = ""
    resources: List[WebsiteResource] = None
    sitemap_urls: List[str] = None
    discovered_urls: List[str] = None
    external_links: List[str] = None
    robots_url: str = ""
    crawl_seconds: float = 0.0
    error: str = ""

    def __post_init__(self) -> None:
        self.resources = self.resources or []
        self.sitemap_urls = self.sitemap_urls or []
        self.discovered_urls = self.discovered_urls or []
        self.external_links = self.external_links or []

    def to_dict(self) -> dict:
        data = asdict(self)
        data["resources"] = [item.to_dict() for item in self.resources]
        return data

class WebsiteDiscoveryService:

    @staticmethod
    def normalize_url(url: str) -> str:
        if not url:
            return ""
        try:
            url = unescape(str(url)).strip()
            if not re.match(r"^https?://", url, re.IGNORECASE):
                url = "https://" + url
            parsed = urlparse(url)
            scheme = parsed.scheme.lower()
            if scheme not in {"http", "https"}:
                return ""
            hostname = (parsed.hostname or "").lower()
            if not hostname:
                return ""
            port = parsed.port
            netloc = hostname
            if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
                netloc = f"{hostname}:{port}"
            path = parsed.path or "/"
            path = re.sub(r"/{2,}", "/", path)
            return urlunparse((scheme, netloc, path, "", "", ""))
        except Exception:
            return ""

    @staticmethod
    def get_domain(url: str) -> str:
        try:
            domain = (urlparse(url).hostname or "").lower()
            return domain.removeprefix("www.")
        except Exception:
            return ""

    @staticmethod
    def is_same_domain(url: str, root_domain: str) -> bool:
        domain = WebsiteDiscoveryService.get_domain(url)
        if not domain or not root_domain:
            return False
        root_clean = root_domain.lower().removeprefix("www.")
        return domain == root_clean or domain.endswith("." + root_clean)

    @classmethod
    def classify_resource(cls, url: str, title: str) -> str:
        path_segments = [s for s in urlparse(url).path.split("/") if s and len(s) > 1]
        if path_segments:
            return f"📁 {path_segments[0].replace('-', ' ').replace('_', ' ').title()}"
        return "🌐 General"

    @staticmethod
    def _request(url: str, timeout: int = DEFAULT_TIMEOUT):
        if HAS_CURL_CFFI:
            try:
                resp = curl_requests.get(
                    url,
                    headers=BROWSER_HEADERS,
                    impersonate="chrome120",
                    timeout=timeout,
                    verify=False,
                )
                if resp.status_code < 400:
                    return resp
            except Exception:
                pass
        try:
            import requests
            session = requests.Session()
            session.headers.update(BROWSER_HEADERS)
            resp = session.get(url, timeout=timeout, allow_redirects=True, verify=False)
            if resp.status_code < 400:
                return resp
        except Exception:
            pass
        return None

    @classmethod
    def _extract_page_content(cls, html: str) -> Tuple[str, List[str], List[Tuple[str, str]]]:
        soup = BeautifulSoup(html, "html.parser")
        headings = [h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3", "h4"]) if h.get_text(strip=True)]
        
        links: List[Tuple[str, str]] = []
        for a in soup.find_all("a", href=True):
            href = (a.get("href") or "").strip()
            anchor_txt = a.get_text(" ", strip=True)
            if href and not href.startswith(("#", "mailto:", "tel:", "javascript:")):
                links.append((href, anchor_txt))

        for tag in soup.find_all(["script", "style", "noscript", "svg"]):
            tag.decompose()

        body_elem = soup.body or soup
        bs4_text = body_elem.get_text("\n", strip=True) if body_elem else ""

        return bs4_text[:MAX_CONTENT_PER_PAGE], headings, links

    @classmethod
    def _fetch_page(cls, res: WebsiteResource) -> WebsiteResource:
        try:
            response = cls._request(res.url, timeout=8)
            if response and response.text:
                content, headings, _ = cls._extract_page_content(response.text)
                res.content = content
                res.headings = headings
                res.word_count = len(content.split())
                if content:
                    res.snippet = content[:250].replace("\n", " ").strip() + "..."
        except Exception:
            pass
        return res

    @classmethod
    def discover(
        cls,
        url: str,
        crawl_timeout: int = DEFAULT_CRAWL_TIMEOUT,
        max_pages: Optional[int] = None,
        query: str = "",
    ) -> dict:
        root_url = cls.normalize_url(url)
        if not root_url:
            return WebsiteDiscoveryResult(success=False, root_url=url or "", error="Invalid URL").to_dict()

        root_domain = cls.get_domain(root_url)
        cache_key = root_url.lower()
        now = time.time()

        # Step 1: Check RAM Cache (Sub-millisecond)
        if cache_key in _DISCOVERY_CACHE:
            cached_time, cached_result = _DISCOVERY_CACHE[cache_key]
            if now - cached_time < CACHE_TTL_SECONDS:
                age_s = round(now - cached_time, 1)
                print("=" * 65)
                print(f"⚡ RAM CACHE HIT: Reusing discovery for {root_domain} ({age_s}s old)")
                print("=" * 65)
                return cached_result

        # Step 2: Check MongoDB Persistent Store
        db_record = URLRepository.get_cached_site(root_domain)
        if db_record and isinstance(db_record.get("data"), dict):
            cached_result = db_record["data"]
            _DISCOVERY_CACHE[cache_key] = (now, cached_result)
            print("=" * 65)
            print(f"💾 MONGODB CACHE HIT: Reusing stored discovery for {root_domain}")
            print("=" * 65)
            return cached_result

        # Step 3: Execute Fresh Multi-Worker Live Crawl
        started = time.monotonic()
        print("=" * 65)
        print(f"🌐 NOVAMIND DISCOVERY: {root_domain}")
        if query:
            print(f"🎯 QUERY TARGET: {query}")
        print("=" * 65)

        response = cls._request(root_url, timeout=DEFAULT_TIMEOUT)
        if response is None:
            return WebsiteDiscoveryResult(success=False, root_url=root_url, error="Could not reach site").to_dict()

        final_root_url = cls.normalize_url(response.url) or root_url
        root_content, root_headings, root_links = cls._extract_page_content(response.text or "")

        soup = BeautifulSoup(response.text or "", "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else root_domain
        desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.IGNORECASE)})
        description = (desc_tag.get("content", "") or "").strip() if desc_tag else ""

        root_resource = WebsiteResource(
            url=final_root_url,
            title=title,
            description=description,
            category="ℹ️ Root Portal",
            source="root",
            status_code=response.status_code,
            word_count=len(root_content.split()),
            content=root_content,
            headings=root_headings,
        )

        resources: List[WebsiteResource] = [root_resource]
        seen_urls: Set[str] = {final_root_url, root_url}

        sub_hubs = []
        for href, anchor_text in root_links:
            full_link = cls.normalize_url(urljoin(final_root_url, href))
            if not full_link or full_link in seen_urls:
                continue
            if any(full_link.lower().endswith(ext) for ext in SKIP_EXTENSIONS):
                continue
            if cls.is_same_domain(full_link, root_domain):
                seen_urls.add(full_link)
                path_slug = urlparse(full_link).path.strip("/").replace("-", " ").replace("_", " ").replace("/", " - ")
                link_title = anchor_text if (anchor_text and len(anchor_text) > 2) else (path_slug.title() if path_slug else "Portal Page")
                
                resources.append(WebsiteResource(
                    url=full_link,
                    title=link_title,
                    category=cls.classify_resource(full_link, link_title),
                    resource_type="HTML",
                    source="homepage-menu",
                    status_code=200,
                ))
                if any(k in full_link.lower() for k in ["series", "simulcast", "calendar", "videos", "browse", "school", "engineering", "sciences", "faculty", "department", "anime", "news"]):
                    sub_hubs.append(full_link)

        def expand_hub(hub_url: str) -> List[WebsiteResource]:
            expanded = []
            try:
                hub_clean = hub_url.rstrip("/") + "/"
                resp = cls._request(hub_url, timeout=6)
                if resp and resp.text:
                    _, _, child_links = cls._extract_page_content(resp.text)
                    for ch_href, ch_anchor in child_links:
                        ch_full = cls.normalize_url(urljoin(hub_clean, ch_href))
                        if ch_full and cls.is_same_domain(ch_full, root_domain):
                            if not any(ch_full.lower().endswith(ext) for ext in SKIP_EXTENSIONS):
                                ch_slug = urlparse(ch_full).path.strip("/").replace("-", " ").replace("_", " ").replace("/", " - ")
                                ch_title = ch_anchor if (ch_anchor and len(ch_anchor) > 2) else (ch_slug.title() if ch_slug else "Sub Page")
                                expanded.append(WebsiteResource(
                                    url=ch_full,
                                    title=ch_title,
                                    category=cls.classify_resource(ch_full, ch_title),
                                    resource_type="HTML",
                                    source="sub-hub",
                                    status_code=200
                                ))
            except Exception:
                pass
            return expanded

        if sub_hubs:
            with ThreadPoolExecutor(max_workers=10) as executor:
                hub_results = executor.map(expand_hub, sub_hubs)
                for res_list in hub_results:
                    for item in res_list:
                        if item.url not in seen_urls:
                            seen_urls.add(item.url)
                            resources.append(item)

        stop_words = {"what", "tell", "about", "give", "show", "where", "which", "how", "who", "the", "and", "for", "with", "this", "is", "are"}
        raw_tokens = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
        query_tokens = [t for t in raw_tokens if t not in stop_words]

        candidates = []
        for r in resources[1:]:
            score = 0.0
            haystack = f"{r.url} {r.title} {r.category}".lower()

            for token in query_tokens:
                if token in haystack:
                    score += 200.0

            if any(k in haystack for k in ["calendar", "simulcast", "series", "anime", "episodes", "faculty", "staff"]):
                score += 100.0
            else:
                score += 10.0

            candidates.append((score, r))

        candidates.sort(key=lambda x: x[0], reverse=True)
        top_to_fetch = [r for _, r in candidates[:MAX_PAGES_TO_MIRROR]]

        if top_to_fetch:
            print(f"📥 Mirroring content from {len(top_to_fetch)} indexed subpages using {MAX_CONCURRENT_FETCHERS} parallel workers...")
            with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_FETCHERS) as executor:
                futures = [executor.submit(cls._fetch_page, r) for r in top_to_fetch]
                for f in as_completed(futures):
                    try:
                        f.result()
                    except Exception:
                        pass

        elapsed = time.monotonic() - started
        loaded_count = len([r for r in resources if r.content])
        print(f"✅ Discovered {len(resources)} sub-links ({loaded_count} pages mirrored) in {round(elapsed, 2)}s.")

        result = WebsiteDiscoveryResult(
            success=True,
            root_url=root_url,
            final_url=final_root_url,
            domain=root_domain,
            title=title,
            description=description,
            resources=resources,
            discovered_urls=list(seen_urls),
            crawl_seconds=round(elapsed, 2),
        )
        out_dict = result.to_dict()
        if out_dict.get("success"):
            # Update RAM Cache
            _DISCOVERY_CACHE[cache_key] = (time.time(), out_dict)
            # Persist to MongoDB
            URLRepository.save_crawled_site(domain=root_domain, root_url=root_url, result_data=out_dict)
        return out_dict

class URLService:

    @classmethod
    def fetch(cls, url: str) -> dict:
        return cls.analyze(url=url)

    @classmethod
    def analyze(
        cls,
        url: str,
        query: str = "",
        max_pages: Optional[int] = None,
        crawl_timeout: int = DEFAULT_CRAWL_TIMEOUT,
    ) -> dict:
        result = WebsiteDiscoveryService.discover(
            url=url,
            crawl_timeout=crawl_timeout,
            max_pages=max_pages,
            query=query,
        )

        resources = result.get("resources", []) or []
        result["source_pages"] = [r.get("url", "") for r in resources if r.get("url")]
        result["analyzed_page_count"] = len(resources)
        result["query"] = query or ""

        root_res = resources[0] if resources else {}
        result["primary_resource"] = root_res

        combined_blocks = []
        for r in resources:
            body = r.get("content", "") or ""
            if body:
                combined_blocks.append(
                    f"=== RESOURCE START ===\nTITLE: {r.get('title', '')}\nURL: {r.get('url', '')}\nCONTENT:\n{body}\n=== RESOURCE END ==="
                )

        combined_text = "\n\n".join(combined_blocks)
        result["combined_content"] = combined_text
        result["content"] = combined_text
        result["content_length"] = len(combined_text)
        result["word_count"] = len(combined_text.split())
        result["status_code"] = root_res.get("status_code", 200)
        result["headings"] = root_res.get("headings", [])

        result["website_resources"] = [
            {
                "url": r.get("url", ""),
                "title": r.get("title", ""),
                "description": r.get("description", ""),
                "category": r.get("category", "🌐 General"),
                "resource_type": r.get("resource_type", "HTML"),
                "source": r.get("source", ""),
                "word_count": r.get("word_count", 0),
            }
            for r in resources
        ]
        return result

    @classmethod
    def process(cls, url: str, query: str = "", max_pages: Optional[int] = None, crawl_timeout: int = DEFAULT_CRAWL_TIMEOUT) -> dict:
        return cls.analyze(url=url, query=query, max_pages=max_pages, crawl_timeout=crawl_timeout)

    @classmethod
    def discover(cls, url: str, crawl_timeout: int = DEFAULT_CRAWL_TIMEOUT, max_pages: Optional[int] = None, query: str = "") -> dict:
        return cls.analyze(url=url, query=query, max_pages=max_pages, crawl_timeout=crawl_timeout)

URLDiscoveryService = WebsiteDiscoveryService

def _request(url: str, timeout: int = DEFAULT_TIMEOUT):
    return WebsiteDiscoveryService._request(url, timeout=timeout)
