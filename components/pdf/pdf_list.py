"""
=========================================
NovaMind AI - PDF List
=========================================

Displays all uploaded PDFs for
the current user.
"""

import streamlit as st

from components.pdf.pdf_card import show_pdf_card
from services.pdf.pdf_service import PDFService


def show_pdf_list(email: str):
    """
    Display all PDFs uploaded by the user.
    """

    st.subheader("📚 My PDF Library")

    # =====================================
    # Load PDFs
    # =====================================

    try:

        pdfs = PDFService.get_user_pdfs(email)

    except Exception as e:

        st.error(f"❌ Failed to load PDF library.\n\n{e}")

        return

    # =====================================
    # Empty State
    # =====================================

    if not pdfs:

        st.info("📂 No PDFs uploaded yet.")

        st.markdown(
            """
### Upload your first PDF

After uploading a PDF you can:

- 💬 Chat with your PDF
- 📝 Generate summaries
- 🔍 Search information instantly
- 🧠 Ask AI questions
- 📚 Build your personal knowledge base
            """
        )

        return

    # =====================================
    # Toolbar
    # =====================================

    col1, col2 = st.columns([4, 1])

    with col1:

        search = st.text_input(
            "🔍 Search PDFs",
            placeholder="Search by filename...",
        )

    with col2:

        st.metric(
            "Total PDFs",
            len(pdfs),
        )

    # =====================================
    # Filter PDFs
    # =====================================

    if search:

        pdfs = [

            pdf

            for pdf in pdfs

            if search.lower()

            in pdf.get(
                "filename",
                "",
            ).lower()

        ]

    # =====================================
    # No Results
    # =====================================

    if not pdfs:

        st.warning("No matching PDFs found.")

        return

    # =====================================
    # Sort PDFs
    # =====================================

    pdfs = sorted(

        pdfs,

        key=lambda pdf: pdf.get(
            "filename",
            "",
        ).lower(),

    )

    st.divider()

    # =====================================
    # Display PDF Cards
    # =====================================

    for pdf in pdfs:

        show_pdf_card(pdf)

    st.divider()

    # =====================================
    # Footer
    # =====================================

    st.caption(
        f"Showing {len(pdfs)} PDF(s)"
    )