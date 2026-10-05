"""
=========================================
NovaMind AI - Text Splitter Service
=========================================

Splits extracted PDF text into
AI-friendly chunks.
"""

# ==========================================
# Resilient Splitter Import
# ==========================================

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore[import-not-found]
    except ImportError:
        RecursiveCharacterTextSplitter = None


class _FallbackTextSplitter:
    """Internal pure-Python text splitter fallback if LangChain is absent."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, separators=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", "? ", "! ", " ", ""]

    def split_text(self, text: str) -> list[str]:
        if not text:
            return []
        chunks = []
        start = 0
        text_len = len(text)
        step = max(1, self.chunk_size - self.chunk_overlap)

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end >= text_len:
                break
            start += step
        return chunks


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

        if RecursiveCharacterTextSplitter is not None:
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
        else:
            splitter = _FallbackTextSplitter(
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