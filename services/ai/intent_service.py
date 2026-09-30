"""
=========================================
NovaMind AI - Intent Detection Service
=========================================
"""

from dataclasses import dataclass
from typing import List


@dataclass
class IntentResult:
    intent: str
    confidence: float
    agent: str
    tools: List[str]


class IntentService:

    RULES = {

        "coding": {
            "keywords": [
                "python", "java", "javascript", "code", "coding",
                "bug", "algorithm", "flask", "django", "api",
                "sql", "html", "css", "streamlit", "langchain",
                "function", "class", "program", "debug",
            ],
            "agent": "coding_agent",
            "tools": ["reasoning", "memory"],
        },

        "pdf_analysis": {
            "keywords": [
                "pdf", "resume", "document", "summarize",
                "summary", "extract", "read", "cv",
                "job description",
            ],
            "agent": "pdf_agent",
            "tools": ["pdf", "reasoning"],
        },

        "research": {
            "keywords": [
                "research", "compare", "difference",
                "latest", "study", "investigate", "news",
            ],
            "agent": "research_agent",
            "tools": ["web", "reasoning"],
        },

        "vision": {
            "keywords": [
                "image", "photo", "picture",
                "diagram", "screenshot", "graph",
            ],
            "agent": "vision_agent",
            "tools": ["vision"],
        },

        "data_analysis": {
            "keywords": [
                "csv", "excel", "xlsx", "spreadsheet",
                "dataset", "data", "dataframe",
                "pandas", "numpy", "table",
                "report", "analytics", "analyze",
                "analysis", "chart", "plot",
                "statistics",
            ],
            "agent": "data_agent",
            "tools": ["python", "reasoning"],
        },

    }

    WEB_KEYWORDS = [
        "latest",
        "today",
        "news",
        "current",
        "weather",
        "stock",
        "price",
        "live",
        "recent",
        "breaking",
    ]

    @classmethod
    def detect(cls, prompt: str) -> IntentResult:

        prompt = prompt.lower()

        best_intent = None
        best_score = 0

        for intent, config in cls.RULES.items():

            score = sum(
                keyword in prompt
                for keyword in config["keywords"]
            )

            if score > best_score:
                best_score = score
                best_intent = (intent, config)

        if best_intent:

            intent, config = best_intent

            confidence = min(
                0.75 + (best_score * 0.08),
                0.99,
            )

            return IntentResult(
                intent=intent,
                confidence=round(confidence, 2),
                agent=config["agent"],
                tools=config["tools"],
            )

        return IntentResult(
            intent="general",
            confidence=0.60,
            agent="general_agent",
            tools=["memory"],
        )

    @classmethod
    def needs_web_search(cls, prompt: str) -> bool:

        prompt = prompt.lower()

        return any(
            keyword in prompt
            for keyword in cls.WEB_KEYWORDS
        )
    # ======================================
# URL Detection
# ======================================

@classmethod
def contains_url(cls, prompt: str) -> bool:

    prompt = prompt.lower()

    return (
        "http://" in prompt
        or "https://" in prompt
        or "www." in prompt
    )