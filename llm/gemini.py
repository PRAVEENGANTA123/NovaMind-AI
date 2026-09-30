"""
=========================================
NovaMind AI - Gemini LLM
=========================================
"""

import os

import google.generativeai as genai

from dotenv import load_dotenv

# Load .env
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini AI
    """

    try:

        response = model.generate_content(prompt)

        if response.text:
            return response.text

        return "No response generated."

    except Exception as e:
        return f"❌ Gemini Error:\n\n{str(e)}"