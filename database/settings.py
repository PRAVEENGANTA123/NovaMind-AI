"""
=========================================
NovaMind AI - Settings Database
=========================================
"""

from database.mongodb import settings_collection


def get_settings(email):

    settings = settings_collection.find_one(
        {"email": email}
    )

    if settings:

        return settings

    default = {

        "email": email,

        "theme": "System",

        "accent": "Blue",

        "font_size": "Medium",

        "ai_model": "Gemini 2.5 Flash",

        "temperature": 0.7,

        "max_tokens": 2048,

        "conversation_memory": True,

        "auto_save": True,

        "email_notifications": True,

        "desktop_notifications": True,

        "chat_notifications": True,

        "weekly_report": False,

        "two_factor": False,

    }

    settings_collection.insert_one(default)

    return default


def update_settings(email, data):

    settings_collection.update_one(

        {"email": email},

        {

            "$set": data

        }

    )