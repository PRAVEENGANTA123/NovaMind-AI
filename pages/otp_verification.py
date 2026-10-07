"""
=========================================
NovaMind AI - OTP Verification Page
=========================================
"""

import time
from pathlib import Path
import streamlit as st
from authentication.verify_otp import verify_otp
from authentication.otp_service import resend_email_otp
from utils.styles import load_css
from utils.responsive import apply_responsive_layout

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="NovaMind AI | Verify Email",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()


# ==========================================
# Page Configuration
# ==========================================

# MUST be the first Streamlit command



# ==========================================
# Hide Navigation
# ==========================================


def hide_sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebar"]{
        display:none !important;
    }

    [data-testid="stSidebarNav"]{
        display:none !important;
    }

    [data-testid="stSidebarNavSeparator"]{
        display:none !important;
    }

    button[kind="header"]{
        display:none !important;
    }
    </style>
    """, unsafe_allow_html=True)
hide_sidebar()

# ==========================================
# Load CSS
# ==========================================

load_css("register.css")

# ==========================================
# Check Session
# ==========================================

if "pending_email" not in st.session_state:

    st.warning("Your verification session has expired.")

    if st.button(
        "Back to Register",
        use_container_width=True
    ):
        st.switch_page("pages/register.py")

    st.stop()

email = st.session_state.pending_email

# ==========================================
# Logo
# ==========================================

logo = Path("assets/images/logo.png")

left, center, right = st.columns([2, 3, 2])

with center:

    if logo.exists():
        st.image(str(logo), width=95)

# ==========================================
# Hero
# ==========================================

st.markdown("""
<div class="hero">

<h1>Verify Email</h1>

<p>

We've sent a verification code to your email.

</p>

</div>
""", unsafe_allow_html=True)

st.info(f"Verification code sent to **{email}**")

# ==========================================
# OTP Form
# ==========================================

with st.form("otp_form"):

    otp = st.text_input(
        "Verification Code",
        placeholder="Enter 6-digit OTP",
        max_chars=6
    )

    verify_btn = st.form_submit_button(
        "Verify Email â†’",
        use_container_width=True
    )

# ==========================================
# Verify OTP
# ==========================================

if verify_btn:

    otp = otp.strip()

    if len(otp) != 6 or not otp.isdigit():

        st.error("Please enter a valid 6-digit OTP.")

    else:

        success, message = verify_otp(
            email=email,
            otp=otp
        )

        if success:

            st.success(message)

            st.balloons()

            st.session_state.pop("pending_email", None)

            time.sleep(2)

            st.switch_page("pages/login.py")

        else:

            st.error(message)

# ==========================================
# Footer Buttons
# ==========================================

st.markdown("---")

col1, col2 = st.columns(2)

# ==========================================
# Resend OTP
# ==========================================

with col1:

    if st.button(
        "ðŸ”„ Resend OTP",
        use_container_width=True
    ):

        with st.spinner("Sending new verification code..."):

            success, message = resend_email_otp(email)

        if success:

            st.success(message)

        else:

            st.error(message)

# ==========================================
# Back to Login
# ==========================================

with col2:

    if st.button(
        "â† Back to Login",
        use_container_width=True
    ):

        st.switch_page("pages/login.py")

# ==========================================
# Footer
# ==========================================

st.caption(
    "Powered by Gemini AI â€¢ NovaMind AI v2.0 Â© 2026"
)