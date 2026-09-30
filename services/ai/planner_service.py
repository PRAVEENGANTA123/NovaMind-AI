"""
=========================================
NovaMind AI - Planner Service
=========================================

Creates execution plans based on
the detected intent.

Author : NovaMind AI
Version: 2.6
"""

from dataclasses import dataclass
from typing import List


# ==========================================
# Execution Plan
# ==========================================

@dataclass
class ExecutionPlan:

    task: str

    agent: str

    tools: List[str]

    steps: List[str]

    complexity: str

    estimated_time: str


# ==========================================
# Planner Service
# ==========================================

class PlannerService:

    PLANS = {

        "coding": {

            "task": "Software Development",

            "agent": "coding_agent",

            "tools": [
                "reasoning",
                "memory",
            ],

            "steps": [

                "Understand Requirement",

                "Design Solution",

                "Generate Code",

                "Review Code",

                "Prepare Final Response",

            ],

            "complexity": "Medium",

            "estimated_time": "3 sec",

        },

        "pdf_analysis": {

            "task": "PDF Analysis",

            "agent": "pdf_agent",

            "tools": [
                "pdf",
                "reasoning",
            ],

            "steps": [

                "Load PDF",

                "Extract Text",

                "Analyze Content",

                "Generate Summary",

            ],

            "complexity": "Medium",

            "estimated_time": "4 sec",

        },

        "research": {

            "task": "Research",

            "agent": "research_agent",

            "tools": [
                "web",
                "reasoning",
            ],

            "steps": [

                "Search Internet",

                "Collect Sources",

                "Analyze Information",

                "Generate Final Report",

            ],

            "complexity": "High",

            "estimated_time": "6 sec",

        },

        "vision": {

            "task": "Image Analysis",

            "agent": "vision_agent",

            "tools": [
                "vision",
            ],

            "steps": [

                "Load Image",

                "Analyze Image",

                "Generate Description",

            ],

            "complexity": "Medium",

            "estimated_time": "3 sec",

        },

        "data_analysis": {

            "task": "Data Analysis",

            "agent": "data_agent",

            "tools": [
                "python",
                "reasoning",
            ],

            "steps": [

                "Load Dataset",

                "Validate Dataset",

                "Clean Data",

                "Analyze Data",

                "Generate Insights",

                "Prepare Final Report",

            ],

            "complexity": "Medium",

            "estimated_time": "5 sec",

        },

        "general": {

            "task": "General Conversation",

            "agent": "general_agent",

            "tools": [
                "memory",
            ],

            "steps": [

                "Understand Request",

                "Generate Response",

            ],

            "complexity": "Low",

            "estimated_time": "2 sec",

        },

    }

    @classmethod
    def create(cls, reasoning):

        intent = reasoning.intent

        config = cls.PLANS.get(
            intent,
            cls.PLANS["general"]
        )

        return ExecutionPlan(

            task=config["task"],

            agent=config["agent"],

            tools=config["tools"],

            steps=config["steps"],

            complexity=config["complexity"],

            estimated_time=config["estimated_time"],

        )