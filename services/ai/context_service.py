"""
=========================================
NovaMind AI - Context Service
=========================================

Builds the AI context before sending
a request to Gemini.

Future Sources:
- Memory
- Chat History
- PDFs
- Web Search
- Vector Database
- User Preferences
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime


# ==========================================
# Context Model
# ==========================================

@dataclass
class AIContext:

    prompt: str

    memory: List[str] = field(default_factory=list)

    history: List[str] = field(default_factory=list)

    documents: List[str] = field(default_factory=list)

    search_results: List[str] = field(default_factory=list)

    user_preferences: Dict = field(default_factory=dict)

    metadata: Dict = field(default_factory=dict)


# ==========================================
# Context Service
# ==========================================

class ContextService:

    @staticmethod
    def build(prompt: str) -> AIContext:
        """
        Build AI context.

        Currently returns placeholder data.
        Future versions will integrate with
        Memory, PDF, Search and Vector DB.
        """

        context = AIContext(

            prompt=prompt,

            memory=[],

            history=[],

            documents=[],

            search_results=[],

            user_preferences={

                "theme": "dark",

                "model": "gemini"

            },

            metadata={

                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "source": "NovaMind",

                "version": "2.5"

            }

        )

        return context