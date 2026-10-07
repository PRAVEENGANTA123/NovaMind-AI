"""
=========================================
NovaMind AI - User Profile
=========================================
"""
import streamlit as st
from utils.styles import load_css
from components.sidebar import show_sidebar
from components.navbar import show_navbar
from components.profile_header import show_profile_header
from components.profile_avatar import show_profile_avatar
from components.profile_form import show_profile_form
from components.security_card import show_security_card
from services.profile_service import load_profile
from components.account_card import show_account_card
from components.profile_dashboard import show_profile_dashboard
from utils.responsive import apply_responsive_layout

# ==========================================
# Page Config
# ==========================================

# MUST be the first Streamlit command
st.set_page_config(
    page_title="NovaMind AI | Profile",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="auto"
)

# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()

# ==========================================
# ==========================================



# ==========================================
# Authentication
# ==========================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()

# ==========================================
# Load CSS
# ==========================================

load_css("profile.css")

# ==========================================
# Sidebar & Navbar
# ==========================================

# ==========================================
# Sidebar & Navbar
# ==========================================

st.session_state["current_page"] = "Profile"
show_sidebar()
show_navbar(is_chat=False)

# ==========================================
# Load User
# ==========================================

email = st.session_state.get("email")

profile = load_profile(email)

if profile is None:
    st.error("Unable to load profile.")
    st.stop()

# ==========================================
# Profile Header
# ==========================================

show_profile_header(profile)

# ==========================================
# Layout
# ==========================================

left, right = st.columns([1, 2], gap="large")

# =========================================================
# LEFT SIDE
# =========================================================

with left:
    show_profile_avatar(
        profile,
        email
    )

# =========================================================
# RIGHT SIDE
# =========================================================

with right:

    show_profile_form(
        profile,
        email
    )
    
# ==========================================
# Change Password
# ==========================================

st.divider()

show_security_card(email)

st.divider()

show_account_card(profile)

st.divider()

show_profile_dashboard(email)