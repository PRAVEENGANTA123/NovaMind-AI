"""
=========================================
NovaMind AI - History List
=========================================

Displays the complete history list
with search, filtering, sorting,
and pagination.
"""

import math

import streamlit as st

from components.history.history_card import (
    show_history_card,
)


# =====================================
# History List
# =====================================

def show_history_list(
    chats,
    search="",
    filters=None,
):
    """
    Display chat history.
    """

    if filters is None:
        filters = {}

    filtered = chats

    # =====================================
    # Search
    # =====================================

    if search:

        query = search.lower()

        filtered = [

            chat

            for chat in filtered

            if (

                query in chat.get(
                    "prompt",
                    "",
                ).lower()

                or

                query in chat.get(
                    "response",
                    "",
                ).lower()

                or

                query in chat.get(
                    "agent",
                    "",
                ).lower()

                or

                query in chat.get(
                    "intent",
                    "",
                ).lower()

            )

        ]

    # =====================================
    # Agent Filter
    # =====================================

    agent = filters.get("agent")

    if agent and agent != "All":

        filtered = [

            chat

            for chat in filtered

            if chat.get(
                "agent",
                "",
            ) == agent

        ]

    # =====================================
    # Intent Filter
    # =====================================

    intent = filters.get("intent")

    if intent and intent != "All":

        filtered = [

            chat

            for chat in filtered

            if chat.get(
                "intent",
                "",
            ).lower()

            == intent.lower()

        ]

    # =====================================
    # Bookmarks
    # =====================================

    if filters.get("bookmarks"):

        filtered = [

            chat

            for chat in filtered

            if chat.get(
                "bookmarked",
                False,
            )

        ]

    # =====================================
    # Favorites
    # =====================================

    if filters.get("favorites"):

        filtered = [

            chat

            for chat in filtered

            if chat.get(
                "liked",
                False,
            )

        ]

    # =====================================
    # Empty
    # =====================================

    if not filtered:

        st.info(
            "No conversations found."
        )

        return

    # =====================================
    # Sort
    # =====================================

    filtered.sort(

        key=lambda x: x.get(
            "created_at",
        ),

        reverse=True,

    )

    # =====================================
    # Pagination
    # =====================================

    PER_PAGE = 10

    pages = max(
        1,
        math.ceil(
            len(filtered) / PER_PAGE
        ),
    )

    page = st.number_input(

        "Page",

        min_value=1,

        max_value=pages,

        value=1,

        key="history_page",

    )

    start = (
        page - 1
    ) * PER_PAGE

    end = start + PER_PAGE

    current = filtered[start:end]

    st.caption(

        f"Showing {len(current)} of {len(filtered)} conversations"

    )

    st.divider()

    # =====================================
    # Cards
    # =====================================

    for chat in current:

        show_history_card(
            chat
        )