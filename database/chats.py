"""
=========================================
NovaMind AI - Chat Database
=========================================
Handles all MongoDB chat operations.
"""

from datetime import datetime

from database.mongodb import db

# MongoDB Collection
chats_collection = db["chats"]


def save_chat(user_email, question, answer):
    """
    Save a chat conversation.
    """

    chat = {
        "user_email": user_email,
        "question": question,
        "answer": answer,
        "created_at": datetime.utcnow()
    }

    chats_collection.insert_one(chat)


def get_chat_history(user_email):
    """
    Get all chats for a user.
    """

    return list(
        chats_collection.find(
            {"user_email": user_email}
        ).sort("created_at", -1)
    )


def delete_chat(chat_id):
    """
    Delete a chat.
    """

    from bson import ObjectId

    chats_collection.delete_one(
        {"_id": ObjectId(chat_id)}
    )


def total_chats():
    """
    Total number of chats.
    """

    return chats_collection.count_documents({})