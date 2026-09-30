"""
=========================================
NovaMind AI - Text Splitter Service
=========================================

Splits extracted PDF text into
AI-friendly chunks.
"""

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


class TextSplitterService:
    """
    Text splitter for PDF documents.
    """

    DEFAULT_CHUNK_SIZE = 1000
    DEFAULT_CHUNK_OVERLAP = 200

    # =====================================
    # Split Text
    # =====================================

    @classmethod
    def split(
        cls,
        text: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ):
        """
        Split text into overlapping chunks.
        """

        if not text or not text.strip():

            return []

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                " ",
                "",
            ],
        )

        chunks = splitter.split_text(text)

        print("=" * 60)
        print("TEXT SPLITTER")
        print(f"Characters : {len(text)}")
        print(f"Chunks     : {len(chunks)}")
        print("=" * 60)

        return chunks

    # =====================================
    # Split Alias
    # =====================================

    @classmethod
    def split_text(
        cls,
        text: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ):
        """
        Backward-compatible alias.
        """

        return cls.split(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )