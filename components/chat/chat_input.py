"""
==========================================================
NovaMind AI - Omnibar Interaction Console
==========================================================
"""

import streamlit as st
from services.pdf.pdf_service import PDFService
from services.ai.voice_service import VoiceService
from services.settings_service import load_settings


AVAILABLE_MODELS = {
    "AI Chat": {
        "tag": "AI Chat",
        "model_id": "gemini-1.5-flash",
        "subtitle": "Fastest answers",
        "badge": "Default",
    },
    "Deep Reasoning": {
        "tag": "Deep Reasoning",
        "model_id": "gemini-1.5-pro",
        "subtitle": "Advanced problem solving",
        "badge": "",
    },
    "Extended Thinking": {
        "tag": "Extended Thinking",
        "model_id": "gemini-1.5-pro-exp",
        "subtitle": "Complex analysis",
        "badge": "",
    },
}


def initialize_chat_settings():
    email = st.session_state.get("email", "")
    user_settings = load_settings(email) if email else {}

    defaults = {
        "active_model_name": "AI Chat",
        "auto_reasoning": False,
        "web_search": False,
        "pdf_mode": False,
        "voice_active": False,
        "uploaded_file": None,
        "uploaded_pdf_id": None,
        "uploaded_pdf_name": None,
        "uploaded_pdf_pages": 0,
        "uploaded_pdf_chunks": 0,
        "pdf_upload_processed": False,
    }

    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def process_pdf_upload(uploaded_file, target_container):
    if uploaded_file is None or uploaded_file.type != "application/pdf":
        return None

    filename = uploaded_file.name
    if (
        st.session_state.get("uploaded_pdf_name") == filename
        and st.session_state.get("uploaded_pdf_id")
        and st.session_state.get("pdf_upload_processed", False)
    ):
        return {"success": True, "pdf_id": st.session_state.uploaded_pdf_id}

    email = st.session_state.get("email", "guest")

    container = target_container.container() if target_container is not None else st.container()
    with container:
        with st.spinner("Indexing document..."):
            result = PDFService.save_pdf(email=email, uploaded_file=uploaded_file)

    if not result.get("success"):
        st.session_state.pdf_upload_processed = False
        st.error(f"Ingestion failed: {result.get('error', 'Unknown error')}")
        return result

    st.session_state.uploaded_pdf_id = result.get("pdf_id")
    st.session_state.uploaded_pdf_name = result.get("filename", filename)
    st.session_state.uploaded_pdf_pages = result.get("pages", 0)
    st.session_state.uploaded_pdf_chunks = result.get("chunks", 0)
    st.session_state.uploaded_file = filename
    st.session_state.pdf_upload_processed = True
    return result


def _on_text_submit():
    val = st.session_state.get("novamind_user_query", "").strip()
    if val:
        st.session_state["submitted_prompt"] = val
        st.session_state["novamind_user_query"] = ""


