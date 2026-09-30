"""
=========================================
NovaMind AI - Recent Chats
=========================================

Displays the latest AI conversations
for the current user.
"""

from datetime import datetime

import streamlit as st

from database.mongodb import chats_collection


# =====================================
# Time Formatter
# =====================================

def format_time(dt):
    """
    Convert datetime into a readable format.
    """

    if not dt:
        return "Unknown"

    now = datetime.utcnow()

    diff = now - dt

    if diff.days == 0:

        seconds = diff.seconds

        if seconds < 60:
            return "Just now"

        if seconds < 3600:
            return f"{seconds // 60} min ago"

        return f"{seconds // 3600} hr ago"

    if diff.days == 1:
        return "Yesterday"

    if diff.days < 7:
        return f"{diff.days} days ago"

    return dt.strftime("%d %b %Y")


# =====================================
# Recent Chats
# =====================================

def show_recent_chats(email: str):
    """
    Display recent chat conversations.
    """

    left, right = st.columns(
        [4, 1]
    )

    with left:

        st.subheader("💬 Recent Chats")

    with right:

        if st.button(

            "View All",

            key="recent_chats_view_all",

            width="stretch",

        ):

            st.switch_page(
                "pages/history.py"
            )

    st.markdown("")

    # ---------------------------------
    # MongoDB
    # ---------------------------------

    chats = list(

        chats_collection.find(
            {
                "email": email
            }
        ).sort(
            "created_at",
            -1,
        ).limit(5)

    )

    # ---------------------------------
    # Empty State
    # ---------------------------------

    if not chats:

        st.info(
            "💬 No conversations yet."
        )

        return

    # ---------------------------------
    # Chat Cards
    # ---------------------------------

    for chat in chats:

        prompt = chat.get(
            "prompt",
            "Untitled Chat"
        )

        response = chat.get(
            "response",
            ""
        )

        created = chat.get(
            "created_at"
        )

        agent = chat.get(
            "agent",
            "AI"
        )

        with st.container(border=True):

            st.markdown(
                f"#### 💬 {prompt[:55]}"
            )

            if len(prompt) > 55:

                st.caption(
                    prompt
                )

            if response:

                st.write(
                    response[:120] + (
                        "..."
                        if len(response) > 120
                        else ""
                    )
                )

            col1, col2 = st.columns(
                [2, 1]
            )

            with col1:

                st.caption(
                    f"🤖 {agent}"
                )

            with col2:

                st.caption(
                    format_time(created)
                )