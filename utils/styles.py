"""
=========================================
NovaMind AI - CSS Loader
=========================================

Loads global CSS and optional page CSS.
"""

from pathlib import Path

import streamlit as st


# =========================================
# CSS Directory
# =========================================

CSS_DIR = Path(__file__).parent.parent / "assets" / "css"


# =========================================
# Global CSS Files
# =========================================

GLOBAL_CSS = [

    "global.css",

    "sidebar.css",

    "navbar.css",

    "cards.css",

    "dashboard.css",

    "buttons.css",

    "animations.css",

    "responsive.css",

]


# =========================================
# Read CSS File
# =========================================

@st.cache_data(show_spinner=False)
def _read_css(filename: str) -> str:
    path = CSS_DIR / filename
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


# =========================================
# Load CSS
# =========================================

def load_css(page: str | None = None):
    """
    Load global CSS plus optional page CSS.
    """

    files = GLOBAL_CSS.copy()

    if page:

        if page not in files:

            files.append(page)

    css = ""

    for file in files:

        css += _read_css(file)
        css += "\n"

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )