"""
=========================================
NovaMind AI - Sidebar
=========================================
"""

from pathlib import Path
import streamlit as st
from services.navigation.navigation_service import NavigationService

# ==========================================
# Current Page
# ==========================================

def get_current_page():

    page = Path(st.context.page_script_hash if hasattr(st, "context") else "").name

    # Fallback to session state
    return st.session_state.get("current_page", "")


# ==========================================
# Navigation Button
# ==========================================

def nav_button(label, page, icon):

    active = st.session_state.get("current_page", "") == label

    button_type = "primary" if active else "secondary"

    if st.button(
        f"{icon}  {label}",
        key=f"nav_{label}",
        use_container_width=True,
        type=button_type,
    ):

        # Save current page
        st.session_state["current_page"] = label

        # Add page to navigation history
        NavigationService.visit(page)

        # Navigate
        st.switch_page(page)


# ==========================================
# Sidebar
# ==========================================

def show_sidebar():

    with st.sidebar:

        # =====================================
        # Logo
        # =====================================

        logo = Path("assets/images/logo.png")

        if logo.exists():
            st.image(str(logo), width=90)

        st.markdown(
            """
### NovaMind AI

*Your Intelligent AI Workspace*
"""
        )

        st.divider()

        # =====================================
        # New Chat
        # =====================================

        if st.button(
            "➕ New Chat",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["messages"] = []
            st.session_state["active_url"] = ""
            st.session_state["uploaded_file"] = None
            st.session_state["current_chat_id"] = None
            st.session_state["current_page"] = "Chat"

            NavigationService.visit("pages/chat.py")

            st.switch_page("pages/chat.py")

            # >>> INSERT DIRECTLY BELOW IT:
            if st.button("📌 Pin Conversation", key="sidebar_pin_chat_btn", use_container_width=True):
                is_pinned = st.session_state.get("chat_pinned", False)
                st.session_state["chat_pinned"] = not is_pinned
                st.toast("📌 Chat pinned to top!" if not is_pinned else "Chat unpinned.")

        # =====================================
        # Navigation
        # =====================================

        st.markdown("### Navigation")

        nav_button(
            "Dashboard",
            "pages/dashboard.py",
            "🏠",
        )

        nav_button(
            "Chat",
            "pages/chat.py",
            "💬",
        )

        nav_button(
            "PDF Library",
            "pages/pdf_library.py",
            "📄",
        )

        nav_button(
            "History",
            "pages/history.py",
            "🕒",
        )

        nav_button(
            "Settings",
            "pages/settings.py",
            "⚙️",
        )

        st.divider()

        # =====================================
        # AI Usage
        # =====================================

        st.markdown("### AI Usage")

        total_messages = len(st.session_state.get("messages", []))

        usage = min(total_messages / 100, 1.0)

        st.progress(usage)

        st.caption(f"{total_messages} / 100 Messages Used")

        st.divider()

        # =====================================
        # User Profile
        # =====================================

        username = st.session_state.get("user", "Guest")

        email = st.session_state.get("email", "")

        st.markdown(f"**👤 {username}**")

        if email:
            st.caption(email)

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):
        # Clear user data
            st.session_state.clear()

            # Initialize authentication state
            st.session_state.logged_in = False

            # Restart the app
            st.rerun()