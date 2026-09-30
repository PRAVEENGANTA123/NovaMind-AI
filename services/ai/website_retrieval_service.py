"""
NovaMind AI - Website Retrieval Service

Local retrieval over resources already discovered by URLService.
No network access is performed here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Dict, List, Optional, Sequence, Tuple
from urllib.parse import urlparse


DEFAULT_TOP_K = 6
DEFAULT_MIN_SCORE = 0.08

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "could",
    "do", "does", "for", "from", "give", "how", "i", "in", "is", "it",
    "me", "of", "on", "or", "please", "tell", "that", "the", "this",
    "to", "was", "what", "when", "where", "which", "who", "why",
    "with", "would", "you", "your",
}

NAVIGATION_PHRASES = (
    "give me the link",
    "provide the link",
    "send me the link",
    "share the link",
    "find the link",
    "find page",
    "which link",
    "which page",
    "direct link",
    "official link",
    "website link",
    "open the page",
    "where can i",
    "where do i",
    "where is the",
)

NAVIGATION_KEYWORDS = {
    "link", "links", "url", "urls", "page", "pages", "portal",
    "results", "result", "admission", "admissions", "application",
    "apply", "placement", "placements", "career", "careers",
    "hostel", "contact", "login", "registration", "register",
    "download", "downloads", "form", "forms", "fee", "fees",
}

TARGET_ALIASES = {
    "result": {
        "result", "results", "exam", "examination", "marks", "score", "scores",
    },
    "admission": {
        "admission", "admissions", "apply", "application", "applications",
    },
    "placement": {
        "placement", "placements", "career", "careers", "job", "jobs",
        "recruitment", "training", "trainingandplacements",
    },
    "hostel": {
        "hostel", "hostels", "accommodation",
    },
    "fee": {
        "fee", "fees", "payment", "payments", "tuition",
    },
    "contact": {
        "contact", "contacts", "address", "phone", "email",
    },
    "login": {
        "login", "signin", "account",
    },
    "registration": {
        "registration", "register", "signup", "enrollment",
    },
    "download": {
        "download", "downloads", "document", "documents",
        "pdf", "form", "forms",
    },
}


@dataclass
class RetrievalResult:
    url: str
    title: str
    description: str
    headings: List[str]
    content: str
    resource_type: str
    score: float
    matched_terms: List[str]
    source: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class WebsiteRetrievalService:

    # -----------------------------------------------------
    # Normalization
    # -----------------------------------------------------

    @staticmethod
    def _normalize_text(text: str) -> str:
        if not text:
            return ""
        text = str(text).lower()
        text = re.sub(r"https?://\S+", " ", text)
        text = re.sub(r"[^a-z0-9+#.\- ]+", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    @classmethod
    def _tokens(cls, text: str) -> List[str]:
        normalized = cls._normalize_text(text)
        if not normalized:
            return []

        raw = re.findall(
            r"[a-z0-9]+(?:[+#.\-][a-z0-9]+)*",
            normalized,
        )

        result = []
        for token in raw:
            if token in STOP_WORDS or len(token) <= 1:
                continue
            if token not in result:
                result.append(token)
        return result

    @staticmethod
    def _unique(items: Sequence[str]) -> List[str]:
        result = []
        seen = set()

        for item in items or []:
            value = str(item or "").strip()
            key = value.lower()
            if not value or key in seen:
                continue
            seen.add(key)
            result.append(value)

        return result

    @classmethod
    def _query_terms(cls, question: str) -> List[str]:
        terms = cls._tokens(question)
        expanded = list(terms)

        # Small semantic expansion useful for common website questions.
        expansions = {
            "placement": {"placements", "career", "careers", "training"},
            "placements": {"placement", "career", "careers", "training"},
            "admission": {"admissions", "apply", "application"},
            "admissions": {"admission", "apply", "application"},
            "result": {"results", "exam", "marks"},
            "results": {"result", "exam", "marks"},
            "fee": {"fees", "payment", "tuition"},
            "fees": {"fee", "payment", "tuition"},
            "hostel": {"hostels", "accommodation"},
            "contact": {"address", "phone", "email"},
        }

        for term in terms:
            expanded.extend(expansions.get(term, set()))

        return cls._unique(expanded)

    # -----------------------------------------------------
    # Resource normalization
    # -----------------------------------------------------

    @classmethod
    def _resource_text(cls, resource: dict) -> Dict[str, str]:
        if not isinstance(resource, dict):
            return {
                "url": "",
                "title": "",
                "description": "",
                "headings": "",
                "content": "",
                "resource_type": "HTML",
                "source": "",
            }

        headings = resource.get("headings", []) or []
        if isinstance(headings, (list, tuple, set)):
            heading_text = " ".join(str(x) for x in headings if x)
        else:
            heading_text = str(headings)

        return {
            "url": str(resource.get("url", "") or "").strip(),
            "title": str(resource.get("title", "") or "").strip(),
            "description": str(resource.get("description", "") or "").strip(),
            "headings": heading_text.strip(),
            "content": str(resource.get("content", "") or ""),
            "resource_type": str(
                resource.get("resource_type", "HTML") or "HTML"
            ),
            "source": str(resource.get("source", "") or ""),
        }

    # -----------------------------------------------------
    # Navigation detection
    # -----------------------------------------------------

    @classmethod
    def is_navigation_query(cls, question: str) -> bool:
        if not question:
            return False

        text = str(question).lower().strip()

        if any(phrase in text for phrase in NAVIGATION_PHRASES):
            return True

        words = set(re.findall(r"\b[a-z0-9]+\b", text))
        return bool(words.intersection(NAVIGATION_KEYWORDS))

    # -----------------------------------------------------
    # General scoring
    # -----------------------------------------------------

    @classmethod
    def _score_resource(
        cls,
        question_terms: Sequence[str],
        resource: dict,
    ) -> Tuple[float, List[str]]:
        fields = cls._resource_text(resource)

        if not question_terms or not fields["url"]:
            return 0.0, []

        title = set(cls._tokens(fields["title"]))
        headings = set(cls._tokens(fields["headings"]))
        description = set(cls._tokens(fields["description"]))
        content = set(cls._tokens(fields["content"]))
        url = set(cls._tokens(fields["url"].replace("/", " ")))

        matched = []
        title_hits = heading_hits = description_hits = 0
        content_hits = url_hits = 0

        for term in question_terms:
            hit = False

            if term in title:
                title_hits += 1
                hit = True
            if term in headings:
                heading_hits += 1
                hit = True
            if term in description:
                description_hits += 1
                hit = True
            if term in content:
                content_hits += 1
                hit = True
            if term in url:
                url_hits += 1
                hit = True

            if hit:
                matched.append(term)

        unique_terms = max(1, len(set(question_terms)))

        score = (
            title_hits * 0.28
            + heading_hits * 0.22
            + description_hits * 0.15
            + content_hits * 0.08
            + url_hits * 0.12
        ) / max(1.0, unique_terms ** 0.5)

        fields_hit = sum(
            value > 0
            for value in (
                title_hits,
                heading_hits,
                description_hits,
                content_hits,
                url_hits,
            )
        )

        if fields_hit >= 3:
            score += 0.08
        elif fields_hit == 2:
            score += 0.04

        normalized_query = cls._normalize_text(" ".join(question_terms))
        if normalized_query:
            if normalized_query in cls._normalize_text(fields["title"]):
                score += 0.20
            if normalized_query in cls._normalize_text(fields["headings"]):
                score += 0.12

        return min(1.0, max(0.0, score)), cls._unique(matched)

    # -----------------------------------------------------
    # Navigation destination scoring
    # -----------------------------------------------------

    @classmethod
    def find_navigation_resource(
        cls,
        question: str,
        resources: Optional[Sequence[dict]],
    ) -> dict:
        if not question or not resources:
            return {
                "found": False,
                "score": 0.0,
                "title": "",
                "url": "",
                "resource": None,
                "matched_targets": [],
            }

        query_words = set(re.findall(r"\b[a-z0-9]+\b", question.lower()))

        targets = [
            target
            for target, aliases in TARGET_ALIASES.items()
            if query_words.intersection(aliases)
        ]

        # "give me the placement link" must be recognized even if
        # the query uses a singular/plural variant not present verbatim.
        if not targets:
            expanded_terms = set(cls._query_terms(question))
            targets = [
                target
                for target, aliases in TARGET_ALIASES.items()
                if expanded_terms.intersection(aliases)
            ]

        if not targets:
            return {
                "found": False,
                "score": 0.0,
                "title": "",
                "url": "",
                "resource": None,
                "matched_targets": [],
            }

        best = None
        best_score = 0.0
        best_targets = []

        for resource in resources:
            if not isinstance(resource, dict):
                continue

            fields = cls._resource_text(resource)
            url = fields["url"]
            if not url:
                continue

            title = fields["title"].lower()
            headings = fields["headings"].lower()
            description = fields["description"].lower()
            content = fields["content"].lower()
            url_lower = url.lower()

            score = 0.0
            matched_targets = []

            for target in targets:
                aliases = TARGET_ALIASES[target]

                title_hits = [x for x in aliases if x in title]
                heading_hits = [x for x in aliases if x in headings]
                url_hits = [x for x in aliases if x in url_lower]
                description_hits = [x for x in aliases if x in description]
                content_hits = [x for x in aliases if x in content]

                if (
                    title_hits
                    or heading_hits
                    or url_hits
                    or description_hits
                    or content_hits
                ):
                    matched_targets.append(target)

                score += min(0.45 * len(title_hits), 0.90)
                score += min(0.30 * len(heading_hits), 0.60)
                score += min(0.45 * len(url_hits), 0.90)
                score += min(0.12 * len(description_hits), 0.24)
                score += min(0.06 * len(content_hits), 0.18)

                # Dedicated route match is stronger than body text.
                if any(
                    re.search(
                        rf"/{re.escape(alias)}(?:[./_-]|$)",
                        url_lower,
                    )
                    for alias in aliases
                ):
                    score += 0.35

            path = (urlparse(url).path or "/").lower()

            if path in {"", "/", "/index.html", "/index.php"}:
                score -= 0.20

            # Generic placement query: prefer the institution-wide page,
            # then portal/general page, and penalize department PDFs.
            if "placement" in targets:
                if any(
                    marker in url_lower
                    for marker in (
                        "trainingandplacements",
                        "training-and-placements",
                        "training_placements",
                        "placement-portal",
                        "placementportal",
                    )
                ):
                    score += 0.90

                if any(
                    marker in url_lower
                    for marker in (
                        "/cse/", "/ce/", "/chemical/", "/eee/",
                        "/ece/", "/it/", "/me/", "/mechanical/",
                        "/civil/", "/csbs/", "/csd/", "/xcsm/",
                        "/aids/", "/ai/", "/cso/",
                    )
                ):
                    score -= 0.25

                if any(
                    marker in url_lower
                    for marker in (".pdf", "/pdf/", "/pdfs/")
                ):
                    score -= 0.45

                if (
                    "placement" in title
                    and ".pdf" not in url_lower
                ):
                    score += 0.20

            if "result" in targets and "examcell" in url_lower and "/result" not in url_lower:
                score -= 0.10

            score = min(1.0, max(0.0, score))

            if score > best_score:
                best_score = score
                best = resource
                best_targets = cls._unique(matched_targets)

        if best is None or best_score < 0.30:
            return {
                "found": False,
                "score": round(best_score, 4),
                "title": "",
                "url": "",
                "resource": None,
                "matched_targets": best_targets,
            }

        return {
            "found": True,
            "score": round(best_score, 4),
            "title": str(best.get("title", "") or ""),
            "url": str(best.get("url", "") or ""),
            "resource": best,
            "matched_targets": best_targets,
        }

    # -----------------------------------------------------
    # Main retrieval
    # -----------------------------------------------------

    @classmethod
    def retrieve(
        cls,
        question: str,
        resources: Optional[Sequence[dict]] = None,
        top_k: int = DEFAULT_TOP_K,
        min_score: float = DEFAULT_MIN_SCORE,
    ) -> dict:
        question = str(question or "").strip()

        if not question:
            return {
                "success": False,
                "question": "",
                "results": [],
                "retrieved_count": 0,
                "has_evidence": False,
                "error": "Question is empty.",
            }

        resources = [
            item for item in list(resources or [])
            if isinstance(item, dict)
        ]

        if not resources:
            return {
                "success": False,
                "question": question,
                "results": [],
                "retrieved_count": 0,
                "has_evidence": False,
                "error": "No analyzed website resources are available.",
            }

        try:
            top_k = max(1, int(top_k))
        except (TypeError, ValueError):
            top_k = DEFAULT_TOP_K

        try:
            min_score = max(0.0, float(min_score))
        except (TypeError, ValueError):
            min_score = DEFAULT_MIN_SCORE

        # Navigation requests should first try the dedicated destination
        # scorer. This avoids generic body-frequency ranking selecting the
        # homepage for "give me the placement link".
        navigation = cls.find_navigation_resource(question, resources)

        query_terms = cls._query_terms(question)
        scored = []

        for index, resource in enumerate(resources):
            url = str(resource.get("url", "") or "").strip()
            if not url:
                continue

            score, matched_terms = cls._score_resource(
                query_terms,
                resource,
            )

            # Give the selected navigation destination a clear ranking boost.
            if navigation["found"] and url == navigation["url"]:
                score = max(score, navigation["score"])

            if score < min_score:
                continue

            fields = cls._resource_text(resource)
            scored.append((score, index, fields, matched_terms))

        scored.sort(key=lambda item: (-item[0], item[1]))

        selected = scored[:top_k]
        results = []

        for score, _, fields, matched_terms in selected:
            headings = [
                value.strip()
                for value in fields["headings"].split()
                if value.strip()
            ]

            results.append(
                RetrievalResult(
                    url=fields["url"],
                    title=fields["title"],
                    description=fields["description"],
                    headings=headings,
                    content=fields["content"],
                    resource_type=fields["resource_type"],
                    score=round(score, 4),
                    matched_terms=matched_terms,
                    source=fields["source"],
                ).to_dict()
            )

        # If navigation found a destination but the generic score filtered
        # it out, force that one resource into the result set.
        if navigation["found"]:
            destination_url = navigation["url"]
            if destination_url and not any(
                item.get("url") == destination_url for item in results
            ):
                destination = navigation["resource"]
                if isinstance(destination, dict):
                    fields = cls._resource_text(destination)
                    results.insert(
                        0,
                        RetrievalResult(
                            url=fields["url"],
                            title=fields["title"],
                            description=fields["description"],
                            headings=(
                                fields["headings"].split()
                                if fields["headings"]
                                else []
                            ),
                            content=fields["content"],
                            resource_type=fields["resource_type"],
                            score=navigation["score"],
                            matched_terms=navigation.get(
                                "matched_targets", []
                            ),
                            source=fields["source"],
                        ).to_dict(),
                    )
                    results = results[:top_k]

        return {
            "success": True,
            "question": question,
            "query_terms": query_terms,
            "navigation": navigation,
            "results": results,
            "retrieved_count": len(results),
            "has_evidence": bool(results),
            "error": "",
        }

    # -----------------------------------------------------
    # Gemini context
    # -----------------------------------------------------

    @classmethod
    def build_context(
        cls,
        retrieval_result: dict,
        max_content_per_resource: int = 12000,
    ) -> str:
        if not retrieval_result:
            return ""

        results = retrieval_result.get("results", []) or []
        if not results:
            return ""

        try:
            max_content_per_resource = max(
                1000,
                int(max_content_per_resource),
            )
        except (TypeError, ValueError):
            max_content_per_resource = 12000

        parts = []

        for index, item in enumerate(results, start=1):
            if not isinstance(item, dict):
                continue

            content = str(item.get("content", "") or "")
            headings = item.get("headings", []) or []

            if isinstance(headings, str):
                heading_text = headings
            else:
                heading_text = ", ".join(str(x) for x in headings if x)

            parts.append(
                "\n".join(
                    [
                        f"--- WEBSITE SOURCE {index} ---",
                        f"URL: {item.get('url', '')}",
                        f"Title: {item.get('title', '')}",
                        f"Description: {item.get('description', '')}",
                        f"Headings: {heading_text}",
                        f"Score: {item.get('score', 0)}",
                        "Retrieved Content:",
                        content[:max_content_per_resource],
                    ]
                ).strip()
            )

        return "\n\n".join(part for part in parts if part)

    # -----------------------------------------------------
    # Compatibility aliases
    # -----------------------------------------------------

    @classmethod
    def search(
        cls,
        question: str,
        resources: Optional[Sequence[dict]] = None,
        top_k: int = DEFAULT_TOP_K,
        min_score: float = DEFAULT_MIN_SCORE,
    ) -> dict:
        return cls.retrieve(
            question=question,
            resources=resources,
            top_k=top_k,
            min_score=min_score,
        )


URLRetrievalService = WebsiteRetrievalService
