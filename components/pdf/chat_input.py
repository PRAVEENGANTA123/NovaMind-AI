"""
=========================================
NovaMind AI - PDF Chat Input
=========================================
"""

import streamlit as st

from services.pdf.pdf_chat_service import PDFChatService


def show_chat_input(pdf_id):
    """
    Chat input component.
    """

    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []

    prompt = st.chat_input(
        "Ask anything about this PDF..."
    )

    if not prompt:
        return

    # -----------------------------
    # Show User Message
    # -----------------------------

    st.session_state.pdf_messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # -----------------------------
    # AI Response
    # -----------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                chat = PDFChatService()
                result = chat.ask(
                     pdf_id=pdf_id,
                     question=prompt,
                    )
                answer = result["answer"]

            except Exception as e:

                answer = f"❌ {e}"

            st.markdown(answer)

    # -----------------------------
    # Save Assistant Response
    # -----------------------------

    st.session_state.pdf_messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
    from services.pdf.pdf_chat_history_service import (
    PDFChatHistoryService,
    )

    PDFChatHistoryService.save(
    email=st.session_state["email"],
    pdf_id=pdf_id,
    question=prompt,
    answer=answer,
    )

    st.rerun()