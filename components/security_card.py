"""
=========================================
NovaMind AI - Security Card
=========================================
"""

import streamlit as st
from services.security_service import update_password


def show_security_card(email):

    st.subheader("🔒 Security")

    current_password = st.text_input(
        "Current Password",
        type="password",
        key="current_password",
    )

    new_password = st.text_input(
        "New Password",
        type="password",
        key="new_password",
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password",
    )

    if st.button(
        "Update Password",
        width="stretch",
        key="update_password_btn",
    ):

        success, message = update_password(
            email=email,
            current_password=current_password,
            new_password=new_password,
            confirm_password=confirm_password,
        )

        if success:
            st.success(message)
        else:
            st.error(message)