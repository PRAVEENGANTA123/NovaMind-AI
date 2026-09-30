"""
=========================================
NovaMind AI - Chat Sidebar
=========================================
"""

import streamlit as st


def show_chat_sidebar():

    st.subheader("💬 Conversations")

    # ==========================
    # New Chat
    # ==========================

    if st.button(
        "➕ New Chat",
        width="stretch",
        key="new_chat_btn",
    ):

        st.session_state["current_chat"] = None

        st.session_state["messages"] = []

        st.rerun()

    st.divider()

    # ==========================
    # Search
    # ==========================

    search = st.text_input(
        "Search Chats",
        placeholder="Search...",
        label_visibility="collapsed",
        key="chat_sidebar_search",
    )

    st.divider()

    # ==========================
    # Quick Menu
    # ==========================

    st.markdown("### ⭐ Favorites")

    st.caption("Coming Soon")

    st.markdown("### 📂 Collections")

    st.caption("Coming Soon")

    st.divider()

    # ==========================
    # Recent Chats
    # ==========================

    st.markdown("### 🕒 Recent Chats")

    demo_chats = [

        "🐍 Python Interview",

        "📄 Resume Review",

        "🤖 AI Agent",

        "📚 Machine Learning",

        "🌐 Web Research",

    ]

    for chat in demo_chats:

        if search:

            if search.lower() not in chat.lower():

                continue

        st.button(

            chat,

            width="stretch",

            key=f"chat_{chat}",

        )