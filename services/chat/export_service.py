"""
=========================================
NovaMind AI - Chat Export Service
=========================================

Export AI conversations to:

• PDF
• Markdown
• Text
• JSON
"""

import json
from pathlib import Path
from datetime import datetime

# ==========================================
# Resilient PDF Engine Import
# ==========================================
try:
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import (
        Paragraph,
        SimpleDocTemplate,
        Spacer,
    )
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class ChatExportService:

    EXPORT_FOLDER = Path("exports")

    # =====================================
    # Create Export Folder
    # =====================================

    @classmethod
    def _prepare(cls):

        cls.EXPORT_FOLDER.mkdir(
            exist_ok=True,
            parents=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        return timestamp

    # =====================================
    # TXT
    # =====================================

    @classmethod
    def export_txt(cls, messages):

        timestamp = cls._prepare()

        file = cls.EXPORT_FOLDER / f"chat_{timestamp}.txt"

        with open(
            file,
            "w",
            encoding="utf-8",
        ) as f:

            f.write("NovaMind AI Conversation\n")
            f.write("=" * 60)
            f.write("\n\n")

            for message in messages:

                role = message.get(
                    "role",
                    "assistant",
                ).upper()

                content = message.get(
                    "content",
                    "",
                )

                f.write(f"{role}\n")
                f.write("-" * 40)
                f.write("\n")
                f.write(content)
                f.write("\n\n")

        return str(file)

    # =====================================
    # Markdown
    # =====================================

    @classmethod
    def export_markdown(cls, messages):

        timestamp = cls._prepare()

        file = cls.EXPORT_FOLDER / f"chat_{timestamp}.md"

        with open(
            file,
            "w",
            encoding="utf-8",
        ) as f:

            f.write("# NovaMind AI Conversation\n\n")

            f.write(
                f"Generated: {datetime.now()}\n\n"
            )

            for message in messages:

                role = message.get(
                    "role",
                    "assistant",
                )

                content = message.get(
                    "content",
                    "",
                )

                f.write(
                    f"## {role.title()}\n\n"
                )

                f.write(content)

                f.write("\n\n")

        return str(file)

    # =====================================
    # JSON
    # =====================================

    @classmethod
    def export_json(cls, messages):

        timestamp = cls._prepare()

        file = cls.EXPORT_FOLDER / f"chat_{timestamp}.json"

        data = {

            "created_at": str(datetime.now()),

            "messages": messages,

            "total_messages": len(messages),

        }

        with open(
            file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                default=str,
                ensure_ascii=False,
            )

        return str(file)

    # =====================================
    # PDF
    # =====================================

    @classmethod
    def export_pdf(cls, messages):

        if not HAS_REPORTLAB:
            print("WARNING: reportlab is not installed. Falling back to plain text export.")
            return cls.export_txt(messages)

        timestamp = cls._prepare()

        file = cls.EXPORT_FOLDER / f"chat_{timestamp}.pdf"

        styles = getSampleStyleSheet()

        doc = SimpleDocTemplate(str(file))

        story = []

        story.append(

            Paragraph(
                "NovaMind AI Conversation",
                styles["Heading1"],
            )

        )

        story.append(

            Paragraph(
                datetime.now().strftime(
                    "%d %B %Y %I:%M %p"
                ),
                styles["Normal"],
            )

        )

        story.append(
            Spacer(1, 20)
        )

        for message in messages:

            role = message.get(
                "role",
                "assistant",
            ).title()

            content = message.get(
                "content",
                "",
            )

            story.append(

                Paragraph(
                    f"**{role}**",
                    styles["Heading2"],
                )

            )

            story.append(

                Paragraph(
                    content.replace(
                        "\n",
                        "<br/>",
                    ),
                    styles["BodyText"], 
                )

            )

            story.append(
                Spacer(1, 12)
            )

        doc.build(story)

        return str(file)