import streamlit as st


def show_chat_header():

    col1, col2, col3, col4 = st.columns([6, 2, 1.5, 1])

    with col1:
        search = st.text_input(
            "Search",
            placeholder="🔍 Search chats, PDFs, history...",
            label_visibility="collapsed",
            key="chat_search",
        )

    with col2:
        model = st.selectbox(
            "Model",
            [
                "Gemini 2.5 Flash",
                "Gemini 2.5 Pro",
                "GPT-4",
                "Claude",
                "Llama 3",
            ],
            label_visibility="collapsed",
            key="chat_model",
        )

    with col3:
        st.success("🟢 Online")

    with col4:
        st.button(
            "📎",
            key="quick_upload",
            use_container_width=True,
        )

    return {
        "search": search,
        "model": model,
    }