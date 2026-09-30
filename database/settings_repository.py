"""
NovaMind AI - Settings Repository
=================================
Manages persistent user configuration and system preferences in MongoDB.
"""

from datetime import datetime
from typing import Any, Dict
from database.db import db


class SettingsRepository:
    COLLECTION_NAME = "user_settings"

    @classmethod
    def get_collection(cls):
        return db[cls.COLLECTION_NAME]

    @classmethod
    def get_settings(cls, email: str) -> Dict[str, Any]:
        """
        Retrieves user settings by email from MongoDB.
        """
        if not email or not isinstance(email, str):
            return {}

        clean_email = email.strip().lower()
        try:
            coll = cls.get_collection()
            record = coll.find_one({"email": clean_email})
            if record and "settings" in record:
                return record["settings"]
        except Exception as e:
            print(f"⚠️ Error fetching user settings: {e}")

        return {}

    @classmethod
    def update_settings(cls, email: str, new_settings: Dict[str, Any]) -> bool:
        """
        Saves or merges updated settings to MongoDB for the given user.
        """
        if not email or not isinstance(email, str):
            return False

        clean_email = email.strip().lower()
        try:
            coll = cls.get_collection()
            # Fetch existing to avoid clobbering other existing preferences
            existing = cls.get_settings(clean_email)
            existing.update(new_settings)

            coll.update_one(
                {"email": clean_email},
                {
                    "$set": {
                        "settings": existing,
                        "updated_at": datetime.now(),
                    },
                    "$setOnInsert": {
                        "email": clean_email,
                        "created_at": datetime.now(),
                    },
                },
                upsert=True,
            )
            return True
        except Exception as e:
            print(f"⚠️ Error updating user settings: {e}")
            return False
