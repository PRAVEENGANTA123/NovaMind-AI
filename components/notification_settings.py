"""
=========================================
NovaMind AI - Notification Settings
=========================================
"""

import streamlit as st


def show_notification_settings(settings):

    st.subheader("🔔 Notifications")

    left, right = st.columns(2)

    with left:

        email_notifications = st.toggle(
            "📧 Email Notifications",
            value=settings.get(
                "email_notifications",
                True
            )
        )

        desktop_notifications = st.toggle(
            "💻 Desktop Notifications",
            value=settings.get(
                "desktop_notifications",
                True
            )
        )

        chat_notifications = st.toggle(
            "💬 Chat Notifications",
            value=settings.get(
                "chat_notifications",
                True
            )
        )

    with right:

        weekly_report = st.toggle(
            "📅 Weekly Report",
            value=settings.get(
                "weekly_report",
                False
            )
        )

        sound_alerts = st.toggle(
            "🔊 Sound Alerts",
            value=settings.get(
                "sound_alerts",
                True
            )
        )

        marketing_email = st.toggle(
            "📨 Product Updates",
            value=settings.get(
                "marketing_email",
                False
            )
        )

    return {

        "email_notifications": email_notifications,

        "desktop_notifications": desktop_notifications,

        "chat_notifications": chat_notifications,

        "weekly_report": weekly_report,

        "sound_alerts": sound_alerts,

        "marketing_email": marketing_email,

    }