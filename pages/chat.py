"""
=========================================
NovaMind AI - Chat Workspace
=========================================

Main chat workspace.

Flow:

User
 ↓
Chat Input
 ↓
PDF / Web / Normal Request
 ↓
AI Orchestrator
 ↓
PDF RAG / Web Search / AI
 ↓
Chat History
 ↓
UI Response
"""

from datetime import datetime
import streamlit as st
import re
from utils.styles import load_css

from components.sidebar import show_sidebar
from components.navbar import show_navbar
from components.chat.chat_header import show_chat_header
from components.chat.smart_toolbar import show_smart_toolbar
from components.chat.status_bar import show_status_bar
from components.chat.chat_messages import show_chat_messages
from components.chat.chat_input import show_chat_input
from components.chat.export_button import show_export_button
from services.chat.chat_service import ChatService
from services.ai.orchestrator_service import AIOrchestrator
from services.site_archiver import SiteArchiver
from services.export.export_service import ExportService
from services.ai.voice_service import VoiceService
from utils.responsive import apply_responsive_layout

# =========================================
# Page Config
# =========================================

# MUST be the first Streamlit command
st.set_page_config(
    page_title="NovaMind AI | Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="auto"
)

# Apply device-flexible styling (mobile, tablet, desktop)
apply_responsive_layout()

def apply_responsive_theme():
    """Inject universal responsive styling for all viewports (mobile, tablet, desktop)."""
    st.markdown("""
        
    """, unsafe_allow_html=True)


# Rest of your app.py logic and navigation...

# =========================================
# Authentication
# =========================================

if not st.session_state.get(
    "logged_in",
    False,
):
    st.switch_page("pages/login.py")
    st.stop()


# =========================================
# Current Page
# =========================================

st.session_state["current_page"] = "Chat"

# ============================================================
# URL CONVERSATION STATE
# Keeps the active website for follow-up questions
# ============================================================

if "active_url" not in st.session_state:
    st.session_state.active_url = None

if "active_domain" not in st.session_state:
    st.session_state.active_domain = None

if "url_analysis_result" not in st.session_state:
    st.session_state.url_analysis_result = None

if "url_analysis_error" not in st.session_state:
    st.session_state.url_analysis_error = None

if "url_input_value" not in st.session_state:
    st.session_state.url_input_value = ""


# =========================================
# CSS
# =========================================

load_css("chat.css")


# =========================================
# Sidebar + Navbar
# =========================================

show_sidebar()

show_navbar(is_chat=True)

# =========================================
# Header
# =========================================

# show_chat_header()

st.divider()

st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

# =========================================
# Step 6B : Website Analysis Panel
# =========================================

