"""
=========================================
NovaMind AI Navigation Service
=========================================
"""

import streamlit as st


class NavigationService:
    """
    Handles page navigation history.
    """

    @staticmethod
    def initialize():
        """Initialize navigation history."""
        if "navigation_history" not in st.session_state:
            st.session_state.navigation_history = []

    @staticmethod
    def visit(page: str):
        """Add a page to history if it isn't already the current page."""
        NavigationService.initialize()

        history = st.session_state.navigation_history

        if not history or history[-1] != page:
            history.append(page)

    @staticmethod
    def can_go_back() -> bool:
        """Return True if a previous page exists."""
        NavigationService.initialize()

        return len(st.session_state.navigation_history) > 1

    @staticmethod
    def go_back():
        """Return the previous page and remove the current page."""
        NavigationService.initialize()

        history = st.session_state.navigation_history

        if len(history) <= 1:
            return None

        # Remove current page
        history.pop()

        # Return previous page
        return history[-1]

    @staticmethod
    def current():
        """Return the current page."""
        NavigationService.initialize()

        history = st.session_state.navigation_history

        if history:
            return history[-1]

        return None

    @staticmethod
    def clear():
        """Clear navigation history."""
        st.session_state.navigation_history = []