"""
=========================================
NovaMind AI - Settings
=========================================
"""

import streamlit as st  

from utils.styles import load_css

from components.sidebar import show_sidebar
from components.navbar import show_navbar

from components.settings_header import show_settings_header
from components.appearance_settings import show_appearance_settings
from utils.responsive import apply_responsive_layout
from services.settings_service import (
    load_settings,
    save_settings,
)

# ==========================================
# ==========================================

# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()

st.set_page_config(
    page_title="NovaMind AI | Settings",
    page_icon="⚙️",
    layout="wide",
)
st.session_state["current_page"] = "Settings"

 
# ==========================================
# Authentication
# ==========================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()

# ==========================================
# Load CSS
# ==========================================

load_css("settings.css")

# ==========================================
# Sidebar & Navbar
# ==========================================

st.session_state["current_page"] = "Settings"
show_sidebar()
show_navbar(is_chat=False)

# ==========================================
# Current User
# ==========================================

email = st.session_state["email"]

settings = load_settings(email)

# ==========================================
# Header
# ==========================================

show_settings_header()

# ==========================================
# Appearance
# ==========================================

with st.container(border=True):

    appearance = show_appearance_settings(settings)

# ==========================================
# AI Preferences
# ==========================================
from components.ai_settings import (
    show_ai_settings
)
with st.container(border=True):

    ai = show_ai_settings(settings)
# ==========================================
# Notifications
# ==========================================

from components.notification_settings import (
    show_notification_settings
)
with st.container(border=True):

    notification = show_notification_settings(
        settings
    )
# ==========================================
# Privacy
# ==========================================
from components.privacy_settings import (
    show_privacy_settings
)
with st.container(border=True):

    privacy = show_privacy_settings(
        settings
    )
# ==========================================
# General
# ==========================================

with st.container(border=True):

    st.subheader("ðŸŒ General")

    languages = [
        "English",
        "Hindi",
        "Telugu",
        "Tamil",
    ]

    current_language = settings.get(
        "language",
        "English"
    )

    if current_language not in languages:
        current_language = "English"

    language = st.selectbox(
        "Language",
        languages,
        index=languages.index(current_language),
    )

    auto_save = st.toggle(
        "Auto Save Chats",
        value=settings.get("auto_save", True),
    )

    notifications = st.toggle(
        "Email Notifications",
        value=settings.get("notifications", True),
    )

# ==========================================
# Appearance Values
# ==========================================

theme = appearance["theme"]
accent = appearance["accent"]
font_size = appearance["font_size"]
compact_mode = appearance["compact_mode"]
default_model = ai["default_model"]
temperature = ai["temperature"]
conversation_memory = ai["conversation_memory"]
max_tokens = ai["max_tokens"]
email_notifications = notification["email_notifications"]
desktop_notifications = notification["desktop_notifications"]
chat_notifications = notification["chat_notifications"]
weekly_report = notification["weekly_report"]
sound_alerts = notification["sound_alerts"]
marketing_email = notification["marketing_email"]
two_factor = privacy["two_factor"]
login_alerts = privacy["login_alerts"]
session_timeout = privacy["session_timeout"]

# ==========================================
# Save Settings
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

if st.button(
    "ðŸ’¾ Save Settings",
    width="stretch",
):

    success, message = save_settings(

        email=email,

        theme=theme,

        accent=accent,

        font_size=font_size,

        compact_mode=compact_mode,

        language=language,

        default_model=default_model,

        temperature=temperature,

        auto_save=auto_save,

        notifications=notifications,

        conversation_memory=conversation_memory,

        max_tokens=max_tokens,

        email_notifications=email_notifications,

        desktop_notifications=desktop_notifications,

        chat_notifications=chat_notifications,

        weekly_report=weekly_report,

        sound_alerts=sound_alerts,

        marketing_email=marketing_email,

        two_factor=two_factor,

        login_alerts=login_alerts,

        session_timeout=session_timeout,

    )

    if success:
        st.success(message)
    else:
        st.error(message)