with st.container():

    st.markdown("### 🔗 Website Analysis")

    url_input = st.text_input(
        "Website URL",
        value=st.session_state.get("url_input_value", ""),
        placeholder="https://example.com/",
        key="website_url_input",
        label_visibility="collapsed",
    )

    url_col1, url_col2 = st.columns([0.78, 0.22], gap="small")

    with url_col2:
        if st.button(
            "🔍 Analyze URL",
            key="analyze_url_btn",
            use_container_width=True,
        ):
            candidate_url = (url_input or "").strip()

            if not candidate_url:
                st.warning("Please enter a website URL.")
            else:
                if not re.match(r"^https?://", candidate_url, re.IGNORECASE):
                    candidate_url = "https://" + candidate_url

                with st.spinner("Analyzing website..."):
                    try:
                        analysis = AIOrchestrator._process_url(
                            candidate_url,
                            query="",
                            max_pages=1,
                            crawl_timeout=60,
                        )

                        if analysis.get("success", False):
                            st.session_state.active_url = analysis.get("final_url", candidate_url)
                            st.session_state.active_domain = analysis.get("domain", "")
                            st.session_state.url_analysis_result = analysis
                            st.session_state.url_analysis_error = None
                            st.session_state.url_input_value = candidate_url
                            st.success("Website analyzed successfully.")
                            st.rerun()
                        else:
                            error_message = analysis.get("error", "Website analysis failed.")
                            st.session_state.url_analysis_error = error_message
                            st.error("❌ " + error_message)

                    except Exception as error:
                        st.session_state.url_analysis_error = str(error)
                        st.error("❌ Website analysis failed: " + str(error))

    with url_col1:
        if st.session_state.get("active_url"):
            analysis_result = st.session_state.get("url_analysis_result") or {}

            st.markdown("#### 🌐 Website Information")

            title = analysis_result.get("title", "") or "Untitled Website"
            final_url = analysis_result.get("final_url", st.session_state.active_url) or st.session_state.active_url
            domain = analysis_result.get("domain", st.session_state.get("active_domain", "")) or st.session_state.get("active_domain", "")
            resources = analysis_result.get("resources", []) or []
            retrieved_resources = analysis_result.get("retrieved_resources", []) or []

            resource_count = len(resources)
            retrieved_count = len(retrieved_resources)

            info_col1, info_col2 = st.columns([0.72, 0.28], gap="small")

            with info_col1:
                st.markdown(f"**Title:** {title}")
                st.markdown(f"**URL:** {final_url}")
                st.markdown(f"**Domain:** {domain or 'Unknown'}")

            with info_col2:
                st.metric("Resources", resource_count)
                if analysis_result.get("success", False):
                    st.success("🟢 Analyzed", icon="🌐")
                else:
                    st.warning("Analysis incomplete")

            st.caption(
                f"Website resources discovered: {resource_count}"
                + (f"  •  Retrieved for current question: {retrieved_count}" if retrieved_count else "")
            )

            # =========================================
            # 2. WEBSITE RESOURCES
            # =========================================

            st.markdown("#### 📚 Website Resources")

            display_resources = retrieved_resources if retrieved_resources else resources

            if display_resources:
                st.caption(f"{len(resources)} resource(s) discovered. Relevant resources are shown first.")

                resource_search = st.text_input(
                    "Search website resources",
                    placeholder="🔎 Search resources by title or URL...",
                    key="website_resource_search",
                    label_visibility="collapsed",
                )

                filtered_resources = []
                search_term = (resource_search or "").strip().lower()

                for resource in display_resources:
                    if not isinstance(resource, dict):
                        continue

                    title_text = str(resource.get("title", "") or "")
                    url_text = str(resource.get("url", "") or "")

                    if (
                        not search_term
                        or search_term in title_text.lower()
                        or search_term in url_text.lower()
                    ):
                        filtered_resources.append(resource)

                if search_term:
                    visible_resources = filtered_resources
                else:
                    visible_resources = filtered_resources[:10]

                if not visible_resources:
                    st.info(f'No resources match "{resource_search}".')
                else:
                    section_label = (
                        f"🔎 Search results ({len(visible_resources)})"
                        if search_term
                        else f"⭐ Relevant Resources ({len(visible_resources)})"
                    )

                    st.markdown(f"**{section_label}**")

                    for index, resource in enumerate(visible_resources, start=1):
                        resource_title = resource.get("title", "") or "Untitled resource"
                        resource_url = resource.get("url", "") or ""
                        resource_score = resource.get("score")

                        with st.container(border=True):
                            st.markdown(f"**{index}. {resource_title}**")
                            if resource_url:
                                st.markdown(resource_url)
                            if resource_score is not None:
                                try:
                                    score_text = f"{float(resource_score):.4f}"
                                except (TypeError, ValueError):
                                    score_text = str(resource_score)
                                st.caption("Relevance score: " + score_text)

                if not search_term and len(filtered_resources) > 10:
                    with st.expander(
                        f"📋 Show all {len(filtered_resources)} resources",
                        expanded=False,
                    ):
                        for index, resource in enumerate(filtered_resources, start=1):
                            resource_title = resource.get("title", "") or "Untitled resource"
                            resource_url = resource.get("url", "") or ""
                            st.markdown(f"**{index}. {resource_title}**")
                            if resource_url:
                                st.caption(resource_url)
            else:
                st.info("No website resources were discovered.")

    if st.session_state.get("active_url"):
        if st.button("🧹 Clear URL", key="clear_active_url"):
            st.session_state.active_url = None
            st.session_state.active_domain = None
            st.session_state.url_analysis_result = None
            st.session_state.url_analysis_error = None
            st.session_state.url_input_value = ""
            st.rerun()


# =========================================
# Active Website Card
# =========================================

active_url = st.session_state.get("active_url")

