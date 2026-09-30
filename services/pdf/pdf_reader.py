"""
=========================================
NovaMind AI - PDF Reader Service
=========================================

Reads both:
1. Normal text-based PDFs using PyPDF
2. Scanned/image-based PDFs using Tesseract OCR

Returns page-by-page text so the RAG pipeline
can preserve document page information.
"""

import io
import os

import pymupdf
import pytesseract

from PIL import Image
from pypdf import PdfReader


class PDFReaderService:
    """
    PDF Reader Service.

    Automatically chooses between normal PDF text
    extraction and OCR when the PDF is scanned.
    """

    # =====================================
    # Tesseract Configuration
    # =====================================

    TESSERACT_PATH = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    # =====================================
    # Extract Text
    # =====================================

    @staticmethod
    def extract_text(pdf_path: str) -> dict:
        """
        Extract text from a PDF.

        Normal PDF:
            Uses PyPDF.

        Scanned PDF:
            Falls back to Tesseract OCR.
        """

        try:

            # =================================
            # Check File
            # =================================

            if not pdf_path:

                return {
                    "success": False,
                    "text": "",
                    "pages": 0,
                    "page_texts": [],
                    "ocr_used": False,
                    "error": "PDF path is empty.",
                }

            if not os.path.exists(pdf_path):

                return {
                    "success": False,
                    "text": "",
                    "pages": 0,
                    "page_texts": [],
                    "ocr_used": False,
                    "error": (
                        f"PDF file not found: {pdf_path}"
                    ),
                }

            # =================================
            # Configure Tesseract
            # =================================

            if os.path.exists(
                PDFReaderService.TESSERACT_PATH
            ):

                pytesseract.pytesseract.tesseract_cmd = (
                    PDFReaderService.TESSERACT_PATH
                )

            # =================================
            # Open PDF with PyPDF
            # =================================

            reader = PdfReader(pdf_path)

            total_pages = len(reader.pages)

            page_texts = []

            normal_text_found = False

            # =================================
            # STEP 1
            # Normal PyPDF Extraction
            # =================================

            for page_number, page in enumerate(
                reader.pages,
                start=1,
            ):

                try:

                    page_text = (
                        page.extract_text()
                        or ""
                    )

                except Exception:

                    page_text = ""

                page_text = page_text.strip()

                page_texts.append(
                    {
                        "page": page_number,
                        "text": page_text,
                    }
                )

                if page_text:

                    normal_text_found = True

            # =================================
            # STEP 2
            # OCR Fallback
            # =================================

            if not normal_text_found:

                print("=" * 60)
                print("PDF TEXT NOT FOUND")
                print("Starting OCR...")
                print(f"Pages: {total_pages}")
                print("=" * 60)

                ocr_pages = []

                # ---------------------------------
                # Read PDF bytes
                # ---------------------------------

                with open(
                    pdf_path,
                    "rb",
                ) as pdf_file:

                    pdf_bytes = pdf_file.read()

                # ---------------------------------
                # Open PDF using modern PyMuPDF
                # ---------------------------------

                try:

                    document = pymupdf.open(
                        stream=pdf_bytes,
                        filetype="pdf",
                    )

                except Exception as e:

                    return {
                        "success": False,
                        "text": "",
                        "pages": total_pages,
                        "page_texts": [],
                        "ocr_used": False,
                        "error": (
                            "Scanned PDF detected, but "
                            "PyMuPDF could not open it. "
                            f"Error: {str(e)}"
                        ),
                    }

                # =================================
                # OCR Each Page
                # =================================

                for page_number, page in enumerate(
                    document,
                    start=1,
                ):

                    print(
                        f"OCR processing page "
                        f"{page_number}/{total_pages}..."
                    )

                    # ---------------------------------
                    # Render PDF page
                    # ---------------------------------

                    matrix = pymupdf.Matrix(
                        2.0,
                        2.0,
                    )

                    pixmap = page.get_pixmap(
                        matrix=matrix,
                        alpha=False,
                    )

                    image_bytes = pixmap.tobytes(
                        "png"
                    )

                    image = Image.open(
                        io.BytesIO(image_bytes)
                    )

                    # ---------------------------------
                    # OCR
                    # ---------------------------------

                    text = pytesseract.image_to_string(
                        image,
                        lang="eng",
                        config="--psm 6",
                    )

                    text = text.strip()

                    ocr_pages.append(
                        {
                            "page": page_number,
                            "text": text,
                        }
                    )

                document.close()

                page_texts = ocr_pages

                print("=" * 60)
                print("OCR COMPLETED")
                print("=" * 60)

            # =================================
            # Combine Page Text
            # =================================

            combined_parts = []

            for item in page_texts:

                page_number = item["page"]

                page_text = item["text"]

                if page_text:

                    combined_parts.append(
                        f"--- Page {page_number} ---\n"
                        f"{page_text}"
                    )

            combined_text = "\n\n".join(
                combined_parts
            )

            # =================================
            # Determine OCR Status
            # =================================

            ocr_used = not normal_text_found

            # =================================
            # Final Result
            # =================================

            return {
                "success": True,
                "text": combined_text,
                "pages": total_pages,
                "page_texts": page_texts,
                "ocr_used": ocr_used,
                "error": None,
            }

        except Exception as e:

            return {
                "success": False,
                "text": "",
                "pages": 0,
                "page_texts": [],
                "ocr_used": False,
                "error": str(e),
            }