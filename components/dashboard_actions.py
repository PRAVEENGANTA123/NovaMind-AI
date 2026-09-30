import streamlit as st


def show_dashboard_actions():

    st.subheader("⚡ Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.button(
            "💬 New Chat",
            use_container_width=True
        ):
            st.switch_page("pages/chat.py")

    with col2:

        if st.button(
            "📄 Upload PDF",
            use_container_width=True
        ):
            st.switch_page("pages/pdf_library.py")

    with col3:

        if st.button(
            "🕒 History",
            use_container_width=True
        ):
            st.switch_page("pages/history.py")

    with col4:

        if st.button(
            "⚙️ Settings",
            use_container_width=True
        ):
            st.switch_page("pages/settings.py")