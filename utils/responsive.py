import streamlit as st

def apply_responsive_layout():
    """
    Injects device-responsive CSS rules ensuring that:
    1. Mobile views do not clip chat containers into circles or ovals.
    2. Input bars and dock controls expand fluidly on mobile screens.
    3. Proper padding is maintained above the bottom viewport.
    """
    responsive_css = """
    <style>
    /* =========================================================
       Global Responsive & Mobile Viewport Normalization
       ========================================================= */
    
    /* Remove any circular / oval clipping mask on mobile devices */
    @media (max-width: 768px) {
        /* Reset any rogue circular containers */
        div[data-testid="stVerticalBlock"] > div,
        .chat-input-container,
        .stChatInput,
        div[class*="chat-input"],
        div[class*="bottom-dock"],
        div[data-testid="stBottomBlockContainer"] {
            border-radius: 12px !important;
            clip-path: none !important;
            -webkit-clip-path: none !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }

        /* Chat input dock container pinning */
        div[data-testid="stBottomBlockContainer"] {
            padding: 8px 12px 16px 12px !important;
            background: #0e1117 !important;
            border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* Ensure input elements and send button stay aligned inline */
        .stChatInput > div {
            border-radius: 24px !important;
            width: 100% !important;
        }

        /* Ensure suggestion buttons do not push into dock */
        .main .block-container {
            padding-bottom: 120px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }
    </style>
    """
    st.markdown(responsive_css, unsafe_allow_html=True)
