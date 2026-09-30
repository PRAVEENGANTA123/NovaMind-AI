from dotenv import load_dotenv
import os
from database.db import db

load_dotenv()

print("MONGO_URI:", os.getenv("MONGO_URI"))
print("DATABASE_NAME:", os.getenv("DATABASE_NAME"))

print("Database Connected:", db.name)
print("Collections:", db.list_collection_names())