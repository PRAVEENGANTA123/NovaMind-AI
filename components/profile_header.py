import streamlit as st
from datetime import datetime


def show_profile_header(profile):

    username = profile.get("username", "User")

    occupation = profile.get(
        "occupation",
        "AI Enthusiast"
    )

    joined = profile.get("created_at")

    if joined:
        joined = joined.strftime("%d %B %Y")
    else:
        joined = "N/A"

    last_login = profile.get("last_login")

    if last_login:
        last_login = last_login.strftime("%I:%M %p")
    else:
        last_login = "First Login"

    left, right = st.columns([5, 1])

    with left:

        st.markdown(
            f"""
# 👋 Hello, {username}

### {occupation}

🕒 **Last Login:** {last_login}

📅 **Joined:** {joined}
"""
        )

    with right:

        st.success("🟢 Active")

    st.divider()