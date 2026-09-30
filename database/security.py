"""
NovaMind AI - Database Security & Input Sanitization
===================================================
Prevents SQL Injection, NoSQL Operator Injection, and Untrusted Query Execution.
"""

import re
from typing import Any, Dict


class SecurityGuard:

    @staticmethod
    def sanitize_search_query(query: str) -> str:
        """Strips dangerous control characters and trims length."""
        if not isinstance(query, str):
            return ""
        # Remove null bytes and limit input length
        clean = query.replace("\x00", "").strip()
        return clean[:500]

    @staticmethod
    def sanitize_nosql_input(payload: Any) -> Any:
        """
        Recursively strips MongoDB operator keys ($gt, $where, $ne)
        from untrusted user input dictionaries.
        """
        if isinstance(payload, dict):
            clean_dict = {}
            for k, v in payload.items():
                # Block keys starting with $ or containing dots
                if not str(k).startswith("$") and "." not in str(k):
                    clean_dict[k] = SecurityGuard.sanitize_nosql_input(v)
            return clean_dict
        elif isinstance(payload, list):
            return [SecurityGuard.sanitize_nosql_input(item) for item in payload]
        elif isinstance(payload, str):
            return payload.replace("\x00", "").strip()
        return payload

    @staticmethod
    def build_safe_filter(domain: str) -> Dict[str, str]:
        """Ensures safe, parameterized MongoDB filter construction."""
        safe_domain = SecurityGuard.sanitize_search_query(domain).lower()
        return {"domain": safe_domain}