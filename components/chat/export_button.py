"""
=========================================
NovaMind AI - Export Button
=========================================

UI for exporting chat conversations.
"""

import os
import streamlit as st

from services.chat.export_service import ChatExportService


# =========================================
# Export Button
# =========================================

def show_export_button():
    """
    Display chat export options.
    """

    messages = st.session_state.get("messages", [])

    if not messages:
        return

    with st.expander(
        "📤 Export Chat",
        expanded=False,
    ):

        export_type = st.selectbox(
            "Choose Export Format",
            (
                "PDF",
                "Markdown",
                "Text",
                "JSON",
            ),
            key="chat_export_type",
        )

        if "last_export_file" not in st.session_state:
            st.session_state.last_export_file = None
            st.session_state.last_export_mime = "text/plain"
            st.session_state.last_export_type = ""

        if st.button(
            "Generate Export",
            key="generate_export",
            type="primary",
            use_container_width=True,
        ):
            try:
                with st.spinner("Generating export..."):
                    if export_type == "PDF":
                        file_path = ChatExportService.export_pdf(messages)
                        mime = "application/pdf"
                    elif export_type == "Markdown":
                        file_path = ChatExportService.export_markdown(messages)
                        mime = "text/markdown"
                    elif export_type == "JSON":
                        file_path = ChatExportService.export_json(messages)
                        mime = "application/json"
                    else:
                        file_path = ChatExportService.export_txt(messages)
                        mime = "text/plain"

                if file_path and os.path.exists(file_path):
                    st.session_state.last_export_file = file_path
                    st.session_state.last_export_mime = mime
                    st.session_state.last_export_type = export_type
                    st.success(f"✅ {export_type} export generated successfully.")
                else:
                    st.error("Export file was not created.")
            except Exception as e:
                st.error(f"Export failed:\n\n{e}")

        # Keep download button visible across reruns if file exists
        if (
            st.session_state.last_export_file
            and os.path.exists(st.session_state.last_export_file)
        ):
            with open(st.session_state.last_export_file, "rb") as f:
                st.download_button(
                    label=f"⬇ Download {st.session_state.last_export_type}",
                    data=f.read(),
                    file_name=os.path.basename(st.session_state.last_export_file),
                    mime=st.session_state.last_export_mime,
                    use_container_width=True,
                    key="export_download_btn",
                )