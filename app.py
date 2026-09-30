"""
=========================================
NovaMind AI
Main Application
=========================================
"""

import streamlit as st

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="NovaMind AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# Initialize Session
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# Protected Pages
# ==========================================

dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="🏠",
)

chat = st.Page(
    "pages/chat.py",
    title="Chat",
    icon="💬",
)

pdf_library = st.Page(
    "pages/pdf_library.py",
    title="PDF Library",
    icon="📄",
)

history = st.Page(
    "pages/history.py",
    title="History",
    icon="🕒",
)

settings = st.Page(
    "pages/settings.py",
    title="Settings",
    icon="⚙️",
)
profile = st.Page(
    "pages/profile.py",
    title="Profile",
    icon="👤",
)


# ==========================================
# Authentication Pages
# ==========================================

login = st.Page(
    "pages/login.py",
    title="Login",
)

register = st.Page(
    "pages/register.py",
    title="Register",
)

forgot_password = st.Page(
    "pages/forgot_password.py",
    title="Forgot Password",
)

verify_email = st.Page(
    "pages/verify_email.py",
    title="Verify Email",
)
otp_verification = st.Page(
    "pages/otp_verification.py",
    title="OTP Verification"
)

# ==========================================
# Navigation
# ==========================================

if st.session_state.logged_in:

    pages = [
        dashboard,
        chat,
        pdf_library,
        history,
        settings,
        profile,
    ]
else:

    pages = [
        login,
        register,
        forgot_password,
        verify_email,
        otp_verification,
    ]

navigation = st.navigation(
    pages,
    position="hidden",
)

# ==========================================
# Run
# ==========================================

navigation.run()