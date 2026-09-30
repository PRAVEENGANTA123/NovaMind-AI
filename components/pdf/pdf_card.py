"""
=========================================
NovaMind AI - PDF Card
=========================================
"""

import streamlit as st

from services.pdf.pdf_service import PDFService


def show_pdf_card(pdf):
    """
    Display one PDF card.
    """

    with st.container(border=True):

        col1, col2 = st.columns([8, 2])

        with col1:

            st.subheader(f"📄 {pdf['filename']}")

            st.write(f"📑 Pages : {pdf.get('pages', 0)}")

            st.write(
                f"💾 Size : {round(pdf['filesize']/1024,2)} KB"
            )

            st.write(
                f"🕒 Uploaded : {pdf['created_at']}"
            )

        with col2:

            if st.button(
                "🗑 Delete",
                key=f"delete_{pdf['_id']}",
                width="stretch",
            ):

                PDFService.delete_pdf(
                    str(pdf["_id"])
                )

                st.success("PDF Deleted")

                st.rerun()

        st.divider()

        if st.button(
            "💬 Chat with PDF",
            key=f"chat_{pdf['_id']}",
            width="stretch",
            type="primary",
        ):

            st.session_state["selected_pdf"] = str(
                pdf["_id"]
            )

            st.session_state["pdf_filename"] = (
                pdf["filename"]
            )

            st.session_state["pdf_messages"] = []

            st.switch_page(
                "pages/pdf_chat.py"
            )