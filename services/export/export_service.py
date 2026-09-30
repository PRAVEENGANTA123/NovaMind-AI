"""
NovaMind AI - Chat & Document Export Service
===========================================
Generates downloadable Markdown and PDF files for chat sessions.
"""

from datetime import datetime
from fpdf import FPDF
import io

class ExportService:

    @staticmethod
    def to_markdown(messages: list) -> str:
        """Converts chat messages into clean Markdown format."""
        md_lines = [
            "# NovaMind AI - Chat Transcript",
            f"*Generated on {datetime.now().strftime('%d %B %Y, %I:%M %p')}*",
            "\n---\n"
        ]
        for msg in messages:
            role = msg.get("role", "User").capitalize()
            content = msg.get("content", "")
            md_lines.append(f"### 👤 {role}" if role.lower() == "user" else f"### 🤖 NovaMind AI")
            md_lines.append(f"{content}\n")
            md_lines.append("---\n")
        return "\n".join(md_lines)

    @staticmethod
    def to_pdf(messages: list) -> bytes:
        """Converts chat transcript into a clean PDF document."""
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "NovaMind AI - Chat Transcript", ln=True, align="C")
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, f"Date: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", ln=True, align="C")
        pdf.ln(5)

        for msg in messages:
            role = "User" if msg.get("role") == "user" else "NovaMind AI"
            raw_content = str(msg.get("content", ""))
            clean_content = raw_content.encode("latin-1", "replace").decode("latin-1")
            
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, f"{role}:", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, clean_content)
            pdf.ln(4)

        return pdf.output(dest="S").encode("latin-1")
