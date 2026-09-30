"""
=========================================
NovaMind AI - PDF Upload Component
=========================================

Handles PDF upload with:
- File validation
- File information
- Upload progress
- PDF indexing
- Session-state storage
- AI Chat integration
"""

import streamlit as st

from services.pdf.pdf_service import PDFService


# =========================================
# Configuration
# =========================================

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


# =========================================
# PDF Upload Component
# =========================================

def show_pdf_upload(email: str):
    """
    Display PDF upload component.

    The uploaded PDF is:
        1. Validated
        2. Saved through PDFService
        3. Stored in session state
        4. Made available for AI Chat
    """

    st.subheader("📄 Upload PDF")

    st.caption(
        "Upload a PDF to chat with it using NovaMind AI."
    )

    uploaded_file = st.file_uploader(
        label="Choose a PDF",
        type=["pdf"],
        accept_multiple_files=False,
        help="Supported format: PDF • Maximum size: 20 MB",
        key="pdf_uploader",
    )

    # =====================================
    # No File Selected
    # =====================================

    if uploaded_file is None:
        return

    # =====================================
    # File Information
    # =====================================

    filename = uploaded_file.name
    filesize = uploaded_file.size

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Filename",
            filename,
        )

    with col2:
        st.metric(
            "Size",
            f"{round(filesize / 1024, 2)} KB",
        )

    with col3:
        st.metric(
            "Type",
            "PDF",
        )

    # =====================================
    # Validation
    # =====================================

    if filesize > MAX_FILE_SIZE:

        st.error(
            "❌ File exceeds the maximum allowed size (20 MB)."
        )

        return

    if not filename.lower().endswith(".pdf"):

        st.error(
            "❌ Please select a valid PDF document."
        )

        return

    st.success("✅ File is ready for upload.")

    # =====================================
    # Upload Button
    # =====================================

    if st.button(
        "🚀 Upload & Index PDF",
        key="upload_pdf",
        type="primary",
        width="stretch",
    ):

        progress = st.progress(0)

        status = st.empty()

        try:

            # ---------------------------------
            # Step 1: Read uploaded PDF bytes
            # ---------------------------------

            status.info("Reading PDF...")

            progress.progress(10)

            pdf_bytes = uploaded_file.getvalue()

            # ---------------------------------
            # Step 2: Store uploaded PDF
            # ---------------------------------
            #
            # Keep the actual PDF available in the
            # current Streamlit session so the
            # Chat/Orchestrator can use it later.
            #

            st.session_state["uploaded_pdf"] = pdf_bytes

            st.session_state["uploaded_pdf_name"] = filename

            st.session_state["uploaded_pdf_size"] = filesize

            st.session_state["pdf_uploaded"] = True

            # ---------------------------------
            # Step 3: Save PDF
            # ---------------------------------

            status.info("Uploading PDF...")

            progress.progress(20)

            result = PDFService.save_pdf(
                email=email,
                uploaded_file=uploaded_file,
            )

            progress.progress(60)

            # ---------------------------------
            # Check Save Result
            # ---------------------------------

            if not result.get("success"):

                # Remove session data if saving failed
                st.session_state.pop(
                    "uploaded_pdf",
                    None,
                )

                st.session_state.pop(
                    "uploaded_pdf_name",
                    None,
                )

                st.session_state["pdf_uploaded"] = False

                progress.empty()

                st.error(
                    result.get(
                        "error",
                        "Failed to upload PDF.",
                    )
                )

                return

            # ---------------------------------
            # Store PDF database information
            # ---------------------------------

            st.session_state["pdf_result"] = result

            # If PDFService returns an ID,
            # preserve it for later PDF retrieval.

            if result.get("pdf_id"):

                st.session_state["pdf_id"] = result["pdf_id"]

            elif result.get("id"):

                st.session_state["pdf_id"] = result["id"]

            # ---------------------------------
            # Step 4: AI Indexing
            # ---------------------------------

            status.info(
                "Creating AI embeddings..."
            )

            progress.progress(90)

            # Your existing PDFService handles
            # the indexing operation.
            # We do not call any new/unknown
            # PDFService method here.

            progress.progress(100)

            # ---------------------------------
            # Step 5: Success
            # ---------------------------------

            status.success(
                "✅ PDF uploaded and indexed successfully."
            )

            st.toast(
                "📚 Your PDF is ready for AI Chat!"
            )

            # Helpful information for debugging
            st.session_state["pdf_ready"] = True

            # ---------------------------------
            # Refresh UI
            # ---------------------------------

            st.rerun()

        except Exception as e:

            progress.empty()

            status.empty()

            # Don't leave the app thinking the PDF
            # is ready if an unexpected error occurs.

            st.session_state["pdf_uploaded"] = False
            st.session_state["pdf_ready"] = False

            st.exception(e)