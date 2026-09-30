"""
=========================================
NovaMind AI - Privacy Settings
=========================================
"""

import streamlit as st


def show_privacy_settings(settings):

    st.subheader("🔐 Privacy & Security")

    left, right = st.columns(2)

    with left:

        two_factor = st.toggle(
            "🔒 Two-Factor Authentication",
            value=settings.get(
                "two_factor",
                False
            )
        )

        login_alerts = st.toggle(
            "🚨 Login Alerts",
            value=settings.get(
                "login_alerts",
                True
            )
        )

        session_timeout = st.selectbox(
            "Session Timeout",
            [
                "15 Minutes",
                "30 Minutes",
                "1 Hour",
                "Never"
            ],
            index=2
        )

    with right:

        st.info(
            "Manage your account security and privacy settings."
        )

        export_data = st.button(
            "📥 Download My Data",
            use_container_width=True,
            key="export_data"
        )

        delete_account = st.button(
            "🗑 Delete Account",
            use_container_width=True,
            key="delete_account"
        )

        logout = st.button(
            "🚪 Logout",
            use_container_width=True,
            key="logout"
        )

    return {

        "two_factor": two_factor,

        "login_alerts": login_alerts,

        "session_timeout": session_timeout,

        "export_data": export_data,

        "delete_account": delete_account,

        "logout": logout,

    }