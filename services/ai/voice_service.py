"""
NovaMind AI - Voice Assistant Service
====================================
Handles Speech-to-Text (STT) transcription and
Text-to-Speech (TTS) audio synthesis for user interactions.
Features automated browser audio decoding and defensive lazy imports
for resilient cloud execution.
"""

from io import BytesIO
import logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger("NovaMind.VoiceService")

# ==========================================
# Resilient Fallback Imports
# ==========================================
try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    gTTS = None
    HAS_GTTS = False
    logger.warning("gTTS not installed. Text-to-speech functionality disabled.")

try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    sr = None
    HAS_SR = False
    logger.warning("SpeechRecognition not installed. Audio transcription disabled.")

try:
    from pydub import AudioSegment
    HAS_PYDUB = True
except ImportError:
    AudioSegment = None
    HAS_PYDUB = False
    logger.warning("pydub not installed. Browser audio format conversion disabled.")


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
        # Remove code blocks and inline code
        text = re.sub(r"```[\s\S]*?```", "", text)
        text = re.sub(r"`[^`]*`", "", text)
        # Remove markdown symbols (*, #, _, >, ~, etc.)
        text = re.sub(r"[*#_>~]", "", text)
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Limit spoken text length for responsiveness
        return text[:1000]

    @classmethod
    def text_to_speech(cls, text: str, lang: str = "en") -> Optional[bytes]:
        """
        Converts text into MP3 audio bytes in-memory using gTTS.
        Returns None gracefully if gTTS is unavailable or fails.
        """
        if not HAS_GTTS or gTTS is None:
            logger.info("Text-to-speech skipped: gTTS package is unavailable.")
            return None

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
            logger.error(f"TTS Synthesis Error: {e}")
            return None

    @classmethod
    def _convert_to_wav(cls, audio_bytes: bytes) -> Optional[BytesIO]:
        """
        Decodes incoming browser audio (WebM, OGG, MP4, WAV) into standard PCM WAV buffer.
        """
        if not audio_bytes:
            return None

        input_buffer = BytesIO(audio_bytes)

        if HAS_PYDUB and AudioSegment is not None:
            try:
                segment = AudioSegment.from_file(input_buffer)
                wav_buffer = BytesIO()
                segment.export(wav_buffer, format="wav")
                wav_buffer.seek(0)
                return wav_buffer
            except Exception as e:
                logger.warning(f"Audio conversion with pydub failed, falling back to raw buffer: {e}")
                input_buffer.seek(0)
                return input_buffer

        input_buffer.seek(0)
        return input_buffer

    @classmethod
    def speech_to_text(cls, audio_bytes: bytes, language: str = "en-US") -> Dict[str, Any]:
        """
        Transcribes audio bytes into plain text using SpeechRecognition.
        Automatically converts browser audio formats to PCM WAV.
        """
        if not HAS_SR or sr is None:
            return {
                "success": False,
                "text": "",
                "error": "Speech recognition library is not available in this environment.",
            }

        if not audio_bytes:
            return {"success": False, "text": "", "error": "No audio received."}

        try:
            wav_stream = cls._convert_to_wav(audio_bytes)
            if wav_stream is None:
                return {"success": False, "text": "", "error": "Could not parse audio input."}

            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_stream) as source:
                # Calibrate for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio_data = recognizer.record(source)
                transcribed = recognizer.recognize_google(audio_data, language=language)

                return {
                    "success": True,
                    "text": transcribed,
                    "error": None,
                }
        except sr.UnknownValueError:
            return {
                "success": False,
                "text": "",
                "error": "Speech was unclear. Please speak clearly and try again.",
            }
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return {
                "success": False,
                "text": "",
                "error": "Transcription service temporarily unreachable. Check internet connection.",
            }
        except Exception as e:
            logger.error(f"Audio transcription failed: {e}")
            return {
                "success": False,
                "text": "",
                "error": f"Audio transcription failed: {str(e)}",
            }