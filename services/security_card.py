"""
=========================================
NovaMind AI - Security Card
=========================================
"""

import streamlit as st
from services.security_service import update_password


def show_security_card(email):

    st.markdown("## 🔒 Security")

    st.caption("Update your account password.")

    current_password = st.text_input(
        "Current Password",
        type="password",
        key="current_password"
    )

    new_password = st.text_input(
        "New Password",
        type="password",
        key="new_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )

    st.info(
        "Password should contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character."
    )

    if st.button(
        "🔑 Update Password",
        width="stretch",
        key="update_password"
    ):

        success, message = update_password(
            email=email,
            current_password=current_password,
            new_password=new_password,
            confirm_password=confirm_password,
        )

        if success:

            st.success(message)

            st.session_state.current_password = ""
            st.session_state.new_password = ""
            st.session_state.confirm_password = ""

        else:

            st.error(message)