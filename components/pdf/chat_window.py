"""
=========================================
NovaMind AI - PDF Chat Window
=========================================

Displays conversation history for
the selected PDF.
"""

import streamlit as st


def show_chat_window(pdf_id):
    """
    Display PDF chat history.
    """

    messages = st.session_state.get(
        "pdf_messages",
        [],
    )

    # =====================================
    # Empty Conversation
    # =====================================

    if not messages:

        st.info(
            "👋 Welcome! Ask any question about your uploaded PDF."
        )

        st.markdown(
            """
### 💡 Example Questions

- Summarize this PDF.
- What is the main topic?
- Explain Chapter 2.
- List the important points.
- What are the conclusions?
- Give me key definitions.
- What technologies are discussed?
- Explain this in simple language.
            """
        )

        return

    # =====================================
    # Display Messages
    # =====================================

    for message in messages:

        role = message.get("role", "assistant")

        content = message.get("content", "")

        with st.chat_message(role):

            st.markdown(content)

    # =====================================
    # Conversation Statistics
    # =====================================

    user_count = sum(
        1
        for message in messages
        if message.get("role") == "user"
    )

    assistant_count = sum(
        1
        for message in messages
        if message.get("role") == "assistant"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Questions",
            user_count,
        )

    with col2:

        st.metric(
            "Answers",
            assistant_count,
        )