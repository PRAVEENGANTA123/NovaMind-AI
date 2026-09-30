"""
=========================================
NovaMind AI - Profile Avatar
=========================================
"""

from pathlib import Path
import streamlit as st

from services.profile_service import save_profile_image


def show_profile_avatar(profile, email):

    st.markdown("### 📷 Profile Picture")

    default_avatar = "assets/images/avatar.png"

    image_path = profile.get("profile_image")

    try:

        if (
            image_path
            and Path(image_path).exists()
        ):

            st.image(
                image_path,
                width=220,
            )

        else:

            st.image(
                default_avatar,
                width=220,
            )

    except Exception:

        st.image(
            default_avatar,
            width=220,
        )

    st.markdown("")

    uploaded = st.file_uploader(
        "Choose Profile Picture",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
        key="profile_upload",
    )

    if uploaded:

        success, message = save_profile_image(
            email,
            uploaded
        )

        if success:

            st.success("✅ Profile picture updated.")

            st.rerun()

        else:

            st.error(message)

    st.markdown("---")

    st.metric(
        "Account Status",
        "Active ✅"
    )

    verified = profile.get(
        "email_verified",
        False
    )

    st.metric(
        "Email",
        "Verified" if verified else "Not Verified"
    )

    st.metric(
        "Role",
        profile.get(
            "role",
            "User"
        ).title()
    )