from services.pdf.vector_store import VectorStoreService
"""
=========================================
NovaMind AI - PDF Service
=========================================

Handles PDF upload, storage,
and AI indexing.
"""

import os
import uuid

from database.pdf_repository import PDFRepository
from services.pdf.pdf_reader import PDFReaderService
from services.pdf.pdf_embedding_pipeline import PDFEmbeddingPipeline


class PDFService:

    UPLOAD_FOLDER = "uploads/pdfs"

    # =====================================
    # Save PDF
    # =====================================

    @classmethod
    def save_pdf(
        cls,
        email,
        uploaded_file,
    ):
        """
        Save uploaded PDF and index it
        for AI chat.
        """

        try:

            print("=" * 60)
            print("PDF SERVICE STARTED")
            print("=" * 60)

            print("Email :", email)
            print("File  :", uploaded_file.name)

            # ---------------------------------
            # Upload Folder
            # ---------------------------------

            os.makedirs(
                cls.UPLOAD_FOLDER,
                exist_ok=True,
            )

            original_name = uploaded_file.name

            unique_name = (
                f"{uuid.uuid4().hex}_{original_name}"
            )

            filepath = os.path.join(
                cls.UPLOAD_FOLDER,
                unique_name,
            )

            # ---------------------------------
            # Save File
            # ---------------------------------

            with open(filepath, "wb") as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            filesize = os.path.getsize(filepath)

            print("Saved :", filepath)

            # ---------------------------------
            # Read PDF
            # ---------------------------------

            read_result = PDFReaderService.extract_text(
                filepath
            )

            if not read_result["success"]:

                os.remove(filepath)

                return {
                    "success": False,
                    "error": read_result["error"],
                }

            pages = read_result["pages"]

            # ---------------------------------
            # Save Metadata
            # ---------------------------------

            pdf_id = PDFRepository.save_pdf(

                email=email,

                filename=original_name,

                filepath=filepath,

                filesize=filesize,

                pages=pages,

            )

            print("MongoDB Saved :", pdf_id)

            # ---------------------------------
            # Create Embeddings
            # ---------------------------------

            pipeline = PDFEmbeddingPipeline()

            pipeline_result = pipeline.process(

                pdf_id=pdf_id,

                filepath=filepath,

            )

            if not pipeline_result["success"]:

                PDFRepository.delete_pdf(pdf_id)

                if os.path.exists(filepath):

                    os.remove(filepath)

                return pipeline_result

            print("=" * 60)
            print("PDF READY FOR AI CHAT")
            print("=" * 60)

            return {

                "success": True,

                "pdf_id": pdf_id,

                "filename": original_name,

                "filepath": filepath,

                "pages": pages,

                "chunks": pipeline_result["chunks"],

                "embeddings": pipeline_result["embeddings"],

            }

        except Exception as e:

            print("=" * 60)
            print("PDF SERVICE ERROR")
            print("=" * 60)
            print(e)
            print("=" * 60)

            return {

                "success": False,

                "error": str(e),

            }

    # =====================================
    # Get User PDFs
    # =====================================

    @staticmethod
    def get_user_pdfs(email):

        return PDFRepository.get_user_pdfs(email)

    # =====================================
    # Get One PDF
    # =====================================

    @staticmethod
    def get_pdf(pdf_id):

        return PDFRepository.get_pdf(pdf_id)
        # =====================================
    # Get PDF By Filename
    # =====================================

    @staticmethod
    def get_pdf_by_filename(
        email,
        filename,
    ):
        """
        Find a user's PDF using its filename.
        """

        return PDFRepository.get_pdf_by_filename(
            email=email,
            filename=filename,
        )

    # =====================================
    # Delete PDF
    # =====================================

    @staticmethod
    def delete_pdf(pdf_id):
        """
        Delete PDF from disk,
        MongoDB and ChromaDB.
        """

        pdf = PDFRepository.get_pdf(pdf_id)

        if pdf:

            filepath = pdf.get("filepath")

            if filepath and os.path.exists(filepath):

                os.remove(filepath)

        PDFRepository.delete_pdf(pdf_id)

        # Future:
        try:
            VectorStoreService().delete_pdf(pdf_id)
        except Exception:
            pass

        return True

    # =====================================
    # Total PDFs
    # =====================================

    @staticmethod
    def total_pdfs(email):

        return PDFRepository.total_pdfs(email)