"""
=========================================
NovaMind AI - MongoDB Connection
=========================================

Creates a single MongoDB connection
shared across the entire application.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# =====================================
# Load Environment & Streamlit Secrets
# =====================================

load_dotenv()


def get_config_var(key: str, default: str = "") -> str:
    """Retrieve config from st.secrets first, then os.getenv."""
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return os.getenv(key, default).strip()


MONGO_URI = get_config_var("MONGO_URI", "")
DATABASE_NAME = get_config_var("DATABASE_NAME", "NovaMindAI")
GOOGLE_API_KEY = get_config_var("GOOGLE_API_KEY", "")

# =====================================
# Debug (Temporary)
# =====================================

print("=" * 60)
print("MONGO_URI       :", "Found" if MONGO_URI else "Missing")
print("DATABASE_NAME   :", repr(DATABASE_NAME))
print("=" * 60)

# =====================================
# Validate Configuration
# =====================================

if not MONGO_URI:
    raise ValueError(
        "MONGO_URI is missing. Please add it to Streamlit Secrets or .env"
    )

if not DATABASE_NAME:
    raise ValueError(
        "DATABASE_NAME is missing. Please add it to Streamlit Secrets or .env"
    )

# =====================================
# MongoDB Client
# =====================================

try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
        maxPoolSize=50,
        minPoolSize=5,
    )

    client.admin.command("ping")
    db = client[DATABASE_NAME]

    print("=" * 60)
    print("MongoDB Connected Successfully")
    print(f"Database : {DATABASE_NAME}")
    print("=" * 60)

except ServerSelectionTimeoutError as e:
    print("=" * 60)
    print("MongoDB Connection Failed")
    print(e)
    print("=" * 60)
    raise

except Exception as e:
    print("=" * 60)
    print("MongoDB Error")
    print(e)
    print("=" * 60)
    raise

# =====================================
# Collections
# =====================================

users_collection = db["users"]
chats_collection = db["chats"]
history_collection = db["history"]
pdf_collection = db["pdfs"]
pdf_chat_collection = db["pdf_chats"]
settings_collection = db["settings"]
logs_collection = db["logs"]

# =====================================
# Database Indexes
# =====================================

try:
    users_collection.create_index("email", unique=True)
    chats_collection.create_index([("email", 1), ("created_at", -1)])
    chats_collection.create_index([("email", 1), ("bookmarked", 1)])
    pdf_collection.create_index([("email", 1), ("created_at", -1)])
except Exception:
    pass

# =====================================
# Helpers
# =====================================

def get_database():
    """Return MongoDB database instance."""
    return db


def get_collection(name: str):
    """Return any MongoDB collection."""
    return db[name]