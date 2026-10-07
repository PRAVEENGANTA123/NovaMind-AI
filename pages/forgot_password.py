"""
=========================================
NovaMind AI - Forgot Password
=========================================
"""

import time
from pathlib import Path
import streamlit as st

from authentication.forgot_password import (
    send_password_reset_otp,
    verify_otp_and_reset_password,
)
from utils.styles import load_css
from utils.responsive import apply_responsive_layout


# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()
# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="NovaMind AI | Forgot Password",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)


def hide_sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebar"]{ display:none !important; }
    [data-testid="stSidebarNav"]{ display:none !important; }
    [data-testid="stSidebarNavSeparator"]{ display:none !important; }
    button[kind="header"]{ display:none !important; }
    </style>
    """, unsafe_allow_html=True)

hide_sidebar()
load_css("login.css")

logo = Path("assets/images/logo.png")
left, center, right = st.columns([2, 3, 2])
with center:
    if logo.exists():
        st.image(str(logo), width=90)

st.markdown("""
<div class="hero">
<h1>Reset Password</h1>
<p>Secure password recovery for your NovaMind AI account.</p>
</div>
""", unsafe_allow_html=True)

if "reset_email_sent" not in st.session_state:
    st.session_state.reset_email_sent = False
if "reset_email" not in st.session_state:
    st.session_state.reset_email = ""

# ==========================================
# Step 1: Request OTP Code
# ==========================================
if not st.session_state.reset_email_sent:
    with st.form("request_otp_form"):
        st.subheader("Step 1: Enter Your Registered Email")
        email_input = st.text_input(
            "Email Address",
            placeholder="name@example.com",
            value=st.session_state.reset_email
        )
        send_btn = st.form_submit_button("Send Verification Code â†’", use_container_width=True)

    if send_btn:
        email = email_input.strip().lower()
        if not email:
            st.warning("Please enter your registered email.")
        else:
            with st.spinner("Sending verification code..."):
                success, msg = send_password_reset_otp(email)
            if success:
                st.session_state.reset_email = email
                st.session_state.reset_email_sent = True
                st.success(msg)
                time.sleep(1)
                st.rerun()
            else:
                st.error(msg)

# ==========================================
# Step 2: Verify OTP & Create New Password
# ==========================================
else:
    st.info(f"Verification code sent to **{st.session_state.reset_email}**")

    with st.form("verify_and_reset_form"):
        st.subheader("Step 2: Enter Verification Code & New Password")
        otp_input = st.text_input(
            "6-Digit Verification Code",
            max_chars=6,
            placeholder="123456"
        )
        new_password = st.text_input(
            "New Password",
            type="password",
            placeholder="At least 8 characters"
        )
        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
            placeholder="Repeat new password"
        )
        submit_reset = st.form_submit_button("Reset Password â†’", use_container_width=True)

    if submit_reset:
        with st.spinner("Updating password securely..."):
            success, msg = verify_otp_and_reset_password(
                email=st.session_state.reset_email,
                otp=otp_input,
                password=new_password,
                confirm_password=confirm_password,
            )
        if success:
            st.success("âœ… Password updated successfully! Redirecting to Login...")
            st.session_state.reset_email_sent = False
            st.session_state.reset_email = ""
            time.sleep(1.5)
            st.switch_page("pages/login.py")
        else:
            st.error(msg)

    if st.button("â† Use a different email"):
        st.session_state.reset_email_sent = False
        st.rerun()

st.markdown("---")
if st.button("â† Back to Login", use_container_width=True):
    st.switch_page("pages/login.py")

st.caption("Powered by Gemini AI â€¢ NovaMind AI v2.0 Â© 2026")
