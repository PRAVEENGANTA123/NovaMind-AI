"""
=========================================
NovaMind AI - AI Settings
=========================================
"""

import streamlit as st


def show_ai_settings(settings):

    st.subheader("🤖 AI Preferences")

    models = [

        "Gemini 2.5 Flash",

        "Gemini 2.5 Pro",

        "GPT-4",

        "Claude 4",

        "Llama 3",

    ]

    current_model = settings.get(
        "default_model",
        "Gemini 2.5 Flash"
    )

    if current_model not in models:
        current_model = models[0]

    col1, col2 = st.columns(2)

    with col1:

        default_model = st.selectbox(
            "Default AI Model",
            models,
            index=models.index(current_model),
        )

        conversation_memory = st.toggle(
            "Conversation Memory",
            value=settings.get(
                "conversation_memory",
                True
            )
        )

    with col2:

        temperature = st.slider(
            "Temperature",
            0.0,
            2.0,
            float(settings.get("temperature", 0.7)),
            0.1,
        )

        max_tokens = st.slider(
            "Max Tokens",
            512,
            8192,
            int(settings.get("max_tokens", 2048)),
            256,
        )

    return {

        "default_model": default_model,

        "temperature": temperature,

        "conversation_memory": conversation_memory,

        "max_tokens": max_tokens,

    }