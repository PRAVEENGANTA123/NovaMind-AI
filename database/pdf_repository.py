"""
=========================================
NovaMind AI - PDF Repository
=========================================

Handles MongoDB operations for PDFs.
"""

from datetime import datetime
from bson import ObjectId

from database.mongodb import pdf_collection


class PDFRepository:

    # =====================================
    # Save PDF
    # =====================================

    @staticmethod
    def save_pdf(
        email: str,
        filename: str,
        filepath: str,
        filesize: int,
        pages: int = 0,
    ):
        """
        Save PDF metadata to MongoDB.
        """

        try:

            document = {

                "email": email,

                "filename": filename,

                "filepath": filepath,

                "filesize": filesize,

                "pages": pages,

                "status": "uploaded",

                "created_at": datetime.utcnow(),

            }

            print("=" * 60)
            print("SAVING PDF")
            print(document)

            result = pdf_collection.insert_one(document)

            print("INSERTED ID:", result.inserted_id)
            print("=" * 60)

            return str(result.inserted_id)

        except Exception as e:

            print("SAVE PDF ERROR:", e)

            return None

    # =====================================
    # Get User PDFs
    # =====================================

    @staticmethod
    def get_user_pdfs(email: str):
        """
        Return all PDFs uploaded by a user.
        """

        try:

            print("=" * 60)
            print("FETCHING PDFS")
            print("EMAIL:", email)

            pdfs = list(

                pdf_collection.find(
                    {
                        "email": email
                    }
                ).sort(
                    "created_at",
                    -1
                )

            )

            print("FOUND:", len(pdfs))
            print("=" * 60)

            return pdfs

        except Exception as e:

            print("GET PDF ERROR:", e)

            return []

    # =====================================
    # Get PDF By ID
    # =====================================

    @staticmethod
    def get_pdf(pdf_id: str):
        """
        Find one user's PDF by MongoDB ObjectId.

        Used by the AI orchestrator when a PDF
        has already been indexed and its PDF ID
        is available.
        """

        try:

            if not pdf_id:
                return None

            pdf = pdf_collection.find_one(
                {
                    "_id": ObjectId(pdf_id)
                }
            )

            return pdf

        except Exception as e:

            print(
                "GET PDF BY ID ERROR:",
                e,
            )

            return None


    # =====================================
    # Get PDF By Filename
    # =====================================

    @staticmethod
    def get_pdf_by_filename(
        email: str,
        filename: str,
    ):
        """
        Find a user's uploaded PDF by filename.

        Uses both email and filename so that
        one user's PDF cannot accidentally be
        selected for another user.
        """

        try:

            if not email:
                return None

            if not filename:
                return None

            pdf = pdf_collection.find_one(
                {
                    "email": email,
                    "filename": filename,
                },
                sort=[
                    ("created_at", -1)
                ],
            )

            return pdf

        except Exception as e:

            print(
                "GET PDF BY FILENAME ERROR:",
                e,
            )

            return None 
        
    # =====================================
    # Delete PDF
    # =====================================

    @staticmethod
    def delete_pdf(pdf_id: str):
        """
        Delete PDF metadata.
        """

        try:

            query = {"_id": ObjectId(pdf_id)}
            result = pdf_collection.delete_one(query)

            print("DELETE COUNT:", result.deleted_count)

            return result.deleted_count > 0

        except Exception as e:

            print("DELETE PDF ERROR:", e)

            return False

    # =====================================
    # Total PDFs
    # =====================================

    @staticmethod
    def total_pdfs(email: str):
        """
        Return total PDFs for a user.
        """

        try:

            total = pdf_collection.count_documents(
                {
                    "email": email
                }
            )

            print("TOTAL PDFS:", total)

            return total

        except Exception as e:

            print("TOTAL PDF ERROR:", e)

            return 0