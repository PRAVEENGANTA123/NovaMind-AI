"""
=========================================
NovaMind AI - Dashboard Cards
=========================================
"""

import streamlit as st


def dashboard_card(icon, title, value, subtitle):

    with st.container(border=True):

        icon_col, text_col = st.columns([1, 4])

        with icon_col:
            st.markdown(
                f"<h1 style='text-align:center'>{icon}</h1>",
                unsafe_allow_html=True,
            )

        with text_col:

            st.caption(title)

            st.markdown(
                f"## {value}"
            )

            st.caption(subtitle)


def show_dashboard_cards(stats):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        dashboard_card(
            "💬",
            "Total Chats",
            stats.get("total_chats", 0),
            f"{stats.get('messages',0)} Messages",
        )

    with c2:
        dashboard_card(
            "📄",
            "PDF Library",
            stats.get("total_pdfs", 0),
            "Uploaded PDFs",
        )

    with c3:
        dashboard_card(
            "🔖",
            "Bookmarks",
            stats.get("bookmarks", 0),
            "Saved Items",
        )

    with c4:
        dashboard_card(
            "⚡",
            "Messages",
            stats.get("messages", 0),
            "AI Conversations",
        )