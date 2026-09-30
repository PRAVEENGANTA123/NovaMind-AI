"""
=========================================
NovaMind AI - Profile Form
=========================================
"""

import streamlit as st

from services.profile_service import save_profile


def show_profile_form(profile, email):

    st.markdown("### 👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:

        username = st.text_input(
            "👤 Full Name",
            value=profile.get("username", "")
        )

        phone = st.text_input(
            "📱 Mobile Number",
            value=profile.get("phone", "")
        )

        country = st.text_input(
            "🌍 Country",
            value=profile.get("country", "")
        )

    with col2:

        occupation = st.text_input(
            "🎓 Occupation",
            value=profile.get("occupation", "")
        )

        languages = [
            "English",
            "Hindi",
            "Telugu",
            "Tamil",
        ]

        current_language = profile.get(
            "language",
            "English"
        )

        if current_language not in languages:
            current_language = "English"

        language = st.selectbox(
            "🗣 Preferred Language",
            languages,
            index=languages.index(current_language)
        )

        st.text_input(
            "📧 Email",
            value=email,
            disabled=True
        )

    bio = st.text_area(
        "📝 Bio",
        value=profile.get("bio", ""),
        height=120,
        placeholder="Tell us something about yourself..."
    )

    verified = profile.get(
        "email_verified",
        False
    )

    if verified:
        st.success("✅ Email Verified")
    else:
        st.warning("⚠ Email Not Verified")

    st.markdown("")

    if st.button(
        "💾 Save Changes",
        width="stretch",
        key="save_profile"
    ):

        success, message = save_profile(
            email=email,
            username=username,
            phone=phone,
            occupation=occupation,
            country=country,
            language=language,
            bio=bio,
        )

        if success:

            st.session_state.user = username

            st.success(message)

            st.rerun()

        else:

            st.error(message)