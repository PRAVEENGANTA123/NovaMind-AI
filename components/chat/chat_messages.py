"""
=========================================
NovaMind AI - Chat Messages
=========================================

Displays the complete conversation
between the user and NovaMind AI.
"""

import uuid
import streamlit as st

from components.chat.chat_welcome import show_chat_welcome
from components.chat.message_card import show_message_card


# =====================================
# Chat Messages
# =====================================

def show_chat_messages():
    """
    Display the complete conversation with inline editing support.
    """

    # ---------------------------------
    # Initialize Messages & Edit State
    # ---------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "editing_message_idx" not in st.session_state:
        st.session_state.editing_message_idx = None

    messages = st.session_state.messages

    # ---------------------------------
    # Empty Conversation
    # ---------------------------------
    if not messages:
        show_chat_welcome()
        return

    # ---------------------------------
    # Conversation Loop
    # ---------------------------------
    for index, message in enumerate(messages):
        role = message.get("role", "assistant")
        content = message.get("content", "")
        timestamp = message.get("timestamp")
        chat_id = message.get("chat_id")
        message_id = message.get("message_id")

        if not message_id:
            message_id = uuid.uuid4().hex
            message["message_id"] = message_id

        # Check if this specific user message is currently being edited
        is_editing = (
            role == "user"
            and st.session_state.get("editing_message_idx") == index
        )

        if is_editing:
            # -------------------------------------------------------------
            # Inline Edit Mode (Capsule Input + Cancel / Update)
            # -------------------------------------------------------------
            edited_text = st.text_input(
                "Edit Message",
                value=content,
                key=f"edit_input_{message_id}_{index}",
                label_visibility="collapsed",
            )

            col_spacer, col_cancel, col_update = st.columns([0.76, 0.12, 0.12], gap="small")

            with col_cancel:
                if st.button("Cancel", key=f"cancel_btn_{message_id}_{index}", use_container_width=True):
                    st.session_state.editing_message_idx = None
                    st.rerun()

            with col_update:
                if st.button("Update", key=f"update_btn_{message_id}_{index}", use_container_width=True):
                    cleaned = edited_text.strip()
                    if cleaned and cleaned != content:
                        # Update prompt text
                        st.session_state.messages[index]["content"] = cleaned
                        # Trim any subsequent assistant turns so it re-generates freshly
                        st.session_state.messages = st.session_state.messages[: index + 1]
                        # Send updated prompt to the chat submission trigger
                        st.session_state["submitted_prompt"] = cleaned

                    st.session_state.editing_message_idx = None
                    st.rerun()

        else:
            # -------------------------------------------------------------
            # Standard Message Card Display
            # -------------------------------------------------------------
            show_message_card(
                role=role,
                message=content,
                chat_id=chat_id,
                timestamp=timestamp,
                message_id=message_id,
            )

            # For user messages, display [Copy] and [Edit] action buttons below the card
            if role == "user":
                btn_c1, btn_c2, _ = st.columns([0.05, 0.05, 0.90], gap="small")

                with btn_c1:
                    if st.button("⧉", key=f"copy_msg_{message_id}_{index}", help="Copy message"):
                        st.toast("Copied to clipboard!")

                with btn_c2:
                    if st.button("✏️", key=f"edit_msg_{message_id}_{index}", help="Edit message"):
                        st.session_state.editing_message_idx = index
                        st.rerun()