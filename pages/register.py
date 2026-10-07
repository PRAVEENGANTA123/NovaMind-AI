"""
=========================================
NovaMind AI - Register Page
=========================================
"""
import time
from pathlib import Path
import streamlit as st
from authentication.register import register_user
from utils.styles import load_css
from utils.responsive import apply_responsive_layout

# ==========================================
# Page Configuration
# ==========================================

# MUST be the first Streamlit command
st.set_page_config(
    page_title="NovaMind AI | Register",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()
# ==========================================
# ==========================================



# ==========================================
# Hide Streamlit Navigation
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
# Logo & Hero
# ==========================================

logo = Path("assets/images/logo.png")

left, center, right = st.columns([2, 3, 2])

with center:

    if logo.exists():
        st.image(str(logo), width=95)

st.markdown("""
<div class="hero">

<h1>NovaMind AI</h1>

<p>

Create your account 🚀

<br>

Join NovaMind AI and start your intelligent AI workspace.

</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# Registration Form
# ==========================================

with st.form("register_form"):

    username = st.text_input(
        "Username",
        placeholder="Enter your username"
    )

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Confirm your password"
    )

    terms = st.checkbox(
        "I agree to the Terms of Service and Privacy Policy"
    )

    register_btn = st.form_submit_button(
        "Create Account →",
        use_container_width=True
    )

# ==========================================
# Registration Logic
# ==========================================

if register_btn:

    username = username.strip()
    email = email.strip().lower()

    if not username:

        st.warning("Please enter your username.")

    elif not email:

        st.warning("Please enter your email.")

    elif not password:

        st.warning("Please create a password.")

    elif len(password) < 8:

        st.warning(
            "Password must contain at least 8 characters."
        )

    elif password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    elif not terms:

        st.warning(
            "Please accept the Terms of Service."
        )

    else:

        with st.spinner("Creating your account..."):

            success, message = register_user(
                username=username,
                email=email,
                password=password,
                confirm_password=confirm_password
            )

        if success:

            # Save email for OTP verification
            st.session_state.pending_email = email

            st.success(message)

            time.sleep(1)

            st.switch_page("pages/otp_verification.py")

        else:

            st.error(message)

# ==========================================
# Footer
# ==========================================

st.markdown("---")

if st.button(
    "← Back to Sign In",
    use_container_width=True
):
    st.switch_page("pages/login.py")

st.caption(
    "Powered by Gemini AI • NovaMind AI v2.0 © 2026"
)