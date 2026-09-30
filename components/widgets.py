import streamlit as st


def show_quick_actions():
    """
    Dashboard Quick Actions
    """

    st.subheader("🚀 Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button(
            "💬 AI Chat",
            use_container_width=True
        ):
            st.switch_page("pages/chat.py")

    with col2:
        if st.button(
            "📄 PDF Library",
            use_container_width=True
        ):
            st.switch_page("pages/pdf_library.py")

    with col3:
        if st.button(
            "🕒 History",
            use_container_width=True
        ):
            st.switch_page("pages/history.py")

    with col4:
        if st.button(
            "⚙ Settings",
            use_container_width=True
        ):
            st.switch_page("pages/settings.py")


def show_recent_activity():
    """
    Recent Activity Section
    """

    st.subheader("📊 Recent Activity")

    st.info("No recent activity available.")

    st.markdown(
        """
- 🤖 Gemini AI Connected
- 💾 MongoDB Connected
- 💬 Chat Service Active
- 📄 PDF Module Ready
"""
    )