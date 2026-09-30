"""
=========================================
NovaMind AI - Confidence Service
=========================================

Calculates NovaMind's confidence score using
multiple reasoning factors.

Factors:
- Intent Confidence
- Tool Availability
- Prompt Clarity
- Context Availability
- Request Complexity
"""

from dataclasses import dataclass
from typing import List


# ==========================================
# Confidence Result
# ==========================================

@dataclass
class ConfidenceResult:
    score: float

    intent_score: float
    tool_score: float
    prompt_score: float
    context_score: float
    complexity_score: float


# ==========================================
# Confidence Service
# ==========================================

class ConfidenceService:

    # -----------------------------
    # Public API
    # -----------------------------

    @staticmethod
    def calculate(intent, tools: List[str], prompt: str) -> float:
        """
        Returns only the final confidence score.
        """

        return ConfidenceService.calculate_details(
            intent,
            tools,
            prompt
        ).score

    @staticmethod
    def calculate_details(
        intent,
        tools: List[str],
        prompt: str
    ) -> ConfidenceResult:

        intent_score = ConfidenceService._intent_score(intent)

        tool_score = ConfidenceService._tool_score(tools)

        prompt_score = ConfidenceService._prompt_score(prompt)

        context_score = ConfidenceService._context_score(prompt)

        complexity_score = ConfidenceService._complexity_score(prompt)

        confidence = (
            intent_score * 0.40
            + tool_score * 0.25
            + prompt_score * 0.15
            + context_score * 0.10
            + complexity_score * 0.10
        )

        confidence = round(
            max(0.0, min(confidence, 1.0)),
            2
        )

        return ConfidenceResult(
            score=confidence,
            intent_score=round(intent_score, 2),
            tool_score=round(tool_score, 2),
            prompt_score=round(prompt_score, 2),
            context_score=round(context_score, 2),
            complexity_score=round(complexity_score, 2),
        )

    # -----------------------------
    # Individual Scores
    # -----------------------------

    @staticmethod
    def _intent_score(intent):

        return getattr(intent, "confidence", 0.80)

    @staticmethod
    def _tool_score(tools):

        if not tools:
            return 0.60

        return 1.00

    @staticmethod
    def _prompt_score(prompt):

        words = prompt.lower().split()

        score = 1.00

        if len(words) < 3:
            score -= 0.20

        vague = {
            "help",
            "fix",
            "do",
            "it",
            "this",
            "that",
            "something",
            "anything",
        }

        vague_count = sum(
            1
            for word in words
            if word in vague
        )

        score -= vague_count * 0.05

        return max(0.40, min(score, 1.00))

    @staticmethod
    def _context_score(prompt):

        prompt = prompt.lower()

        score = 0.70

        if ".pdf" in prompt:
            score += 0.10

        if "image" in prompt:
            score += 0.10

        if "csv" in prompt:
            score += 0.10

        return min(score, 1.00)

    @staticmethod
    def _complexity_score(prompt):

        words = len(prompt.split())

        if words <= 5:
            return 1.00

        if words <= 12:
            return 0.90

        if words <= 25:
            return 0.80

        return 0.70