"""
=========================================
NovaMind AI - Chat Service
=========================================

Business logic layer for chat operations.
"""

import streamlit as st

from database.chat_repository import ChatRepository
from services.ai.orchestrator_service import AIOrchestrator


class ChatService:
    """
    Handles chat business logic.
    """

    @staticmethod
    def ask(user_email: str, prompt: str):
        """
        Process a user prompt using the AI Orchestrator,
        save the conversation, and return the result.
        """

        result = AIOrchestrator.process(prompt)

        ChatRepository.save_chat(
            email=user_email,
            prompt=prompt,
            response=result.answer,
            intent=result.intent,
            confidence=result.confidence,
            agent=result.agent,
        )

        return result

    @staticmethod
    def history(user_email: str):
        """
        Get all chats for a user.
        """

        return ChatRepository.get_user_chats(user_email)

    @staticmethod
    def get(chat_id):
        """
        Get one chat by ID.
        """

        return ChatRepository.get_chat(chat_id)

    @staticmethod
    def delete(chat_id):
        """
        Delete one chat.
        """

        ChatRepository.delete_chat(chat_id)

    @staticmethod
    def total():
        """
        Total chat count.
        """

        return ChatRepository.total_chats()

    @staticmethod
    def clear_session():
        """
        Clear Streamlit chat session.
        """

        st.session_state["messages"] = []