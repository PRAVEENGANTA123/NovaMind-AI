"""
NovaMind AI - Document & Grounding Exporter Service
==================================================
Generates downloadable Markdown reports and formatted HTML summaries 
of indexed sites, sub-links, and AI chat groundings.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List

class GroundingExportService:

    @staticmethod
    def generate_markdown_report(site_data: Dict[str, Any], chat_history: List[Dict[str, str]] = None) -> str:
        """Generates a complete structured Markdown document from indexed website data."""
        domain = site_data.get("domain", "Unknown Domain")
        root_url = site_data.get("root_url", "")
        resources = site_data.get("resources", []) or site_data.get("website_resources", [])
        crawl_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        lines = [
            f"# NovaMind AI - Grounded Website Intelligence Report",
            f"**Target Domain:** `{domain}`  ",
            f"**Root URL:** {root_url}  ",
            f"**Indexed Timestamp:** {crawl_time}  ",
            f"**Total Indexed Sub-Links:** {len(resources)}  ",
            "\n---\n",
            "## 1. Executive Summary & Site Structure\n",
        ]

        if resources:
            root_item = resources[0]
            lines.append(f"### {root_item.get('title', 'Root Portal')}")
            lines.append(f"> {root_item.get('description', 'No meta description provided.')}\n")

        lines.append("## 2. Indexed Sub-Link Directory\n")
        lines.append("| Category | Page Title | URL |")
        lines.append("| :--- | :--- | :--- |")

        for r in resources[:40]:  # Cap table to top 40 for clean document formatting
            cat = r.get("category", "🌐 General")
            title = r.get("title", "Resource Link").replace("|", "-")
            url = r.get("url", "")
            lines.append(f"| {cat} | {title} | [{url}]({url}) |")

        if len(resources) > 40:
            lines.append(f"\n*...and {len(resources) - 40} additional sub-links cataloged.*")

        if chat_history:
            lines.append("\n---\n")
            lines.append("## 3. Grounded Q&A Insights\n")
            for msg in chat_history:
                role = "User" if msg.get("role") == "user" else "NovaMind AI"
                content = msg.get("content", "").strip()
                lines.append(f"**{role}:**\n{content}\n")

        return "\n".join(lines)
