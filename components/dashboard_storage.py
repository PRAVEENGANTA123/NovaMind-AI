"""
=========================================
NovaMind AI - Dashboard Storage
=========================================

Displays live PDF storage statistics.
"""

import streamlit as st

from database.mongodb import pdf_collection


# =====================================
# Storage Settings
# =====================================

MAX_STORAGE_MB = 500


# =====================================
# Dashboard Storage
# =====================================

def show_dashboard_storage(email: str):
    """
    Display storage usage for the current user.
    """

    pdfs = list(

        pdf_collection.find(
            {
                "email": email
            }
        )

    )

    total_files = len(pdfs)

    total_bytes = sum(

        pdf.get(
            "filesize",
            0,
        )

        for pdf in pdfs

    )

    used_mb = round(
        total_bytes / (1024 * 1024),
        2,
    )

    remaining_mb = round(
        MAX_STORAGE_MB - used_mb,
        2,
    )

    percentage = min(

        (used_mb / MAX_STORAGE_MB) * 100,

        100,

    )

    average_size = round(

        used_mb / total_files,

        2,

    ) if total_files else 0

    # ---------------------------------
    # Header
    # ---------------------------------

    st.metric(

        "Storage Used",

        f"{percentage:.1f}%",

    )

    st.progress(

        percentage / 100,

        text=f"{used_mb:.2f} MB / {MAX_STORAGE_MB} MB",

    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "📄 PDFs",

            total_files,

        )

        st.metric(

            "💾 Used",

            f"{used_mb:.2f} MB",

        )

    with col2:

        st.metric(

            "📦 Remaining",

            f"{remaining_mb:.2f} MB",

        )

        st.metric(

            "📊 Avg Size",

            f"{average_size:.2f} MB",

        )

    st.caption(

        f"You are using {percentage:.1f}% of your available storage."

    )