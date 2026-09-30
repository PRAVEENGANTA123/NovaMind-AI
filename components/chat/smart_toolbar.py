"""
=========================================
NovaMind AI - Smart Toolbar (Condensed Menu)
=========================================
"""

import streamlit as st


def show_smart_toolbar():
    """
    Renders top chat actions organized into a clean dropdown menu.
    """
    col_spacer, col_menu = st.columns([0.82, 0.18], gap="small")

    with col_menu:
        with st.popover("⚙️ Chat Options", use_container_width=True):
            st.markdown("#### 💬 Chat Actions")

            # 1. New Chat
            if st.button("🆕 New Chat", key="menu_new_chat_btn", use_container_width=True):
                st.session_state.messages = []
                st.session_state["submitted_prompt"] = None
                st.session_state.active_url = None
                st.session_state.active_domain = None
                st.session_state.url_analysis_result = None
                st.rerun()

            # 2. Favorite Toggle
            fav_state = st.session_state.get("is_favorite", False)
            fav_label = "⭐ Favorited" if fav_state else "☆ Add to Favorites"
            if st.button(fav_label, key="menu_fav_btn", use_container_width=True):
                st.session_state["is_favorite"] = not fav_state
                st.rerun()

            # 3. Export Trigger
            if st.button("📤 Export Chat", key="menu_export_btn", use_container_width=True):
                st.session_state["show_export_modal"] = True
                st.rerun()

            # 4. Clear Canvas
            if st.button("🗑️ Clear History", key="menu_clear_btn", use_container_width=True):
                st.session_state.messages = []
                st.session_state["submitted_prompt"] = None
                st.rerun()

            st.divider()

            # 5. Persona / Mode Select
            st.markdown("#### 🧠 Persona Mode")
            st.selectbox(
                "Persona",
                ["General AI", "Code Specialist", "Document RAG", "Research Analyst"],
                key="menu_persona_mode",
                label_visibility="collapsed",
            )