"""
NovaMind AI - Concurrent Chunked File Downloader (IDM-Style)
===========================================================
Downloads large resources using HTTP Range headers and multi-threading.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import requests
from typing import Optional


class ChunkDownloader:

    @staticmethod
    def _download_byte_range(url: str, start_byte: int, end_byte: int, part_path: str, headers: dict) -> bool:
        """Fetch a specific byte segment and save to temporary part file."""
        req_headers = headers.copy()
        req_headers["Range"] = f"bytes={start_byte}-{end_byte}"
        try:
            resp = requests.get(url, headers=req_headers, stream=True, timeout=15)
            if resp.status_code in (200, 206):
                with open(part_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=65536):
                        if chunk:
                            f.write(chunk)
                return True
        except Exception as e:
            print(f"Error downloading chunk {start_byte}-{end_byte}: {e}")
        return False

    @classmethod
    def download(cls, url: str, output_path: str, num_threads: int = 4) -> bool:
        """Download file concurrently using segmented ranges."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # 1. Inspect headers to check Range support and Content-Length
        try:
            head_resp = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
            total_size = int(head_resp.headers.get("content-length", 0))
            accept_ranges = head_resp.headers.get("accept-ranges", "").lower() == "bytes"
        except Exception:
            total_size = 0
            accept_ranges = False

        # Fallback to single-stream download if ranges not supported or size unknown
        if not accept_ranges or total_size < 1024 * 1024:
            resp = requests.get(url, headers=headers, stream=True, timeout=20)
            if resp.status_code == 200:
                os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
                with open(output_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=65536):
                        f.write(chunk)
                return True
            return False

        # 2. Partition byte segments
        chunk_size = total_size // num_threads
        tasks = []
        part_files = []

        for i in range(num_threads):
            start = i * chunk_size
            end = total_size - 1 if i == num_threads - 1 else (start + chunk_size - 1)
            part_path = f"{output_path}.part{i}"
            part_files.append(part_path)
            tasks.append((start, end, part_path))

        # 3. Download chunks concurrently
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(cls._download_byte_range, url, start, end, part, headers)
                for start, end, part in tasks
            ]
            results = [f.result() for f in as_completed(futures)]

        if not all(results):
            # Clean up partials on failure
            for p in part_files:
                if os.path.exists(p):
                    os.remove(p)
            return False

        # 4. Merge byte segments in sequence
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as outfile:
            for part in part_files:
                with open(part, "rb") as infile:
                    outfile.write(infile.read())
                os.remove(part)

        return True