def show_chat_input(status_placeholder=None):
    initialize_chat_settings()

    active_model = st.session_state.get("active_model_name", "AI Chat")
    model_meta = AVAILABLE_MODELS.get(active_model, AVAILABLE_MODELS["AI Chat"])

    top_status_area = status_placeholder if status_placeholder is not None else st.empty()

    # Voice Input Recorder
    if st.session_state.get("voice_active", False):
        with top_status_area.container():
            with st.expander("🎙️ Speech Recognition Active", expanded=True):
                if hasattr(st, "audio_input"):
                    audio_val = st.audio_input("Record audio", key="novamind_mic_rec")
                else:
                    audio_val = st.file_uploader("Audio clip", type=["wav", "mp3", "m4a"], key="novamind_mic_fallback")

                if audio_val is not None:
                    with st.spinner("Transcribing..."):
                        res = VoiceService.speech_to_text(audio_val.read())
                        if res.get("success"):
                            transcribed = res.get("text", "").strip()
                            if transcribed:
                                st.session_state["submitted_prompt"] = transcribed
                                st.session_state.voice_active = False
                                st.rerun()
                        else:
                            st.warning(res.get("error", "Transcription failed."))

    # Styling with explicit top-gap spacing
    st.markdown("""
        <style>
        /* Capsule Wrapper with generous spacing from above suggestions */
        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 9999px !important;
            padding: 4px 16px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
            align-items: center !important;
            margin-top: 24px !important;
            margin-bottom: 12px !important;
        }

        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor):focus-within {
            border-color: #CBD5E1 !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08) !important;
        }

        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) div[data-testid="stColumn"] {
            padding: 0 !important;
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            display: flex !important;
            align-items: center !important;
        }

        /* Seamless transparent text input */
        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) div[data-testid="stTextInput"],
        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) div[data-baseweb="input"],
        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) div[data-baseweb="base-input"] {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
        }

        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) input {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            color: #0F172A !important;
            -webkit-text-fill-color: #0F172A !important;
            font-size: 16px !important;
            padding: 8px 10px !important;
            width: 100% !important;
        }

        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) input::placeholder {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-size: 16px !important;
        }

        /* Borderless popover trigger buttons */
        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) div[data-testid="stPopover"] {
            border: none !important;
            background: transparent !important;
        }

        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) div[data-testid="stPopover"] > button {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            color: #1E293B !important;
            font-size: 15px !important;
            font-weight: 400 !important;
            padding: 4px 6px !important;
            border-radius: 9999px !important;
        }

        /* Action buttons (Mic & Send) */
        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) button[kind="secondary"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            color: #1E293B !important;
            font-size: 18px !important;
            padding: 4px 6px !important;
            border-radius: 9999px !important;
        }

        div[data-testid="stHorizontalBlock"]:has(#novamind-omnibar-anchor) button[kind="secondary"]:hover {
            background: #F1F5F9 !important;
            color: #0F172A !important;
        }
        </style>
    """, unsafe_allow_html=True)

    c_plus, c_text, c_model, c_mic, c_send = st.columns(
        [0.08, 0.64, 0.16, 0.06, 0.06],
        gap="small",
        vertical_alignment="center",
    )

    uploaded = None

    # 1. [+] Tools Popover
    with c_plus:
        st.markdown('<span id="novamind-omnibar-anchor" style="display:none;"></span>', unsafe_allow_html=True)
        with st.popover("+ ⌵", help="Tools & Files", use_container_width=True):
            st.markdown("#### 🛠️ Workspace Tools")
            uploaded = st.file_uploader(
                "Attach Documents",
                type=["pdf", "docx", "txt", "csv", "xlsx", "png", "jpg", "jpeg"],
                key="omnibar_file_up",
            )
            st.divider()

            pdf_toggle = st.toggle("📄 PDF Grounding", value=st.session_state.get("pdf_mode", False), key="w_pdf_mode")
            web_toggle = st.toggle("🌐 Web Grounding", value=st.session_state.get("web_search", False), key="w_web_search")
            reason_toggle = st.toggle("🧠 Adaptive Reasoning", value=st.session_state.get("auto_reasoning", False), key="w_auto_reasoning")

            st.session_state["pdf_mode"] = pdf_toggle
            st.session_state["web_search"] = web_toggle
            st.session_state["auto_reasoning"] = reason_toggle

            st.divider()
            if st.button("🗑️ Reset Chat History", use_container_width=True):
                st.session_state.messages = []
                st.session_state["submitted_prompt"] = None
                st.rerun()

    # 2. Text Input Field
    with c_text:
        typed = st.text_input(
            "Query Input",
            placeholder="Ask NovaMind-AI...",
            label_visibility="collapsed",
            key="novamind_user_query",
            on_change=_on_text_submit,
        )

    # 3. Model Engine Picker
    with c_model:
        with st.popover(f"{model_meta['tag']} ⌵", use_container_width=True):
            st.markdown("#### Select Engine")
            for name, meta in AVAILABLE_MODELS.items():
                is_selected = name == active_model
                prefix = "✓ " if is_selected else ""
                badge = f" `{meta['badge']}`" if meta.get("badge") else ""

                if st.button(
                    f"{prefix}{name}{badge}\n\n{meta['subtitle']}",
                    key=f"engine_{name}",
                    use_container_width=True,
                ):
                    st.session_state.active_model_name = name
                    st.rerun()

    # 4. Microphone Trigger
    with c_mic:
        if st.button("🎙️", key="novamind_mic_btn", help="Voice Input", use_container_width=True):
            st.session_state.voice_active = not st.session_state.get("voice_active", False)
            st.rerun()

    # 5. Send Button (Clickable Arrow)
    with c_send:
        if st.button("➤", key="novamind_send_btn", help="Send Message", use_container_width=True):
            if typed.strip():
                st.session_state["submitted_prompt"] = typed.strip()
                st.session_state["novamind_user_query"] = ""
                st.rerun()

    if uploaded is not None and uploaded.type == "application/pdf":
        process_pdf_upload(uploaded, top_status_area)

    final_prompt = st.session_state.pop("submitted_prompt", None)
    if final_prompt:
        return {
            "prompt": final_prompt,
            "model_id": model_meta["model_id"],
            "model_name": active_model,
            "web_search": st.session_state.get("web_search", False),
            "pdf_mode": st.session_state.get("pdf_mode", False) or (uploaded is not None),
            "uploaded_file": uploaded,
            "pdf_id": st.session_state.get("uploaded_pdf_id"),
            "status_placeholder": top_status_area,
        }

    return None