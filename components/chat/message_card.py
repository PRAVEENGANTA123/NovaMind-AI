"""
=========================================
NovaMind AI - Message Card
=========================================

Displays one chat message with
interactive actions.
"""

from datetime import datetime
import uuid

import streamlit as st

from services.chat.chat_service import ChatService
from services.ai.voice_service import VoiceService


def show_message_card(
    role,
    message,
    chat_id=None,
    timestamp=None,
    message_id=None,
):
    """
    Display one chat message.
    """

    if timestamp is None:
        timestamp = datetime.now().strftime("%I:%M %p")

    if message_id is None:
        message_id = uuid.uuid4().hex

    is_user = role.lower() == "user"

    # =====================================
    # User Message
    # =====================================

    if is_user:
        with st.chat_message("user", avatar="👤"):
            st.markdown(message)
            st.caption(timestamp)
        return

    # =====================================
    # Assistant Message
    # =====================================

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(message)

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        # ---------------------------------
        # Like
        # ---------------------------------
        with col1:
            if st.button("👍", key=f"like_{message_id}", width="stretch"):
                if chat_id:
                    ChatService.like_chat(chat_id)
                    st.toast("👍 Liked")

        # ---------------------------------
        # Dislike
        # ---------------------------------
        with col2:
            if st.button("👎", key=f"dislike_{message_id}", width="stretch"):
                if chat_id:
                    ChatService.dislike_chat(chat_id)
                    st.toast("👎 Disliked")

        # ---------------------------------
        # Copy
        # ---------------------------------
        with col3:
            if st.button("📋", key=f"copy_{message_id}", width="stretch"):
                st.session_state[f"copy_{message_id}"] = not st.session_state.get(
                    f"copy_{message_id}", False
                )

        # ---------------------------------
        # Regenerate
        # ---------------------------------
        with col4:
            if st.button("🔄", key=f"regen_{message_id}", width="stretch"):
                st.session_state["regenerate"] = True
                st.rerun()

        # ---------------------------------
        # Voice (TTS Audio Playback)
        # ---------------------------------
        with col5:
            if st.button("🔊", key=f"voice_{message_id}", width="stretch", help="Listen to answer"):
                with st.spinner("Synthesizing audio..."):
                    audio_bytes = VoiceService.text_to_speech(message)
                    if audio_bytes:
                        st.session_state[f"audio_bytes_{message_id}"] = audio_bytes
                    else:
                        st.warning("Could not synthesize speech.")

        # ---------------------------------
        # Bookmark
        # ---------------------------------
        with col6:
            if st.button("📌", key=f"bookmark_{message_id}", width="stretch"):
                if chat_id:
                    ChatService.bookmark_chat(chat_id)
                    st.toast("📌 Bookmarked")

        # ---------------------------------
        # Expanders / Dynamic Triggers
        # ---------------------------------
        if st.session_state.get(f"copy_{message_id}", False):
            with st.expander("📋 Copy Response", expanded=True):
                st.code(message, language=None)

        if st.session_state.get(f"audio_bytes_{message_id}"):
            st.audio(
                st.session_state[f"audio_bytes_{message_id}"],
                format="audio/mp3",
                autoplay=True,
            )

        st.caption(timestamp)