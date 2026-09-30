"""
=========================================
NovaMind AI - Dashboard Quick Actions
=========================================

Quick navigation shortcuts for NovaMind AI.
"""

import streamlit as st


# =====================================
# Action Card
# =====================================

def action_card(
    icon: str,
    title: str,
    subtitle: str,
    page: str,
    key: str,
):
    """
    Display one quick action card.
    """

    with st.container(border=True):

        st.markdown(
            f"""
<div style="text-align:center;padding:12px;">

<div style="font-size:40px;">
{icon}
</div>

<h4 style="margin-top:10px;margin-bottom:5px;">
{title}
</h4>

<p style="
color:#64748B;
font-size:13px;
min-height:40px;
">
{subtitle}
</p>

</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            f"Open {title}",
            key=key,
            width="stretch",
        ):

            try:

                st.switch_page(page)

            except Exception:

                st.warning(
                    f"{title} page is not available yet."
                )


# =====================================
# Quick Actions
# =====================================

def show_dashboard_quick_actions():
    """
    Display dashboard shortcuts.
    """

    st.subheader("⚡ Quick Actions")

    col1, col2 = st.columns(
        2,
        gap="medium",
    )

    with col1:

        action_card(
            "💬",
            "New Chat",
            "Start a conversation with NovaMind AI.",
            "pages/chat.py",
            "qa_chat",
        )

        action_card(
            "📄",
            "Upload PDF",
            "Upload documents and chat with them.",
            "pages/pdf_library.py",
            "qa_pdf",
        )

        action_card(
            "📚",
            "PDF Library",
            "Browse your uploaded documents.",
            "pages/pdf_library.py",
            "qa_library",
        )

    with col2:

        action_card(
            "🕒",
            "History",
            "Review previous AI conversations.",
            "pages/history.py",
            "qa_history",
        )

        action_card(
            "👤",
            "Profile",
            "Manage your profile information.",
            "pages/profile.py",
            "qa_profile",
        )

        action_card(
            "⚙️",
            "Settings",
            "Customize NovaMind preferences.",
            "pages/settings.py",
            "qa_settings",
        )