"""
=========================================
NovaMind AI - PDF Chat
=========================================

Chat with one uploaded PDF.
"""

import streamlit as st

from utils.styles import load_css

from components.sidebar import show_sidebar
from components.navbar import show_navbar

from components.pdf.chat_window import show_chat_window
from components.pdf.chat_input import show_chat_input
from components.pdf.source_cards import show_source_cards

from services.pdf.pdf_service import PDFService
from services.pdf.pdf_chat_history_service import (
    PDFChatHistoryService,
)

# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="NovaMind AI | PDF Chat",
    page_icon="📄",
    layout="wide",
)

# ==========================================
# Authentication
# ==========================================

if not st.session_state.get("logged_in", False):

    st.switch_page("pages/login.py")

    st.stop()

# ==========================================
# Current Page
# ==========================================

st.session_state["current_page"] = "PDF Chat"

# ==========================================
# CSS
# ==========================================

load_css("pdf_chat.css")

# ==========================================
# Layout
# ==========================================

st.session_state["current_page"] = "PDF Chat"
show_sidebar()
show_navbar(is_chat=False)

# ==========================================
# Selected PDF
# ==========================================

pdf_id = st.session_state.get("selected_pdf")

if not pdf_id:

    st.warning("⚠ Please select a PDF first.")

    st.stop()

# ==========================================
# Get PDF Information
# ==========================================

pdf = PDFService.get_pdf(pdf_id)

if not pdf:

    st.error("❌ PDF not found.")

    st.stop()

# ==========================================
# Reset Chat When PDF Changes
# ==========================================

current_pdf = st.session_state.get("current_pdf")

if current_pdf != pdf_id:

    st.session_state.current_pdf = pdf_id

    st.session_state.pdf_messages = []

    st.session_state.pdf_sources = []

# ==========================================
# Initialize Session
# ==========================================

if "pdf_messages" not in st.session_state:

    st.session_state.pdf_messages = []

if "pdf_sources" not in st.session_state:

    st.session_state.pdf_sources = []

# ==========================================
# Load Previous History
# ==========================================

if not st.session_state.pdf_messages:

    try:

        chats = PDFChatHistoryService.load(

            email=st.session_state["email"],

            pdf_id=pdf_id,

        )

        for chat in chats:

            st.session_state.pdf_messages.append(
                {
                    "role": "user",
                    "content": chat["question"],
                }
            )

            st.session_state.pdf_messages.append(
                {
                    "role": "assistant",
                    "content": chat["answer"],
                }
            )

    except Exception as e:

        print("=" * 60)
        print("PDF CHAT HISTORY ERROR")
        print(e)
        print("=" * 60)

# ==========================================
# Header
# ==========================================

st.title("💬 Chat with PDF")

st.caption(f"📄 {pdf['filename']}")

st.write(
    "Ask questions, summarize content, and explore your uploaded document."
)

st.divider()

# ==========================================
# Chat Window
# ==========================================

show_chat_window(pdf_id)

# ==========================================
# Chat Input
# ==========================================

show_chat_input(pdf_id)

# ==========================================
# Sources
# ==========================================

if st.session_state.pdf_sources:

    st.divider()

    show_source_cards(
        st.session_state.pdf_sources
    )