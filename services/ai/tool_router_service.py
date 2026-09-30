"""
=========================================
NovaMind AI - Tool Router Service
=========================================
"""

from dataclasses import dataclass

from services.ai.tool_detection_service import ToolDetectionService


@dataclass
class ToolRoute:

    use_url: bool

    use_web: bool

    use_pdf: bool

    use_chat: bool


class ToolRouterService:

    @staticmethod
    def detect(prompt: str) -> ToolRoute:

        use_url = ToolDetectionService.has_url(prompt)

        use_web = ToolDetectionService.needs_web_search(prompt)

        use_pdf = ToolDetectionService.has_pdf(prompt)

        use_chat = not (
            use_url
            or use_web
            or use_pdf
        )

        return ToolRoute(

            use_url=use_url,

            use_web=use_web,

            use_pdf=use_pdf,

            use_chat=use_chat,

        )