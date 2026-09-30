"""
=========================================
NovaMind AI - Account Information Card
=========================================
"""

import streamlit as st
from datetime import datetime


def format_date(value):

    if not value:
        return "N/A"

    if isinstance(value, datetime):
        return value.strftime("%d %b %Y")

    return str(value)


def show_account_card(profile):

    st.markdown("## 📋 Account Information")
    st.caption("Read-only account details.")

    left, right = st.columns(2)

    with left:

        st.markdown("**👤 Username**")
        st.info(profile.get("username", "N/A"))

        st.markdown("**📧 Email**")
        st.info(profile.get("email", "N/A"))

        st.markdown("**🛡 Role**")
        st.info(profile.get("role", "User").title())

    with right:

        st.markdown("**🟢 Account Status**")
        st.success(profile.get("status", "Active").title())

        st.markdown("**📅 Member Since**")
        st.info(format_date(profile.get("created_at")))

        st.markdown("**🕒 Last Login**")
        st.info(format_date(profile.get("last_login")))

    st.success("✅ Your account information is synchronized with MongoDB.")