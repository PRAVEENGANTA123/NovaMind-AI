"""
=========================================
NovaMind AI - Login Page
=========================================
"""

import time
from pathlib import Path
import streamlit as st
from authentication.login import login_user
from utils.styles import load_css
from utils.responsive import apply_responsive_layout
# ==========================================
# Page Configuration
# ==========================================
# MUST be the first Streamlit command
st.set_page_config(
    page_title="NovaMind AI | Login",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)
def apply_responsive_theme():
    """Inject universal responsive styling for all viewports (mobile, tablet, desktop)."""
    st.markdown("""
        
    """, unsafe_allow_html=True)


# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()

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

load_css("login.css")

# ==========================================
# Logo
# ==========================================

logo = Path("assets/images/logo.png")

col1, col2 = st.columns([1, 5])

with col1:
    if logo.exists():
        st.image(str(logo), width=70)

with col2:
    st.markdown("""
    <h1 style="margin-bottom:0;">
        NovaMind AI
    </h1>

    <p style="
        color:#64748B;
        font-size:18px;
        margin-top:8px;
    ">
        Welcome back 👋<br>
        Sign in to access your AI Workspace.
    </p>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# Login Form
# ==========================================

with st.form("login_form"):

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    remember = st.checkbox("Keep me signed in")

    login_btn = st.form_submit_button(
        "Sign In →",
        use_container_width=True
    )

# ==========================================
# Login Logic
# ==========================================

if login_btn:

    email = email.strip().lower()
    password = password.strip()

    if not email:
        st.warning("Please enter your email.")

    elif not password:
        st.warning("Please enter your password.")

    else:

        print("=" * 60)
        print("LOGIN EMAIL :", repr(email))

        success, result = login_user(
            email=email,
            password=password
        )

        print("SUCCESS :", success)
        print("RESULT  :", result)
        print("=" * 60)

        if success:

            st.session_state.logged_in = True
            st.session_state.user = result["username"]
            st.session_state.email = result["email"]
            st.session_state.remember = remember

            if "_id" in result:
                st.session_state.user_id = str(result["_id"])

            st.success(
                f"Welcome back, {result['username']}!"
            )

            time.sleep(1)

            st.rerun()

        else:

            st.error(result)

# ==========================================
# Footer
# ==========================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🔑 Forgot Password",
        use_container_width=True
    ):
        st.switch_page("pages/forgot_password.py")

with col2:

    if st.button(
        "📝 Create Account",
        use_container_width=True
    ):
        st.switch_page("pages/register.py")

st.markdown("<br>", unsafe_allow_html=True)

st.caption(
    "Powered by Gemini AI • NovaMind AI v2.0 © 2026"
)
