"""
NovaMind AI - Offline Site Archiver (HTTrack-Style)
==================================================
Saves structured crawls and mirrored subpages to offline storage.
"""

import json
import os
import re
from typing import Dict, Any


class SiteArchiver:

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        return re.sub(r'[\\/*?:"<>| ]', "_", name)[:80]

    @classmethod
    def export_offline_mirror(cls, discovery_data: Dict[str, Any], base_dir: str = "downloads/mirrors") -> str:
        """Exports crawled site metadata and pages to local structured markdown files."""
        domain = discovery_data.get("domain", "website")
        target_dir = os.path.join(base_dir, cls._sanitize_filename(domain))
        os.makedirs(target_dir, exist_ok=True)

        # 1. Save Full Discovery Manifest
        manifest_path = os.path.join(target_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(discovery_data, f, indent=2, ensure_ascii=False)

        # 2. Save Individual Pages
        pages_dir = os.path.join(target_dir, "pages")
        os.makedirs(pages_dir, exist_ok=True)

        resources = discovery_data.get("resources", [])
        for idx, res in enumerate(resources):
            title = res.get("title") or f"page_{idx}"
            file_name = f"{idx:03d}_{cls._sanitize_filename(title)}.md"
            file_path = os.path.join(pages_dir, file_name)

            content = (
                f"# {res.get('title', '')}\n"
                f"**URL:** {res.get('url', '')}\n"
                f"**Category:** {res.get('category', 'General')}\n\n"
                f"---\n\n"
                f"{res.get('content', '')}\n"
            )
            with open(file_path, "w", encoding="utf-8") as pf:
                pf.write(content)

        return target_dir