"""
=========================================
NovaMind AI - Chat Welcome
=========================================
"""

import streamlit as st


def show_chat_welcome():
    """
    Display welcome screen when there are no chat messages.
    """
    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # Header
    # =====================================
    st.markdown(
        """
        <div style="text-align:center;">
            <h1>🤖 NovaMind AI</h1>
            <p style="font-size:18px;color:#64748B;">
                How can I help you today?
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # Suggested Prompts
    # =====================================
    st.subheader("✨ Suggested Prompts")

    prompts = [
        ("🧠 Explain LangChain Agents", "Explain LangChain Agents and how they make decisions."),
        ("📄 Summarize my PDF", "Can you summarize the key takeaways of my uploaded document?"),
        ("💻 Write Python Code", "Write a Python script for asynchronous data fetching."),
        ("🌐 Research Latest AI News", "Search the web for the latest artificial intelligence breakthroughs."),
        ("📊 Analyze Dataset", "How do I perform exploratory data analysis on a CSV file?"),
        ("🎓 Prepare Interview Questions", "Give me 5 challenging machine learning interview questions."),
    ]

    col1, col2 = st.columns(2)

    for idx, (label, prompt_text) in enumerate(prompts):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            if st.button(label, key=f"prompt_suggestion_{idx}", use_container_width=True):
                st.session_state["pending_prompt"] = prompt_text
                st.rerun()
