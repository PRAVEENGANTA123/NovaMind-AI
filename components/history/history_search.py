"""
=========================================
NovaMind AI - History Search
=========================================
"""

import streamlit as st


def show_history_search():

    return st.text_input(

        "🔍 Search Conversations",

        placeholder="Search by prompt...",

    )