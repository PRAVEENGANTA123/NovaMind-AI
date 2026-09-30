"""
=========================================
NovaMind AI - History Search Bar
=========================================

Search conversations by prompt,
response, agent, or intent.
"""

import streamlit as st


def show_history_search():
    """
    Display the history search bar.

    Returns:
        str: Search text entered by the user.
    """

    st.markdown("### 🔍 Search Conversations")

    search = st.text_input(
        label="Search",
        placeholder=(
            "Search prompts, responses, "
            "agents, or intents..."
        ),
        key="history_search",
        label_visibility="collapsed",
    )

    return search.strip()