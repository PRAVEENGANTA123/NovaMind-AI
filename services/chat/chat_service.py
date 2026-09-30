"""
=========================================
NovaMind AI - Chat Service
=========================================

Business logic for AI chat conversations.
"""

from database.chat_repository import ChatRepository


class ChatService:
    """
    Business logic layer for AI chat.
    """

    # =====================================
    # Save Chat
    # =====================================

    @staticmethod
    def save(
        result,
        email: str,
        prompt: str,
    ):
        """
        Save AI conversation.
        """

        try:

            return ChatRepository.save_chat(

                email=email,

                prompt=prompt,

                response=result.answer,

                intent=result.intent,

                confidence=result.confidence,

                agent=getattr(
                    result,
                    "agent",
                    result.intent,
                ),

            )

        except Exception as e:

            print("=" * 60)
            print("CHAT SAVE ERROR")
            print(e)
            print("=" * 60)

            return None

    # =====================================
    # Chat History
    # =====================================

    @staticmethod
    def history(
        email: str,
    ):
        """
        Return all chats.
        """

        try:

            return ChatRepository.get_user_chats(
                email
            )

        except Exception as e:

            print("=" * 60)
            print("CHAT HISTORY ERROR")
            print(e)
            print("=" * 60)

            return []

    # =====================================
    # Get One Chat
    # =====================================

    @staticmethod
    def get(
        chat_id: str,
    ):

        return ChatRepository.get_chat(
            chat_id
        )

    # =====================================
    # Like Chat
    # =====================================

    @staticmethod
    def like_chat(
        chat_id: str,
    ):
        """
        Like one chat.
        """

        return ChatRepository.like_chat(
            chat_id
        )

    # =====================================
    # Dislike Chat
    # =====================================

    @staticmethod
    def dislike_chat(
        chat_id: str,
    ):
        """
        Dislike one chat.
        """

        return ChatRepository.dislike_chat(
            chat_id
        )

    # =====================================
    # Bookmark Chat
    # =====================================

    @staticmethod
    def bookmark_chat(
        chat_id: str,
    ):
        """
        Bookmark one chat.
        """

        return ChatRepository.bookmark_chat(
            chat_id
        )

    # =====================================
    # Remove Bookmark
    # =====================================

    @staticmethod
    def remove_bookmark(
        chat_id: str,
    ):
        """
        Remove bookmark.
        """

        return ChatRepository.remove_bookmark(
            chat_id
        )

    # =====================================
    # Bookmarked Chats
    # =====================================

    @staticmethod
    def bookmarked(
        email: str,
    ):
        """
        Return bookmarked chats.
        """

        return ChatRepository.get_bookmarked_chats(
            email
        )

    # =====================================
    # Delete Chat
    # =====================================

    @staticmethod
    def delete(
        chat_id: str,
    ):

        return ChatRepository.delete_chat(
            chat_id
        )

    # =====================================
    # Delete All Chats
    # =====================================

    @staticmethod
    def delete_all(
        email: str,
    ):

        return ChatRepository.delete_user_chats(
            email
        )

    # =====================================
    # Total Chats
    # =====================================

    @staticmethod
    def total(
        email: str,
    ):

        return ChatRepository.total_chats(
            email
        )

    # =====================================
    # Total Bookmarks
    # =====================================

    @staticmethod
    def total_bookmarks(
        email: str,
    ):

        return ChatRepository.total_bookmarks(
            email
        )