import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

print("=" * 70)
print("Available Gemini Models")
print("=" * 70)

for model in client.models.list():
    print(model.name)