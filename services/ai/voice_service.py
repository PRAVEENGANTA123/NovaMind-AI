"""
NovaMind AI - Voice Assistant Service
====================================
Handles Speech-to-Text (STT) transcription and
Text-to-Speech (TTS) audio synthesis for user interactions.
"""

from io import BytesIO
import re
from typing import Any, Dict, Optional
from gtts import gTTS
import speech_recognition as sr


class VoiceService:
    @staticmethod
    def clean_text_for_speech(text: str) -> str:
        """
        Removes Markdown symbols, URLs, and code snippets
        so the spoken output sounds natural.
        """
        if not text:
            return ""

        # Remove URLs
        text = re.sub(r"https?://\S+", "", text)
        # Remove markdown headers and formatting (*, #, _, `, >)
        text = re.sub(r"[*#_`>~]", "", text)
        # Remove code blocks
        text = re.sub(r"```[\s\S]*?```", "", text)
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Limit spoken text length for responsiveness
        return text[:1000]

    @classmethod
    def text_to_speech(cls, text: str, lang: str = "en") -> Optional[bytes]:
        """
        Converts text into MP3 audio bytes in-memory using gTTS.
        """
        clean_text = cls.clean_text_for_speech(text)
        if not clean_text:
            return None

        try:
            tts = gTTS(text=clean_text, lang=lang, slow=False)
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except Exception as e:
            print(f"⚠️ TTS Synthesis Error: {e}")
            return None

    @staticmethod
    def speech_to_text(audio_bytes: bytes) -> Dict[str, Any]:
        """
        Transcribes audio bytes (WAV/Audio recording) into plain text.
        """
        if not audio_bytes:
            return {"success": False, "text": "", "error": "No audio received."}

        recognizer = sr.Recognizer()
        try:
            audio_file = BytesIO(audio_bytes)
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
                transcribed = recognizer.recognize_google(audio_data)

                return {
                    "success": True,
                    "text": transcribed,
                    "error": None,
                }
        except sr.UnknownValueError:
            return {
                "success": False,
                "text": "",
                "error": "Speech was unclear. Please try speaking again.",
            }
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "error": f"Audio transcription failed: {str(e)}",
            }
