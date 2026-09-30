"""
=========================================
NovaMind AI - Dashboard Service
=========================================

Provides live dashboard statistics
for the logged-in user.
"""

from database.mongodb import (
    chats_collection,
    pdf_collection,
    pdf_chat_collection,
    users_collection,
)


class DashboardService:

    # =====================================
    # Dashboard Stats
    # =====================================

    @staticmethod
    def get_dashboard_stats(email: str):

        try:

            user = users_collection.find_one(
                {
                    "email": email
                }
            )

            if not user:

                return {

                    "username": "User",

                    "total_chats": 0,

                    "total_pdfs": 0,

                    "bookmarks": 0,

                    "messages": 0,

                    "storage_used": 0,

                    "recent_chats": [],

                    "last_login": None,

                }

            # ---------------------------------
            # Live Counts
            # ---------------------------------

            total_chats = chats_collection.count_documents(
                {
                    "email": email
                }
            )

            total_pdfs = pdf_collection.count_documents(
                {
                    "email": email
                }
            )

            total_pdf_messages = pdf_chat_collection.count_documents(
                {
                    "email": email
                }
            )

            bookmarks = len(
                user.get(
                    "bookmarks",
                    [],
                )
            )

            # ---------------------------------
            # Storage Used
            # ---------------------------------

            storage_used = 0

            pdfs = pdf_collection.find(
                {
                    "email": email
                }
            )

            for pdf in pdfs:

                storage_used += pdf.get(
                    "filesize",
                    0,
                )

            # ---------------------------------
            # Recent Chats
            # ---------------------------------

            recent_chats = list(

                chats_collection.find(
                    {
                        "email": email
                    }
                ).sort(
                    "created_at",
                    -1,
                ).limit(5)

            )

            return {

                "username": user.get(
                    "username",
                    "User",
                ),

                "total_chats": total_chats,

                "total_pdfs": total_pdfs,

                "bookmarks": bookmarks,

                "messages": total_chats + total_pdf_messages,

                "storage_used": storage_used,

                "recent_chats": recent_chats,

                "last_login": user.get(
                    "last_login"
                ),

            }

        except Exception as e:

            print("=" * 60)
            print("DASHBOARD ERROR")
            print(e)
            print("=" * 60)

            return {

                "username": "User",

                "total_chats": 0,

                "total_pdfs": 0,

                "bookmarks": 0,

                "messages": 0,

                "storage_used": 0,

                "recent_chats": [],

                "last_login": None,

            }


# =====================================
# Backward Compatibility
# =====================================

def get_dashboard_stats(email: str):
    """
    Keeps existing imports working.
    """

    return DashboardService.get_dashboard_stats(
        email
    )