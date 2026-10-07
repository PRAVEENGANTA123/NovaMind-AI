"""
=========================================
NovaMind AI - History
=========================================

Professional conversation history page.
"""
import streamlit as st
from utils.styles import load_css
from components.sidebar import show_sidebar
from components.navbar import show_navbar
from components.history.search_bar import (
    show_history_search,
)
from components.history.filter_bar import (
    show_history_filters,
)
from components.history.history_list import (
    show_history_list,
)
from services.chat.chat_service import ChatService
from utils.responsive import apply_responsive_layout

# ==========================================
# Page Config
# ==========================================

# MUST be the first Streamlit command
st.set_page_config(
    page_title="NovaMind AI | History",
    page_icon="🕒",
    layout="wide"
)

# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()





# ==========================================
# Authentication
# ==========================================

if not st.session_state.get(
    "logged_in",
    False,
):

    st.switch_page(
        "pages/login.py"
    )

    st.stop()

# ==========================================
# Current Page
# ==========================================

st.session_state["current_page"] = "History"

# ==========================================
# CSS
# ==========================================

load_css("history.css")

# ==========================================
# Sidebar + Navbar
# ==========================================

show_sidebar()
show_navbar(is_chat=False)

# ==========================================
# Header
# ==========================================

st.title("🕒 Chat History")

st.caption(
    "Browse, search and manage all your AI conversations."
)

st.divider()

# ==========================================
# Search
# ==========================================

search = show_history_search()

# ==========================================
# Filters
# ==========================================

filters = show_history_filters()

st.divider()

# ==========================================
# Load Chats
# ==========================================

email = st.session_state.get("email")

try:

    chats = ChatService.history(email)

except Exception as e:

    st.error(e)

    chats = []

# ==========================================
# Summary
# ==========================================

left, right = st.columns([3, 1])

with left:

    st.metric(
        "Total Conversations",
        len(chats),
    )

with right:

    if st.button(
        "🔄 Refresh",
        width="stretch",
    ):

        st.rerun()

st.divider()

# ==========================================
# Conversation List
# ==========================================

show_history_list(

    chats=chats,

    search=search,

    filters=filters,

)