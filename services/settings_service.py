"""
=========================================
NovaMind AI - Settings Service
=========================================
Handles reading, merging, and persisting user preferences
via SettingsRepository in MongoDB.
"""

from typing import Any, Dict, Optional, Tuple, Union

try:
    from database.settings_repository import SettingsRepository
except ImportError:
    SettingsRepository = None

try:
    from database.users import get_user_settings, update_user_settings
except ImportError:
    get_user_settings = None
    update_user_settings = None


# ==========================================
# Default Settings
# ==========================================

DEFAULT_SETTINGS = {
    # Appearance
    "theme": "auto",
    "accent": "Blue",
    "font_size": "Medium",
    "compact_mode": False,

    # General & Voice
    "language": "English",
    "tts_voice_language": "en",
    "enable_voice_input": True,

    # AI Model & Discovery
    "default_model": "gemini-1.5-pro",
    "model_name": "gemini-1.5-pro",
    "temperature": 0.7,
    "conversation_memory": True,
    "max_tokens": 2048,
    "max_workers": 25,
    "default_web_search": False,
    "default_auto_reasoning": True,

    # General Options
    "auto_save": True,
    "notifications": True,

    # Notifications
    "email_notifications": True,
    "desktop_notifications": True,
    "chat_notifications": True,
    "weekly_report": False,
    "sound_alerts": True,
    "marketing_email": False,

    # Privacy & Session
    "two_factor": False,
    "login_alerts": True,
    "session_timeout": 30,
}


# ==========================================
# Load Settings
# ==========================================

def load_settings(email: str) -> Dict[str, Any]:
    """
    Load settings from MongoDB.
    Falls back gracefully to DEFAULT_SETTINGS.
    """
    if not email:
        return DEFAULT_SETTINGS.copy()

    stored_settings = None

    if SettingsRepository:
        stored_settings = SettingsRepository.get_settings(email)

    if not stored_settings and get_user_settings:
        stored_settings = get_user_settings(email)

    if not stored_settings:
        return DEFAULT_SETTINGS.copy()

    merged = DEFAULT_SETTINGS.copy()
    merged.update(stored_settings)
    return merged


# ==========================================
# Save Settings
# ==========================================

def save_settings(
    email: str,
    theme: Optional[str] = "auto",
    accent: Optional[str] = "Blue",
    font_size: Optional[str] = "Medium",
    compact_mode: Optional[bool] = False,
    language: Optional[str] = "English",
    default_model: Optional[str] = "gemini-1.5-pro",
    temperature: Optional[float] = 0.7,
    auto_save: Optional[bool] = True,
    notifications: Optional[bool] = True,
    conversation_memory: Optional[bool] = True,
    max_tokens: Optional[int] = 2048,
    email_notifications: Optional[bool] = True,
    desktop_notifications: Optional[bool] = True,
    chat_notifications: Optional[bool] = True,
    weekly_report: Optional[bool] = False,
    sound_alerts: Optional[bool] = True,
    marketing_email: Optional[bool] = False,
    two_factor: Optional[bool] = False,
    login_alerts: Optional[bool] = True,
    session_timeout: Optional[int] = 30,
    **kwargs: Any,
) -> Tuple[bool, str]:
    """
    Save all settings to MongoDB.
    Supports individual parameter calls from settings page forms as well
    as arbitrary dictionary kwargs.
    """
    if not email:
        return False, "❌ Invalid user email."

    # If the first argument after email was passed as a full settings dictionary
    if isinstance(theme, dict):
        settings_dict = theme
    else:
        settings_dict = {
            "theme": str(theme).lower(),
            "accent": accent,
            "font_size": font_size,
            "compact_mode": compact_mode,
            "language": language,
            "default_model": default_model,
            "model_name": default_model,
            "temperature": temperature,
            "conversation_memory": conversation_memory,
            "max_tokens": max_tokens,
            "auto_save": auto_save,
            "notifications": notifications,
            "email_notifications": email_notifications,
            "desktop_notifications": desktop_notifications,
            "chat_notifications": chat_notifications,
            "weekly_report": weekly_report,
            "sound_alerts": sound_alerts,
            "marketing_email": marketing_email,
            "two_factor": two_factor,
            "login_alerts": login_alerts,
            "session_timeout": session_timeout,
        }
        settings_dict.update(kwargs)

    # Persist in MongoDB
    saved = False
    if SettingsRepository:
        saved = SettingsRepository.update_settings(email, settings_dict)

    if not saved and update_user_settings:
        try:
            update_user_settings(email, settings_dict)
            saved = True
        except Exception:
            saved = False

    if saved:
        return True, "✅ Settings saved successfully."
    return False, "❌ Failed to persist settings to database."