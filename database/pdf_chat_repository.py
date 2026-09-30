"""
=========================================
NovaMind AI - PDF Chat Repository
=========================================

Handles MongoDB operations for
PDF chat conversations.
"""

from datetime import datetime

from bson import ObjectId

from database.mongodb import pdf_chat_collection


class PDFChatRepository:
    """
    MongoDB repository for PDF chat history.
    """

    # =====================================
    # Save Chat
    # =====================================

    @staticmethod
    def save_chat(
        email: str,
        pdf_id: str,
        question: str,
        answer: str,
    ):
        """
        Save one PDF conversation.
        """

        document = {

            "email": email,

            "pdf_id": ObjectId(pdf_id),

            "question": question,

            "answer": answer,

            "created_at": datetime.utcnow(),

        }

        result = pdf_chat_collection.insert_one(
            document
        )

        return str(result.inserted_id)

    # =====================================
    # Get PDF Chats
    # =====================================

    @staticmethod
    def get_pdf_chats(
        email: str,
        pdf_id: str,
    ):
        """
        Return all conversations for one PDF.
        """

        return list(

            pdf_chat_collection.find(
                {
                    "email": email,
                    "pdf_id": ObjectId(pdf_id),
                }
            ).sort(
                "created_at",
                1,
            )

        )

    # =====================================
    # Get One Chat
    # =====================================

    @staticmethod
    def get_chat(chat_id: str):
        """
        Return one PDF chat.
        """

        return pdf_chat_collection.find_one(
            {
                "_id": ObjectId(chat_id)
            }
        )

    # =====================================
    # Delete One Chat
    # =====================================

    @staticmethod
    def delete_chat(chat_id: str):
        """
        Delete one PDF chat.
        """

        return pdf_chat_collection.delete_one(
            {
                "_id": ObjectId(chat_id)
            }
        )

    # =====================================
    # Delete All Chats of PDF
    # =====================================

    @staticmethod
    def delete_pdf_chats(
        pdf_id: str,
    ):
        """
        Delete all conversations
        belonging to one PDF.
        """

        return pdf_chat_collection.delete_many(
            {
                "pdf_id": ObjectId(pdf_id)
            }
        )

    # =====================================
    # Total Chats
    # =====================================

    @staticmethod
    def total_chats(
        email: str,
    ):
        """
        Return total PDF chats
        for one user.
        """

        return pdf_chat_collection.count_documents(
            {
                "email": email
            }
        )