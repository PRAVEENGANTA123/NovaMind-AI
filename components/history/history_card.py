"""
=========================================
NovaMind AI - History Card
=========================================

Professional conversation card.
"""

from datetime import datetime

import streamlit as st

from services.chat.chat_service import ChatService


def _short(text: str, limit: int = 120):
    """
    Short preview text.
    """

    if not text:
        return ""

    if len(text) <= limit:
        return text

    return text[:limit] + "..."


# =====================================
# History Card
# =====================================

def show_history_card(chat):
    """
    Display one professional history card.
    """

    chat_id = str(chat.get("_id"))

    prompt = chat.get("prompt", "")

    response = chat.get("response", "")

    intent = chat.get(
        "intent",
        "general",
    )

    agent = chat.get(
        "agent",
        "NovaMind AI",
    )

    confidence = float(
        chat.get(
            "confidence",
            0,
        )
    )

    created = chat.get("created_at")

    bookmarked = chat.get(
        "bookmarked",
        False,
    )

    liked = chat.get(
        "liked",
        None,
    )

    # ---------------------------------
    # Card
    # ---------------------------------

    with st.container(border=True):

        left, right = st.columns(
            [5, 1]
        )

        with left:

            st.markdown(
                f"### 💬 {_short(prompt, 80)}"
            )

        with right:

            if bookmarked:

                st.markdown(
                    "### 📌"
                )

        # -----------------------------
        # Metadata
        # -----------------------------

        c1, c2, c3 = st.columns(3)

        with c1:

            st.caption(
                f"🧠 {agent}"
            )

        with c2:

            st.caption(
                f"🎯 {intent.title()}"
            )

        with c3:

            if created:

                if isinstance(
                    created,
                    datetime,
                ):

                    created = created.strftime(
                        "%d %b %Y %I:%M %p"
                    )

                st.caption(
                    f"📅 {created}"
                )

        st.markdown(
            "**🤖 Response Preview**"
        )

        st.write(
            _short(
                response,
                180,
            )
        )

        st.markdown(
            "**⭐ Confidence**"
        )

        st.progress(
            min(
                confidence,
                1.0,
            )
        )

        st.caption(
            f"{confidence:.0%} Confidence"
        )

        # -----------------------------
        # Status
        # -----------------------------

        status = []

        if liked is True:

            status.append("👍 Liked")

        elif liked is False:

            status.append("👎 Disliked")

        if bookmarked:

            status.append("📌 Bookmarked")

        if status:

            st.info(
                " | ".join(status)
            )

        st.divider()

        # -----------------------------
        # Actions
        # -----------------------------

        a1, a2, a3 = st.columns(3)

        with a1:

            if st.button(
                "💬 Continue",
                key=f"continue_{chat_id}",
                width="stretch",
            ):

                st.session_state.messages = [

                    {
                        "role": "user",
                        "content": prompt,
                    },

                    {
                        "role": "assistant",
                        "content": response,
                    },

                ]

                st.switch_page(
                    "pages/chat.py"
                )

        with a2:

            if st.button(
                "📤 Export",
                key=f"export_{chat_id}",
                width="stretch",
            ):

                st.info(
                    "Export feature will be connected in the next step."
                )

        with a3:

            if st.button(
                "🗑 Delete",
                key=f"delete_{chat_id}",
                width="stretch",
            ):

                if ChatService.delete(
                    chat_id
                ):

                    st.success(
                        "Conversation deleted."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Failed to delete conversation."
                    )