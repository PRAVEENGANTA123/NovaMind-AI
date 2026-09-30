"""
=========================================
NovaMind AI - Reasoning Service
=========================================

Orchestrates the AI reasoning pipeline.

Pipeline:
User Prompt
    ↓
Intent Detection
    ↓
Tool Routing
    ↓
Confidence Calculation
    ↓
Reasoning Result
"""

from dataclasses import dataclass
from typing import List
from services.ai.intent_service import IntentService
from services.ai.router_service import RouterService
from services.ai.confidence_service import ConfidenceService
from services.ai.context_service import ContextService


# ==========================================
# Reasoning Result
# ==========================================

@dataclass
class ReasoningResult:
    """Result produced by the reasoning engine."""

    prompt: str
    intent: str
    confidence: float

    agent: str
    tools: List[str]
    execution_plan: List[str]

    # Future-ready fields
    complexity: str = "low"

    requires_memory: bool = False
    requires_web: bool = False
    requires_pdf: bool = False
    requires_image: bool = False
    requires_code_execution: bool = False
    context: object = None


# ==========================================
# Reasoning Service
# ==========================================

class ReasoningService:
    """
    Main AI orchestration service.

    Responsibilities:
    - Detect intent
    - Select agent
    - Select tools
    - Calculate confidence
    - Produce execution plan
    """

    @staticmethod
    def analyze(prompt: str) -> ReasoningResult:
        """
        Analyze a user prompt and create an execution plan.

        Args:
            prompt (str): User input

        Returns:
            ReasoningResult
        """

        # ----------------------------------
        # Step 1: Detect Intent
        # ----------------------------------
        intent = IntentService.detect(prompt)

        # ----------------------------------
        # Step 2: Create Execution Plan
        # ----------------------------------
        plan = RouterService.create_plan(intent)

        # ----------------------------------
        # Step 3: Calculate Confidence
        # ----------------------------------
        confidence = ConfidenceService.calculate(
            intent=intent,
            tools=plan.tools,
            prompt=prompt,
        )

        # ----------------------------------
        # Step 4: Detect Required Resources
        # ----------------------------------
        prompt_lower = prompt.lower()

        requires_pdf = ".pdf" in prompt_lower
        requires_image = any(
            word in prompt_lower
            for word in ["image", "photo", "picture"]
        )

        requires_web = (
            "search" in prompt_lower
            or "latest" in prompt_lower
            or "news" in prompt_lower
        )

        requires_memory = "memory" in plan.tools

        requires_code_execution = (
            intent.intent == "coding"
        )
        context = ContextService.build(prompt)

        # ----------------------------------
        # Step 5: Return Result
        # ----------------------------------
        return ReasoningResult(
            prompt=prompt,
            intent=intent.intent,
            confidence=confidence,

            agent=plan.agent,
            tools=plan.tools,
            execution_plan=plan.steps,
            context=context,

            complexity="low",
            requires_memory=requires_memory,
            requires_web=requires_web,
            requires_pdf=requires_pdf,
            requires_image=requires_image,
            requires_code_execution=requires_code_execution,
             
        )