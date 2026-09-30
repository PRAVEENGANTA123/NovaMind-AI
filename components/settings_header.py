"""
=========================================
NovaMind AI - Settings Header
=========================================
"""

import streamlit as st


def show_settings_header():

    username = st.session_state.get(
        "user",
        "User"
    )

    st.markdown(
        f"""
<div class="settings-header">

<div>

<h1>⚙️ Settings</h1>

<p>
Customize your NovaMind AI experience.
</p>

</div>

<div class="settings-user">

👤 {username}

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()