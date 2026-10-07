"""
=========================================
NovaMind AI - Dashboard
=========================================
"""

from datetime import datetime
import streamlit as st
from utils.styles import load_css
from services.dashboard_service import DashboardService
from components.sidebar import show_sidebar
from components.navbar import show_navbar
from components.dashboard_cards import show_dashboard_cards
from components.dashboard_activity import show_dashboard_activity
from components.dashboard_storage import show_dashboard_storage
from components.dashboard_agents import show_dashboard_agents
from components.dashboard_quick_actions import show_dashboard_quick_actions
from components.recent_chats import show_recent_chats
from utils.responsive import apply_responsive_layout

# ==========================================
# Page Config
# ==========================================

# MUST be the first Streamlit command
st.set_page_config(
    page_title="NovaMind AI | Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="auto"
)

# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()
# ==========================================
# ==========================================


# ==========================================
# Session
# ==========================================

st.session_state["current_page"] = "Dashboard"

# ==========================================
# Authentication
# ==========================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()

# ==========================================
# CSS
# ==========================================

load_css("dashboard.css")
load_css("dashboard_cards.css")

# ==========================================
# Layout
# ==========================================

show_sidebar()
show_navbar(is_chat=False)

# ==========================================
# User
# ==========================================

email = st.session_state.get("email")

if not email:
    st.error("Session expired.")
    st.switch_page("pages/login.py")
    st.stop()

# ==========================================
# Dashboard Data
# ==========================================

stats = DashboardService.get_dashboard_stats(email)

username = stats.get("username", "User")

# ==========================================
# Greeting
# ==========================================

now = datetime.now()

if now.hour < 12:
    greeting = "Good Morning â˜€ï¸"
elif now.hour < 17:
    greeting = "Good Afternoon ðŸŒ¤ï¸"
else:
    greeting = "Good Evening ðŸŒ™"

left, right = st.columns([5, 1])

with left:

    st.title(f"ðŸ‘‹ Welcome back, {username}")

    st.subheader(greeting)

    st.write(
        "Manage your AI workspace and monitor your activity."
    )

    st.caption(
        f"Chats: {stats['total_chats']} | "
        f"PDFs: {stats['total_pdfs']} | "
        f"Messages: {stats['messages']}"
    )

with right:

    st.metric(
        "Current Time",
        now.strftime("%I:%M %p"),
    )

    st.caption(
        now.strftime("%A, %d %B %Y")
    )

st.divider()

# ==========================================
# Refresh
# ==========================================

if st.button(
    "ðŸ”„ Refresh Dashboard",
    use_container_width=False,
):
    st.rerun()

# ==========================================
# Dashboard Cards
# ==========================================

show_dashboard_cards(stats)

st.divider()

# ==========================================
# Activity
# ==========================================

left, right = st.columns([2.3, 1])

with left:

    with st.container(border=True):

        st.subheader("ðŸ“ˆ Chat Activity")

        show_dashboard_activity(email)

with right:

    with st.container(border=True):

        show_recent_chats(email)

st.divider()

# ==========================================
# Bottom Section
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        show_dashboard_agents(email)

with col2:

    with st.container(border=True):

        show_dashboard_storage(email)

with col3:

    with st.container(border=True):

        show_dashboard_quick_actions()