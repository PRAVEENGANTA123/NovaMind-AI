"""
=========================================
NovaMind AI - History Filter Bar
=========================================

Provides filters for
history conversations.
"""

import streamlit as st


def show_history_filters():
    """
    Display history filters.

    Returns:
        dict
    """

    st.markdown("### ⚙️ Filters")

    col1, col2, col3 = st.columns(3)

    with col1:

        agent = st.selectbox(
            "Agent",
            [
                "All",
                "General AI",
                "PDF Assistant",
                "Code Assistant",
                "Web Search",
            ],
            key="history_agent_filter",
        )

    with col2:

        intent = st.selectbox(
            "Intent",
            [
                "All",
                "General",
                "Coding",
                "Reasoning",
                "PDF",
                "Search",
            ],
            key="history_intent_filter",
        )

    with col3:

        date = st.selectbox(
            "Date",
            [
                "All Time",
                "Today",
                "Yesterday",
                "Last 7 Days",
                "Last 30 Days",
            ],
            key="history_date_filter",
        )

    col4, col5 = st.columns(2)

    with col4:

        bookmarks = st.toggle(
            "📌 Bookmarked Only",
            key="history_bookmarks",
        )

    with col5:

        favorites = st.toggle(
            "⭐ Favorites Only",
            key="history_favorites",
        )

    return {
        "agent": agent,
        "intent": intent,
        "date": date,
        "bookmarks": bookmarks,
        "favorites": favorites,
    }