"""
=========================================
NovaMind AI - Gemini Service
=========================================

Handles communication with Google Gemini using the Google GenAI SDK.
Features automatic DNS/socket retry, multi-model fallback, and user preference configuration.
"""

import os
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class GeminiService:
    PRIMARY_MODEL = "gemini-3.6-flash"
    FALLBACK_MODELS = ["gemini-3.5-flash-lite", "gemini-3-flash-preview"]

    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 2048,
    ):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")

        self.client = genai.Client(api_key=api_key)
        self.model = model or self.PRIMARY_MODEL
        self.temperature = float(temperature)
        self.max_output_tokens = int(max_output_tokens)

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate AI response with automatic socket retry and multi-model fallback.
        """
        if not prompt or not prompt.strip():
            return "Please provide a prompt."

        config = types.GenerateContentConfig(
            temperature=kwargs.get("temperature", self.temperature),
            max_output_tokens=kwargs.get("max_output_tokens", self.max_output_tokens),
        )

        models_to_try = [self.model] + [m for m in self.FALLBACK_MODELS if m != self.model]

        last_error = ""

        for current_model in models_to_try:
            # Try up to 3 times per model in case of temporary DNS/socket glitch
            for attempt in range(3):
                try:
                    response = self.client.models.generate_content(
                        model=current_model,
                        contents=prompt,
                        config=config,
                    )

                    if response.text:
                        return response.text

                    return "No response returned from Gemini."

                except Exception as e:
                    error_msg = str(e)
                    last_error = error_msg

                    # If DNS / network socket glitch (11001 getaddrinfo), pause and retry
                    if "11001" in error_msg or "getaddrinfo" in error_msg.lower() or "timeout" in error_msg.lower():
                        time.sleep(1.2)
                        continue

                    # If 503 high demand or 429 rate limit, switch to fallback model
                    if "503" in error_msg or "UNAVAILABLE" in error_msg.upper() or "429" in error_msg:
                        break  # Move to next fallback model in models_to_try
                    else:
                        # Non-retryable error
                        return f"Gemini Error: {error_msg}"

        # If all retries and fallback models failed due to DNS/network
        if "11001" in last_error or "getaddrinfo" in last_error.lower():
            return (
                "⚠️ **Network / DNS Connection Error**\n\n"
                "Unable to connect to Google Gemini servers (`generativelanguage.googleapis.com`).\n\n"
                "**Quick Fixes:**\n"
                "1. Check that your Wi-Fi / Internet connection is active.\n"
                "2. Open Command Prompt as Administrator and run `ipconfig /flushdns`.\n"
                "3. If using a VPN, proxy, or firewall, ensure outgoing HTTPS traffic on port 443 is allowed."
            )

        return f"Gemini is temporarily unavailable: {last_error}"
