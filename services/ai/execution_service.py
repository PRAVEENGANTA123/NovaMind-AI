"""
=========================================
NovaMind AI - Execution Service
=========================================

Executes the execution plan generated
by PlannerService.
"""

from dataclasses import dataclass
from typing import List

from services.ai.planner_service import ExecutionPlan


# ==========================================
# Execution Result
# ==========================================

@dataclass
class ExecutionResult:

    success: bool

    completed_steps: List[str]

    outputs: List[str]

    execution_time: str


# ==========================================
# Execution Service
# ==========================================

class ExecutionService:

    @staticmethod
    def execute(plan: ExecutionPlan) -> ExecutionResult:
        """
        Execute an execution plan.

        Version 1:
        Simulates execution.

        Future:
        Will call Memory, PDF, Web,
        Python and Gemini services.
        """

        completed = []

        outputs = []

        for step in plan.steps:

            completed.append(step)

            outputs.append(f"✓ {step} completed")

        return ExecutionResult(

            success=True,

            completed_steps=completed,

            outputs=outputs,

            execution_time=plan.estimated_time,

        )