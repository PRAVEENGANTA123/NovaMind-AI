"""
NovaMind AI - Document Export & Print Service
============================================
Generates structured Markdown and HTML documents from analyzed websites
and chat interactions for printing or offline saving.
"""

from datetime import datetime
import html
import os
from typing import Any, Dict, List, Optional


class DocumentExportService:
    @staticmethod
    def generate_website_summary_document(
        url: str,
        title: str,
        domain: str,
        query: str,
        ai_answer: str,
        resources: List[Dict[str, Any]],
    ) -> str:
        """
        Creates a clean, printable HTML document containing the synthesized answer,
        active source links, and crawled sub-page directory tree.
        """
        now_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
        
        resource_rows = ""
        for idx, r in enumerate(resources[:30], start=1):
            r_title = html.escape(str(r.get("title") or "Page"))
            r_url = html.escape(str(r.get("url") or "#"))
            r_cat = html.escape(str(r.get("category") or "General"))
            resource_rows += f"""
            <tr>
                <td>{idx}</td>
                <td><strong>{r_title}</strong></td>
                <td><a href="{r_url}" target="_blank">{r_url}</a></td>
                <td>{r_cat}</td>
            </tr>
            """

        formatted_answer = ai_answer.replace("\n", "<br/>")

        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NovaMind AI - Website Summary Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #222;
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        .header {{
            border-bottom: 2px solid #0066cc;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}
        .meta-box {{
            background: #f4f7f9;
            border-left: 4px solid #0066cc;
            padding: 12px 18px;
            margin-bottom: 25px;
            border-radius: 4px;
        }}
        .answer-box {{
            background: #ffffff;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 14px;
        }}
        th, td {{
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
        }}
        @media print {{
            body {{ margin: 10mm; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>NovaMind AI — Website Discovery & Intelligence Report</h1>
        <p>Generated on: {now_str}</p>
    </div>

    <div class="meta-box">
        <strong>Domain:</strong> {domain}<br/>
        <strong>Source URL:</strong> <a href="{url}">{url}</a><br/>
        <strong>Topic / User Query:</strong> {html.escape(query)}<br/>
        <strong>Total Indexed Pages:</strong> {len(resources)}
    </div>

    <h2>Synthesized Insights</h2>
    <div class="answer-box">
        {formatted_answer}
    </div>

    <h2>Discovered Internal Sub-Pages (Directory Map)</h2>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Page Title</th>
                <th>URL</th>
                <th>Category</th>
            </tr>
        </thead>
        <tbody>
            {resource_rows}
        </tbody>
    </table>
</body>
</html>
"""
        return html_doc
