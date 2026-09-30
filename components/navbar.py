"""
=========================================
NovaMind AI - Navigation Bar
=========================================

Top unified navigation bar for all pages.
Menu is strictly shown only on the Chat page.
"""

import streamlit as st


def show_navbar(is_chat: bool = None):
    """
    Display top navigation bar.
    Shows '⋮ Menu ⌵' strictly only on the Chat page.
    """
    user_data = st.session_state.get("user", "Guest")
    if isinstance(user_data, dict):
        username = user_data.get("username", "User")
    else:
        username = str(user_data) if user_data else "Guest"

    current_page = st.session_state.get("current_page", "Dashboard")
    is_dashboard = (current_page == "Dashboard")

    # Determine if this is the Chat page
    if is_chat is None:
        is_chat = (current_page.lower() == "chat")

    # Anchor hook for CSS targeting
    st.markdown('<span id="novamind-navbar-anchor" style="display:none;"></span>', unsafe_allow_html=True)

    # Dynamic columns: Menu column allocated ONLY on the Chat page
    if is_chat:
        col_back, col_menu, col_search, col_settings, col_notif, col_profile = st.columns(
            [0.10, 0.11, 0.51, 0.05, 0.05, 0.18],
            gap="small",
            vertical_alignment="center",
        )
    else:
        col_back, col_search, col_settings, col_notif, col_profile = st.columns(
            [0.12, 0.60, 0.05, 0.05, 0.18],
            gap="small",
            vertical_alignment="center",
        )
        col_menu = None

    # 1. Back Button / Brand
    with col_back:
        if not is_dashboard:
            if st.button("← Back", key="navbar_back_btn", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.switch_page("pages/dashboard.py")
        else:
            st.markdown(
                '<div class="navbar-brand-tag">⚡ NovaMind</div>',
                unsafe_allow_html=True,
            )

    # 2. Menu Popover (Rendered ONLY on Chat Page)
    if is_chat and col_menu is not None:
        with col_menu:
            with st.popover("⋮ Menu ⌵", use_container_width=True):
                st.markdown("##### ⚡ Quick Actions")
                if st.button("🆕 New Chat", key="nav_menu_new_chat", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state["submitted_prompt"] = None
                    st.session_state["url_input_value"] = ""
                    st.session_state["active_url"] = None
                    st.rerun()

                if st.button("⭐ Favorite", key="nav_menu_fav_chat", use_container_width=True):
                    st.toast("⭐ Conversation saved to favorites!")

                if st.button("📤 Export", key="nav_menu_export_chat", use_container_width=True):
                    st.session_state["trigger_export"] = True
                    st.toast("📄 Export ready.")

                if st.button("🗑️ Clear Chat", key="nav_menu_clear_chat", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state["submitted_prompt"] = None
                    st.session_state["active_url"] = None
                    st.rerun()

                st.divider()
                st.markdown("##### 🎯 Assistant Mode")
                current_mode = st.selectbox(
                    "Mode Selector",
                    ["General AI", "Code Assistant", "Research Assistant", "Creative Mode"],
                    key="nav_menu_mode_selector",
                    label_visibility="collapsed",
                )
                st.session_state["active_assistant_mode"] = current_mode

    # 3. Search Bar
    with col_search:
        search_query = st.text_input(
            "Search",
            placeholder="🔍 Search chats, PDFs, history...",
            key="navbar_search",
            label_visibility="collapsed",
        )
        if search_query and search_query.strip():
            st.session_state["history_search"] = search_query.strip()
            if st.session_state.get("current_page") != "History":
                st.session_state.current_page = "History"
                st.switch_page("pages/history.py")

    # 4. Settings
    with col_settings:
        if st.button("⚙️", key="navbar_settings_btn", use_container_width=True, help="Settings"):
            st.session_state.current_page = "Settings"
            st.switch_page("pages/settings.py")

    # 5. Notifications
    with col_notif:
        if st.button("🔔", key="navbar_notification", use_container_width=True, help="Notifications"):
            st.toast("✅ All systems operational.")

    # 6. Profile
    with col_profile:
        username_clean = username.upper()
        display_name = username_clean[:14] + "…" if len(username_clean) > 14 else username_clean
        if st.button(f"👤 {display_name}", key="navbar_profile", use_container_width=True, help="View Profile"):
            st.session_state.current_page = "Profile"
            st.switch_page("pages/profile.py")
