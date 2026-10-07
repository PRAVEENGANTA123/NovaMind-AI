"""
=========================================
NovaMind AI - Verify Email Page
=========================================
"""

from pathlib import Path
import streamlit as st

from authentication import verify_email
from authentication.verify_email import verify_email_token
from utils.styles import load_css


# ==========================================
# Load CSS
# ==========================================

load_css("login.css")

import streamlit as st

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
# Logo
# ==========================================

logo = Path("assets/images/logo.png")

col1, col2, col3 = st.columns([2, 3, 2])

with col2:
    if logo.exists():
        st.image(str(logo), width=90)

# ==========================================
# Header
# ==========================================

st.markdown("""
<div class="hero">

<h1>Email Verification</h1>

<p>
Verifying your NovaMind AI account...
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# Read Token
# ==========================================

token = st.query_params.get("token")

# ==========================================
# Verify Email
# ==========================================

if token:

    success, message = verify_email_token(token)

    if success:

        st.success("âœ… " + message)

        st.balloons()

        st.info(
            "Your account is now active. Click below to sign in."
        )

    else:

        st.error("âŒ " + message)

else:

    st.warning(
        "Verification token not found."
    )

# ==========================================
# Back To Login
# ==========================================

st.divider()

if st.button(
    "â† Go to Login",
    use_container_width=True
):
    st.switch_page("pages/login.py")

# ==========================================
# Footer
# ==========================================

st.caption(
    "Powered by Gemini AI â€¢ NovaMind AI v2.0 Â© 2026"
)