"""
NovaMind AI - Persistent URL Ingestion Repository
================================================
Saves and retrieves crawled website structures to/from MongoDB.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from database.mongodb import get_database


class URLRepository:
    _collection_name = "cached_websites"

    @classmethod
    def get_collection(cls):
        """Retrieve the MongoDB collection for cached websites."""
        try:
            db = get_database()
            if db is not None:
                return db[cls._collection_name]
        except Exception as e:
            print("MongoDB collection access warning in URLRepository:", e)
        return None

    @classmethod
    def get_cached_site(cls, domain: str) -> Optional[Dict[str, Any]]:
        """Retrieve a cached crawl record from MongoDB if it exists."""
        try:
            col = cls.get_collection()
            if col is None:
                return None
            record = col.find_one({"domain": domain.lower()})
            return record
        except Exception as e:
            print("Error reading cached site from MongoDB:", e)
            return None

    @classmethod
    def save_crawled_site(cls, domain: str, root_url: str, result_data: dict) -> bool:
        """Upsert parsed site data into the MongoDB collection."""
        try:
            col = cls.get_collection()
            if col is None:
                return False
            col.update_one(
                {"domain": domain.lower()},
                {
                    "$set": {
                        "domain": domain.lower(),
                        "root_url": root_url,
                        "data": result_data,
                        "updated_at": datetime.now(timezone.utc),
                    }
                },
                upsert=True,
            )
            return True
        except Exception as e:
            print("Error saving crawled site to MongoDB:", e)
            return False