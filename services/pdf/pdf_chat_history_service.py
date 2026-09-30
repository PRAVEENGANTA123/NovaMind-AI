"""
=========================================
NovaMind AI - PDF Chat History
=========================================
"""

from database.pdf_chat_repository import PDFChatRepository


class PDFChatHistoryService:

    @staticmethod
    def save(
        email,
        pdf_id,
        question,
        answer,
    ):

        return PDFChatRepository.save_chat(
            email=email,
            pdf_id=pdf_id,
            question=question,
            answer=answer,
        )

    @staticmethod
    def load(
        email,
        pdf_id,
    ):

        return PDFChatRepository.get_pdf_chats(
            email=email,
            pdf_id=pdf_id,
        )