"""
=========================================
NovaMind AI - Profile Dashboard
=========================================
"""

import streamlit as st
from services.dashboard_service import get_dashboard_stats


def show_profile_dashboard(email):

    stats = get_dashboard_stats(email)

    st.markdown("## 📊 Workspace Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "💬 Chats",
            stats.get("total_chats", 0)
        )

    with c2:
        st.metric(
            "📄 PDFs",
            stats.get("total_pdfs", 0)
        )

    with c3:
        st.metric(
            "⭐ Bookmarks",
            stats.get("bookmarks", 0)
        )

    with c4:
        st.metric(
            "💬 Messages",
            stats.get("messages", 0)
        )

    st.divider()

    st.markdown("## ⚡ Quick Actions")

    a1, a2, a3 = st.columns(3)

    with a1:
        if st.button(
            "📤 Export Profile",
            width="stretch",
            key="export_profile"
        ):
            st.info("Coming Soon")

    with a2:
        if st.button(
            "📥 Download My Data",
            width="stretch",
            key="download_data"
        ):
            st.info("Coming Soon")

    with a3:
        if st.button(
            "🚪 Logout",
            width="stretch",
            key="logout_profile"
        ):
            st.session_state.clear()
            st.switch_page("pages/login.py")