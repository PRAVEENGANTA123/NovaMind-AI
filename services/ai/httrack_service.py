"""
NovaMind AI - HTTrack CLI Integration Service
============================================
Executes the HTTrack CLI engine to mirror target websites locally,
cleans the DOM trees, and packages extracted content for AI grounding.
"""

import os
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

# Standard Windows installation paths for WinHTTrack
POSSIBLE_HTTRACK_PATHS = [
    "httrack",
    r"C:\Program Files\WinHTTrack\httrack.exe",
    r"C:\Program Files (x86)\WinHTTrack\httrack.exe",
    r"C:\Program Files\HTTrack\httrack.exe",
    r"C:\Program Files (x86)\HTTrack\httrack.exe",
]


class HTTrackService:
    @staticmethod
    def get_executable() -> Optional[str]:
        """Locate the HTTrack binary executable."""
        for path in POSSIBLE_HTTRACK_PATHS:
            if shutil.which(path) or os.path.isfile(path):
                return path
        return None

    @classmethod
    def is_httrack_available(cls) -> bool:
        """Check if httrack binary is accessible."""
        exe = cls.get_executable()
        if not exe:
            return False
        try:
            res = subprocess.run(
                [exe, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
            )
            return res.returncode == 0
        except Exception:
            return False

    @classmethod
    def mirror_site(
        cls,
        url: str,
        depth: int = 2,
        max_pages: int = 50,
        timeout: int = 60,
    ) -> Dict[str, Any]:
        """Executes the HTTrack CLI to clone a website's HTML tree locally."""
        exe = cls.get_executable()
        if not exe:
            return {
                "success": False,
                "error": "HTTrack executable not found in system or standard Program Files paths.",
            }

        if not url:
            return {"success": False, "error": "No URL provided."}

        parsed = urlparse(url)
        domain = (parsed.hostname or "").lower().removeprefix("www.")
        
        temp_dir = tempfile.mkdtemp(prefix="novamind_httrack_")

        cmd = [
            exe,
            url,
            "-O", temp_dir,
            f"-r{depth}",
            "-%v",
            "+*.html",
            "+*.htm",
            "-*.jpg",
            "-*.jpeg",
            "-*.png",
            "-*.gif",
            "-*.zip",
            "-*.rar",
            "-*.pdf",
            "-*.mp4",
            "-*.mp3",
        ]

        print("=" * 60)
        print(f"🚀 RUNNING HTTRACK CLI ENGINE: {domain}")
        print(f"Executable: {exe}")
        print(f"Target URL: {url}")
        print(f"Recursion Depth: {depth}")
        print("=" * 60)

        try:
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
            )

            extracted_resources: List[Dict[str, Any]] = []
            
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith((".html", ".htm")):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                soup = BeautifulSoup(f.read(), "html.parser")
                                for tag in soup(["script", "style", "noscript", "svg"]):
                                    tag.decompose()
                                
                                title = soup.title.get_text(" ", strip=True) if soup.title else file
                                text = soup.get_text("\n", strip=True)
                                
                                if len(text) > 100:
                                    extracted_resources.append({
                                        "file": file,
                                        "title": title,
                                        "content": text[:15000],
                                        "word_count": len(text.split()),
                                    })
                        except Exception:
                            continue

                    if len(extracted_resources) >= max_pages:
                        break

            shutil.rmtree(temp_dir, ignore_errors=True)

            print(f"✅ HTTrack successfully mirrored and parsed {len(extracted_resources)} pages.")
            
            return {
                "success": bool(extracted_resources),
                "engine": "HTTrack CLI",
                "domain": domain,
                "url": url,
                "mirrored_pages": len(extracted_resources),
                "resources": extracted_resources,
            }

        except subprocess.TimeoutExpired:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return {"success": False, "error": "HTTrack execution timed out."}
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return {"success": False, "error": f"HTTrack execution error: {str(e)}"}
