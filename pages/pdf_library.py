"""
=========================================
NovaMind AI - PDF Library
=========================================
"""
import streamlit as st
from utils.styles import load_css
from components.sidebar import show_sidebar
from components.navbar import show_navbar
from components.pdf.pdf_upload import show_pdf_upload
from components.pdf.pdf_list import show_pdf_list
from utils.responsive import apply_responsive_layout

# ==========================================
# Page Configuration
# ==========================================

# MUST be the first Streamlit command
st.set_page_config(
    page_title="NovaMind AI | PDF Library",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="auto"
)

# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()
    
# ==========================================
# ==========================================


st.session_state["current_page"] = "PDF Library"

# ==========================================
# Authentication
# ==========================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()

# ==========================================
# Load CSS
# ==========================================

load_css("pdf_library.css")

# ==========================================
# Sidebar & Navbar
# ==========================================

st.session_state["current_page"] = "PDF Library"
show_sidebar()
show_navbar(is_chat=False)

# ==========================================
# Header
# ==========================================

st.title("ðŸ“„ PDF Library")
st.caption("Upload, manage, and chat with your PDF documents.")

st.divider()

# ==========================================
# Current User
# ==========================================

email = st.session_state.get("email")

if not email:
    st.error("âŒ User session not found.")
    st.stop()

# ==========================================
# Upload Section
# ==========================================

with st.container(border=True):
    show_pdf_upload(email)

st.divider()

# ==========================================
# PDF Library
# ==========================================

with st.container(border=True):
    show_pdf_list(email)