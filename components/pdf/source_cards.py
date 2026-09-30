"""
=========================================
NovaMind AI - PDF Source Cards
=========================================

Displays retrieved source chunks
used by the AI to answer questions.
"""

import streamlit as st


def show_source_cards(sources):
    """
    Display retrieved PDF chunks.
    """

    if not sources:
        return

    st.divider()

    st.subheader("📚 AI Sources")

    st.caption(
        "These are the PDF sections used to generate the answer."
    )

    for index, source in enumerate(sources, start=1):

        # ------------------------------------
        # Extract Data
        # ------------------------------------

        if isinstance(source, dict):

            text = source.get("text", "")

            metadata = source.get(
                "metadata",
                {},
            )

            page = metadata.get(
                "page",
                "Unknown",
            )

            chunk = metadata.get(
                "chunk",
                index,
            )

        else:

            text = str(source)

            page = "Unknown"

            chunk = index

        # ------------------------------------
        # Source Card
        # ------------------------------------

        with st.expander(
            f"📄 Source {index} | Page {page} | Chunk {chunk}"
        ):

            st.markdown(text)

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.caption(
                    f"📄 Page : {page}"
                )

            with col2:

                st.caption(
                    f"🧩 Chunk : {chunk}"
                )