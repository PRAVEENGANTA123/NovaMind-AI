"""
=========================================
NovaMind AI - Tool Router
=========================================
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ExecutionPlan:

    agent: str

    tools: List[str]

    steps: List[str]
class RouterService:

    @staticmethod
    def create_plan(intent_result):

        steps = []

        for tool in intent_result.tools:

            if tool == "memory":

                steps.append(
                    "Load Conversation Memory"
                )

            elif tool == "pdf":

                steps.append(
                    "Read Uploaded PDF"
                )

            elif tool == "web":

                steps.append(
                    "Search Internet"
                )

            elif tool == "vision":

                steps.append(
                    "Analyze Image"
                )

            elif tool == "python":

                steps.append(
                    "Run Python Analysis"
                )

            elif tool == "reasoning":

                steps.append(
                    "Automatic Reasoning"
                )

        steps.append("Generate AI Response")

        return ExecutionPlan(

            agent=intent_result.agent,

            tools=intent_result.tools,

            steps=steps,

        )