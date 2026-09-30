"""
=========================================
NovaMind AI - Chat Repository
=========================================

MongoDB repository for AI chat conversations.
"""

from datetime import datetime, timezone
from bson import ObjectId
from database.mongodb import chats_collection


class ChatRepository:
    """
    Repository layer for AI chat operations.
    """

    @staticmethod
    def save_chat(
        email: str,
        prompt: str,
        response: str,
        intent: str,
        confidence: float,
        agent: str,
    ) -> str:
        document = {
            "email": email,
            "prompt": prompt,
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "agent": agent,
            "liked": None,
            "bookmarked": False,
            "created_at": datetime.now(timezone.utc),
        }
        result = chats_collection.insert_one(document)
        return str(result.inserted_id)

    @staticmethod
    def get_user_chats(email: str):
        return list(
            chats_collection.find({"email": email}).sort("created_at", -1)
        )

    @staticmethod
    def get_chat(chat_id: str, email: str = None):
        try:
            query = {"_id": ObjectId(chat_id)}
            if email:
                query["email"] = email
            return chats_collection.find_one(query)
        except Exception:
            return None

    @staticmethod
    def like_chat(chat_id: str, email: str = None):
        try:
            query = {"_id": ObjectId(chat_id)}
            if email:
                query["email"] = email
            return chats_collection.update_one(query, {"$set": {"liked": True}})
        except Exception:
            return None

    @staticmethod
    def dislike_chat(chat_id: str, email: str = None):
        try:
            query = {"_id": ObjectId(chat_id)}
            if email:
                query["email"] = email
            return chats_collection.update_one(query, {"$set": {"liked": False}})
        except Exception:
            return None

    @staticmethod
    def bookmark_chat(chat_id: str, email: str = None):
        try:
            query = {"_id": ObjectId(chat_id)}
            if email:
                query["email"] = email
            return chats_collection.update_one(query, {"$set": {"bookmarked": True}})
        except Exception:
            return None

    @staticmethod
    def remove_bookmark(chat_id: str, email: str = None):
        try:
            query = {"_id": ObjectId(chat_id)}
            if email:
                query["email"] = email
            return chats_collection.update_one(query, {"$set": {"bookmarked": False}})
        except Exception:
            return None

    @staticmethod
    def get_bookmarked_chats(email: str):
        return list(
            chats_collection.find({"email": email, "bookmarked": True}).sort("created_at", -1)
        )

    @staticmethod
    def delete_chat(chat_id: str, email: str = None):
        try:
            query = {"_id": ObjectId(chat_id)}
            if email:
                query["email"] = email
            result = chats_collection.delete_one(query)
            return result.deleted_count > 0
        except Exception:
            return False

    @staticmethod
    def delete_user_chats(email: str):
        result = chats_collection.delete_many({"email": email})
        return result.deleted_count

    @staticmethod
    def total_chats(email: str):
        return chats_collection.count_documents({"email": email})

    @staticmethod
    def total_bookmarks(email: str):
        return chats_collection.count_documents({"email": email, "bookmarked": True})