if active_url:
    active_domain = st.session_state.get("active_domain")
    if not active_domain:
        active_domain = re.sub(r"^https?://", "", active_url, flags=re.IGNORECASE).split("/")[0]
        st.session_state.active_domain = active_domain

    st.markdown(
        f"""
        <div class="active-url-card">
            <div class="active-url-title">
                🔗 Active Website
            </div>
            <div class="active-url-domain">
                {active_domain}
            </div>
            <div class="active-url-address">
                {active_url}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# =========================================
# Active Document Indicator
# =========================================
# >>> REPLACE WITH:
active_document_name = st.session_state.get("active_document_name")
active_document_type = st.session_state.get("active_document_type")

if active_document_name:
    st.caption(
        f"📎 Active document: {active_document_name}"
        + (f" ({active_document_type})" if active_document_type else "")
    )

# show_status_bar()  # Removed: hides the "🟢 Online | 🌐 General AI | 🧠 Auto AI" strip

# Spacing gap between Website Analysis and NovaMind AI logo / suggested prompts
st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)

# =========================================
# Initialize Messages
# =========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================
# Active Document State
# =========================================

if "active_document_name" not in st.session_state:
    st.session_state.active_document_name = None

if "active_document_type" not in st.session_state:
    st.session_state.active_document_type = None

if "active_pdf_id" not in st.session_state:
    st.session_state.active_pdf_id = None

if "active_pdf_name" not in st.session_state:
    st.session_state.active_pdf_name = None


def _uploaded_file_info(uploaded_file):
    if uploaded_file is None:
        return "", "", ""
    name = str(getattr(uploaded_file, "name", "") or "").strip()
    mime_type = str(getattr(uploaded_file, "type", "") or "").strip().lower()
    extension = ""
    if "." in name:
        extension = "." + name.rsplit(".", 1)[-1].lower()
    return name, extension, mime_type


def _is_pdf_file(uploaded_file):
    name, extension, mime_type = _uploaded_file_info(uploaded_file)
    return extension == ".pdf" or mime_type == "application/pdf"


def _extract_url(text):
    if not text:
        return ""
    match = re.search(r"https?://[^\s\]\)>]+", str(text), re.IGNORECASE)
    return match.group(0).strip().rstrip(".,;:!?)]}>") if match else ""


def _set_active_url(url):
    clean_url = str(url or "").strip().rstrip(".,;:!?)]}>")
    if not clean_url:
        return ""
    if not re.match(r"^https?://", clean_url, re.IGNORECASE):
        clean_url = "https://" + clean_url
    st.session_state.active_url = clean_url
    st.session_state.active_domain = re.sub(r"^https?://", "", clean_url, flags=re.IGNORECASE).split("/")[0]
    return clean_url


def _get_active_url():
    value = str(st.session_state.get("active_url") or "").strip()
    if not re.match(r"^https?://", value, re.IGNORECASE):
        return ""
    return value.rstrip(".,;:!?)]}>")


def _safe_result_answer(result):
    return str(getattr(result, "answer", "") or "").strip()


def _run_orchestrator(prompt, active_url, web_search, uploaded_file, pdf_mode, pdf_id, email):
    kwargs = dict(
        prompt=prompt,
        web_search=web_search,
        active_url=active_url or None,
        uploaded_file=uploaded_file,
        pdf_mode=pdf_mode,
        pdf_id=pdf_id,
        email=email,
        crawl_timeout=60,
    )

    result = AIOrchestrator.process(**kwargs)

    if active_url and not getattr(result, "success", False):
        print("=" * 60)
        print("URL RETRY")
        print("Active URL:", active_url)
        print("Reason:", _safe_result_answer(result))
        print("=" * 60)

        retry = AIOrchestrator.process(**kwargs)
        if getattr(retry, "success", False):
            return retry

    return result


uploaded_pdf_id = st.session_state.get("uploaded_pdf_id")
uploaded_pdf_name = st.session_state.get("uploaded_pdf_name")

if uploaded_pdf_id:
    st.session_state.active_pdf_id = uploaded_pdf_id

if uploaded_pdf_name:
    st.session_state.active_pdf_name = uploaded_pdf_name
    st.session_state.active_document_name = uploaded_pdf_name
    st.session_state.active_document_type = ".pdf"


# =========================================
# Export Button
# =========================================

if st.session_state.get("last_url_result"):
    if st.sidebar.button("💾 Export Offline Site Mirror"):
        export_dir = SiteArchiver.export_offline_mirror(st.session_state["last_url_result"])
        st.sidebar.success(f"Archived to `{export_dir}`!")

show_export_button()
st.divider()


# =========================================
# Display Existing Messages (Strictly Above Input)
# =========================================

show_chat_messages()


# =========================================
# Regenerate Response
# =========================================

if st.session_state.get("regenerate", False):
    st.session_state.regenerate = False
    last_prompt = None

    for message in reversed(st.session_state.messages):
        if message.get("role") == "user":
            last_prompt = message.get("content")
            break

    detected_url = _extract_url(last_prompt)
    if detected_url:
        _set_active_url(detected_url)
        print("=" * 60)
        print("ACTIVE URL SET")
        print("URL:", detected_url)
        print("=" * 60)

    if last_prompt:
        with st.spinner("Regenerating response..."):
            try:
                email = st.session_state.get("email")
                pdf_mode = st.session_state.get("pdf_mode", False)
                pdf_id = st.session_state.get("uploaded_pdf_id")
                web_search = st.session_state.get("web_search", False)

                result = _run_orchestrator(
                    prompt=last_prompt,
                    active_url=_get_active_url(),
                    web_search=web_search,
                    uploaded_file=None,
                    pdf_mode=pdf_mode,
                    pdf_id=pdf_id,
                    email=email,
                )

                answer = result.answer
                chat_id = ChatService.save(
                    result=result,
                    email=email,
                    prompt=last_prompt,
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "timestamp": datetime.now().strftime("%I:%M %p"),
                    "chat_id": chat_id,
                    "message_id": None,
                })
                st.rerun()
            except Exception as e:
                st.error(f"❌ Regeneration failed: {e}")


# ==============================================================================
# Dynamic Message & Thinking Container (Always Stays Above the Chat Bar)
# ==============================================================================

# Gap between suggested prompts / messages and the input bar
st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# Placeholder that renders current turn messages & thinking spinner
thinking_placeholder = st.empty()

# ==============================================================================
# Chat Input (Anchored at the bottom)
# ==============================================================================

chat = show_chat_input(status_placeholder=thinking_placeholder)

if chat is None:
    st.stop()

# =========================================
# Read Chat Input
# =========================================

prompt = chat.get("prompt", "")
web_search = chat.get("web_search", False)
requested_pdf_mode = bool(chat.get("pdf_mode", False))
uploaded_file = chat.get("uploaded_file")
pdf_id = chat.get("pdf_id")

document_name, document_extension, document_mime = _uploaded_file_info(uploaded_file)
is_pdf_upload = _is_pdf_file(uploaded_file)

pdf_mode = requested_pdf_mode and (is_pdf_upload or bool(pdf_id))

if uploaded_file is not None:
    st.session_state.active_document_name = document_name or None
    st.session_state.active_document_type = document_extension or document_mime or None
    if is_pdf_upload:
        st.session_state.active_pdf_name = document_name or None

if not prompt:
    st.stop()

if pdf_id:
    st.session_state.active_pdf_id = pdf_id
    st.session_state.active_pdf_name = st.session_state.get("uploaded_pdf_name")

if requested_pdf_mode and uploaded_file is not None:
    if not is_pdf_upload:
        pdf_mode = False
elif requested_pdf_mode and uploaded_file is None and not pdf_id:
    st.error("📄 PDF Mode is enabled, but no processed PDF is selected. Please upload a PDF first.")
    st.stop()

if is_pdf_upload and requested_pdf_mode and not pdf_id:
    st.error("📄 The PDF was uploaded, but it has not been processed/selected for PDF mode yet.")
    st.stop()


# =========================================
# AI Processing (Routed inside thinking_placeholder ABOVE chat bar)
# =========================================

answer = ""
chat_id = None

with thinking_placeholder.container():
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("NovaMind AI is thinking..."):
        try:
            email = st.session_state.get("email")

            print("=" * 60)
            print("CHAT REQUEST")
            print("=" * 60)
            print("Prompt     :", prompt)
            print("Web Search :", web_search)
            print("PDF Mode   :", pdf_mode)
            print("PDF ID     :", pdf_id)
            print("File Name  :", document_name or "None")
            print("File Type  :", document_extension or document_mime or "None")
            print("Active URL :", _get_active_url() or "None")
            print("Email      :", email)
            print("=" * 60)

            detected_url = _extract_url(prompt)
            if detected_url:
                _set_active_url(detected_url)
                st.session_state.url_analysis_result = None
                st.session_state.url_analysis_error = None
                print("=" * 60)
                print("NEW ACTIVE URL")
                print("Active URL:", _get_active_url())
                print("=" * 60)

            result = _run_orchestrator(
                prompt=prompt,
                active_url=_get_active_url(),
                web_search=web_search,
                uploaded_file=uploaded_file,
                pdf_mode=pdf_mode,
                pdf_id=pdf_id,
                email=email,
            )

            answer = _safe_result_answer(result)

            if not answer:
                if _get_active_url() and not getattr(result, "success", False):
                    answer = "I couldn't retrieve readable information from the active website. Please try again or re-analyze the website."
                else:
                    answer = "NovaMind AI did not return a response."

            chat_id = ChatService.save(
                result=result,
                email=email,
                prompt=prompt,
            )

        except Exception as e:
            print("=" * 60)
            print("CHAT ERROR")
            print(e)
            print("=" * 60)
            answer = f"❌ I could not process your request.\n\nError: {e}"
            chat_id = None

# =========================================
# Save Messages & Refresh
# =========================================

# 1. Save user prompt
st.session_state.messages.append({
    "role": "user",
    "content": prompt,
    "timestamp": datetime.now().strftime("%I:%M %p"),
    "chat_id": None,
    "message_id": None,
})

# 2. Save assistant answer
st.session_state.messages.append({
    "role": "assistant",
    "content": answer,
    "timestamp": datetime.now().strftime("%I:%M %p"),
    "chat_id": chat_id,
    "message_id": None,
})

# 3. Clean up placeholder and re-render conversation history cleanly
thinking_placeholder.empty()
st.rerun()
