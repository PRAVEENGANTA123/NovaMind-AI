"""
=========================================
NovaMind AI - MongoDB Connection
=========================================

Creates a singleton MongoDB connection shared across the entire application,
with cross-environment support for local dev (.env) and Streamlit Cloud (st.secrets),
CA certificate validation via certifi, and automatic retry handling.
"""

import os
import certifi
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
    val = os.getenv(key)
    return str(val).strip() if val is not None else default


MONGO_URI = get_config_var("MONGO_URI", "")
DATABASE_NAME = get_config_var("DATABASE_NAME", "NovaMindAI")
GOOGLE_API_KEY = get_config_var("GOOGLE_API_KEY", "")

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
# MongoDB Client Initialization
# =====================================

def init_mongo_client(uri: str) -> MongoClient:
    """
    Connect to MongoDB with TLS support for Atlas and fallback for local instances.
    """
    is_atlas = "mongodb.net" in uri or "ssl=true" in uri.lower() or "tls=true" in uri.lower()

    client_kwargs = {
        "serverSelectionTimeoutMS": 15000,  # 15s window for cloud replica set negotiation
        "connectTimeoutMS": 10000,
        "socketTimeoutMS": 45000,
        "maxPoolSize": 50,
        "minPoolSize": 1,
        "retryWrites": True,
        "retryReads": True,
    }

    if is_atlas:
        client_kwargs["tls"] = True
        client_kwargs["tlsCAFile"] = certifi.where()

    return MongoClient(uri, **client_kwargs)


try:
    client = init_mongo_client(MONGO_URI)
    # Ping database to verify active connection
    client.admin.command("ping")
    db = client[DATABASE_NAME]

    print("=" * 60)
    print("✅ MongoDB Connected Successfully")
    print(f"Database : {DATABASE_NAME}")
    print("=" * 60)

except ServerSelectionTimeoutError as e:
    print("=" * 60)
    print("❌ MongoDB ServerSelectionTimeoutError: Failed to reach cluster")
    print(f"Details  : {e}")
    print("=" * 60)
    raise

except Exception as e:
    print("=" * 60)
    print(f"❌ MongoDB Connection Error: {e}")
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