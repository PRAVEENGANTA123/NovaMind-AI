"""
=========================================
NovaMind AI - AI Status Bar
=========================================
"""

import streamlit as st


def show_status_bar():

    # -------------------------------------
    # Defaults
    # -------------------------------------

    defaults = {

        "connection": "🟢 Online",

        "agent": "🤖 General AI",

        "auto_reasoning": True,

        "web_search": False,

        "code_mode": False,

        "fast_mode": False,

        "uploaded_file": None,

    }

    for key, value in defaults.items():

        st.session_state.setdefault(key, value)

    # -------------------------------------
    # Status Chips
    # -------------------------------------

    chips = []

    chips.append(st.session_state.connection)

    chips.append(st.session_state.agent)

    if st.session_state.auto_reasoning:

        chips.append("🧠 Auto AI")

    if st.session_state.web_search:

        chips.append("🌐 Web")

    if st.session_state.code_mode:

        chips.append("💻 Code")

    if st.session_state.fast_mode:

        chips.append("⚡ Fast")

    if st.session_state.uploaded_file:

        chips.append(
            f"📎 {st.session_state.uploaded_file}"
        )

    st.info("   |   ".join(chips))