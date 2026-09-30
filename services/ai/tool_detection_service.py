"""
=========================================
NovaMind AI - Tool Detection Service
=========================================
"""

import re


class ToolDetectionService:

    @staticmethod
    def has_url(prompt: str) -> bool:

        pattern = r"(https?://\S+|www\.\S+)"

        return bool(
            re.search(
                pattern,
                prompt,
            )
        )

    @staticmethod
    def has_pdf(prompt: str) -> bool:

        prompt = prompt.lower()

        keywords = [

            "pdf",
            "document",
            "resume",
            "file",
            "report",
            "chapter",
            "page",

        ]

        return any(
            word in prompt
            for word in keywords
        )

    @staticmethod
    def needs_web_search(prompt: str) -> bool:

        prompt = prompt.lower()

        keywords = [

            "latest",
            "today",
            "news",
            "current",
            "weather",
            "stock",
            "price",
            "recent",
            "breaking",
            "live",

        ]

        return any(
            word in prompt
            for word in keywords
        )