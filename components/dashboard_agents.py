"""
=========================================
NovaMind AI - AI Models Dashboard
=========================================

Displays live AI usage statistics.
"""

import streamlit as st

from database.mongodb import (
    chats_collection,
    pdf_chat_collection,
)


# =====================================
# Dashboard Agents
# =====================================

def show_dashboard_agents(email: str):
    """
    Display live AI usage.
    """

    # ---------------------------------
    # Live Counts
    # ---------------------------------

    general_ai = chats_collection.count_documents(
        {
            "email": email
        }
    )

    pdf_ai = pdf_chat_collection.count_documents(
        {
            "email": email
        }
    )

    web_ai = 0

    total = general_ai + pdf_ai + web_ai

    if total == 0:
        total = 1

    agents = [

        {
            "icon": "🤖",
            "name": "Gemini AI",
            "status": "🟢 Online",
            "uses": general_ai,
            "percent": round(
                general_ai / total * 100,
                1,
            ),
            "default": True,
        },

        {
            "icon": "📄",
            "name": "PDF Assistant",
            "status": "🟢 Ready",
            "uses": pdf_ai,
            "percent": round(
                pdf_ai / total * 100,
                1,
            ),
            "default": False,
        },

        {
            "icon": "🌐",
            "name": "Web Search",
            "status": "🟡 Coming Soon",
            "uses": web_ai,
            "percent": 0,
            "default": False,
        },

    ]

    st.subheader("🤖 AI Models")

    for agent in agents:

        with st.container(border=True):

            left, right = st.columns(
                [3, 1]
            )

            with left:

                st.markdown(
                    f"### {agent['icon']} {agent['name']}"
                )

                st.caption(
                    agent["status"]
                )

                st.progress(
                    agent["percent"] / 100
                )

            with right:

                st.metric(
                    "Uses",
                    agent["uses"],
                )

                st.metric(
                    "Usage",
                    f"{agent['percent']}%",
                )

            if agent["default"]:

                st.success(
                    "Default AI Model"
                )