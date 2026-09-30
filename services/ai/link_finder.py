import re
from typing import List, Dict, Any
from urllib.parse import urlparse

class WebsiteLinkFinder:
    NAVIGATION_TRIGGERS = [
        r"\blink\b", r"\bwhere\b", r"\burl\b", r"\bportal\b",
        r"\bwebsite\b", r"\bpage\b", r"\bfind\b", r"\bsite\b",
        r"\bhow to (check|apply|download|access|view|get|see|find)\b",
        r"\bshow (me )?(the )?link\b", r"\bgive (me )?(the )?link\b", 
        r"\bcheck (the )?result\b", r"\bfee structure\b"
    ]

    CATEGORY_RULES = {
        "📊 Academics & Exams": [r"result", r"exam", r"syllabus", r"timetable", r"grade", r"curriculum", r"marks"],
        "🎓 Admissions & Fees": [r"admission", r"apply", r"fee", r"eligibility", r"scholarship", r"hostel", r"tuition"],
        "💼 Placements & Careers": [r"placement", r"recruit", r"career", r"internship", r"job", r"alumni", r"training"],
        "📚 Documentation & Guides": [r"doc", r"tutorial", r"api", r"guide", r"manual", r"reference", r"download"],
        "🏠 Campus & Facilities": [r"hostel", r"library", r"transport", r"sports", r"canteen", r"campus", r"lab"],
        "📞 Contact & Info": [r"contact", r"about", r"reach", r"faculty", r"directory", r"address", r"administration"]
    }

    @classmethod
    def is_navigation_intent(cls, prompt: str) -> bool:
        prompt_lower = prompt.lower()
        return any(re.search(pattern, prompt_lower) for pattern in cls.NAVIGATION_TRIGGERS)

    @classmethod
    def classify_resource(cls, url: str, title: str) -> str:
        text = f"{url} {title}".lower()
        for category, patterns in cls.CATEGORY_RULES.items():
            if any(re.search(pat, text) for pat in patterns):
                return category
        return "🌐 General Resource"

    @classmethod
    def find_direct_links(cls, query: str, resources: List[Any], top_k: int = 4) -> List[Dict[str, Any]]:
        stop_words = {"where", "can", "i", "the", "a", "an", "is", "for", "link", "url", "to", "how", "give", "me", "check", "see"}
        query_terms = set(re.findall(r"\w+", query.lower())) - stop_words
        scored_links = []

        for item in resources:
            if hasattr(item, "url"):
                url = getattr(item, "url", "")
                title = getattr(item, "title", "") or ""
                snippet = getattr(item, "snippet", "") or ""
            elif isinstance(item, dict):
                url = item.get("url", "")
                title = item.get("title", "") or ""
                snippet = item.get("snippet", "") or item.get("content", "") or ""
            else:
                continue

            if not url:
                continue

            parsed_path = urlparse(url).path.lower().replace("-", " ").replace("_", " ").replace("/", " ")
            title_lower = title.lower()
            snippet_lower = snippet.lower()

            score = 0.0
            for term in query_terms:
                if len(term) <= 2:
                    continue
                if term in title_lower:
                    score += 4.0
                if term in parsed_path:
                    score += 3.5
                if term in snippet_lower:
                    score += 1.0

            if score > 0:
                category = cls.classify_resource(url, title)
                scored_links.append({
                    "title": title.strip() if title.strip() else url,
                    "url": url,
                    "category": category,
                    "score": round(score, 2)
                })

        scored_links.sort(key=lambda x: x["score"], reverse=True)
        return scored_links[:top_k]