"""
=========================================
NovaMind AI - PDF Embedding Pipeline
=========================================

Complete PDF indexing pipeline.

Flow:

PDF
 ↓
PDF Reader
 ↓
OCR if required
 ↓
Page Text
 ↓
Text Chunking
 ↓
Embeddings
 ↓
ChromaDB
"""

from services.pdf.pdf_reader import PDFReaderService
from services.pdf.pdf_chunker import TextSplitterService
from services.pdf.embedding_service import EmbeddingService
from services.pdf.vector_store import VectorStoreService


class PDFEmbeddingPipeline:
    """
    Complete PDF embedding pipeline.

    Responsibilities:
        1. Read PDF
        2. Use OCR when required
        3. Split page text into chunks
        4. Generate embeddings
        5. Store vectors in ChromaDB
    """

    # =====================================
    # Initialize
    # =====================================

    def __init__(self):

        self.vector_db = VectorStoreService()

    # =====================================
    # Process PDF
    # =====================================

    def process(
        self,
        pdf_id: str,
        filepath: str,
    ):
        """
        Process a PDF and store its embeddings.
        """

        try:

            print("=" * 60)
            print("PDF EMBEDDING PIPELINE STARTED")
            print("=" * 60)

            # =================================
            # Step 1 - Read PDF
            # =================================

            result = PDFReaderService.extract_text(
                filepath
            )

            if not result.get("success"):

                return {
                    "success": False,
                    "error": result.get(
                        "error",
                        "PDF reading failed.",
                    ),
                }

            pages = result.get(
                "pages",
                0,
            )

            page_texts = result.get(
                "page_texts",
                [],
            )

            ocr_used = result.get(
                "ocr_used",
                False,
            )

            print(
                f"Pages      : {pages}"
            )

            print(
                f"OCR Used   : {ocr_used}"
            )

            # =================================
            # Step 2 - Validate page text
            # =================================

            if not page_texts:

                return {
                    "success": False,
                    "error": (
                        "No readable text found "
                        "in the PDF."
                    ),
                }

            # =================================
            # Step 3 - Create page chunks
            # =================================

            all_chunks = []

            page_numbers = []

            for page_data in page_texts:

                page_number = page_data.get(
                    "page",
                    0,
                )

                page_text = page_data.get(
                    "text",
                    "",
                )

                if not page_text:
                    continue

                page_text = page_text.strip()

                if not page_text:
                    continue

                chunks = TextSplitterService.split(
                    page_text
                )

                for chunk in chunks:

                    if not chunk.strip():
                        continue

                    all_chunks.append(
                        chunk
                    )

                    page_numbers.append(
                        page_number
                    )

            if not all_chunks:

                return {
                    "success": False,
                    "error": (
                        "Failed to create "
                        "text chunks."
                    ),
                }

            print(
                f"Total Chunks : "
                f"{len(all_chunks)}"
            )

            # =================================
            # Step 4 - Create embeddings
            # =================================

            embeddings = (
                EmbeddingService.create_embeddings(
                    all_chunks
                )
            )

            print(
                f"Embeddings : "
                f"{len(embeddings)}"
            )

            # =================================
            # Step 5 - Store in ChromaDB
            # =================================

            store_result = (
            self.vector_db.add_pdf(
            pdf_id=pdf_id,
            chunks=all_chunks,
            embeddings=embeddings,
            pages=page_numbers,
            )
            )

            if not store_result:

                return {
                    "success": False,
                    "error": (
                        "Failed to store "
                        "PDF embeddings."
                    ),
                }

            # =================================
            # Completed
            # =================================

            print("=" * 60)
            print("PDF PIPELINE COMPLETED")
            print("=" * 60)

            return {
                "success": True,
                "pdf_id": str(pdf_id),
                "pages": pages,
                "chunks": len(all_chunks),
                "embeddings": len(embeddings),
                "ocr_used": ocr_used,
                "page_numbers": page_numbers,
            }

        except Exception as e:

            print("=" * 60)
            print("PDF PIPELINE ERROR")
            print("=" * 60)

            print(e)

            print("=" * 60)

            return {
                "success": False,
                "error": str(e),
            }