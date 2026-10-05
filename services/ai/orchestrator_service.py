"""
=========================================
NovaMind AI - AI Orchestrator Service
=========================================

Main AI Pipeline

User
  ↓
Reasoning
  ↓
Tool Router
  ↓
Context
  ↓
Planner
  ↓
Execution
  ↓
PDF / DOCX / TXT / URL / Web Search
  ↓
STRICT SOURCE GROUNDING
  ↓
Gemini
  ↓
Final AI Response
"""

from dataclasses import dataclass
import io
import logging
import re
import time
from typing import Any, Dict, List, Optional

from pypdf import PdfReader
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from services.ai.reasoning_service import ReasoningService
from services.ai.context_service import ContextService
from services.ai.planner_service import PlannerService
from services.ai.execution_service import ExecutionService
from services.ai.gemini_service import GeminiService
from services.ai.web_search_service import WebSearchService
from services.ai.url_service import URLService
from services.ai.url_engine import SafeAsyncURLEngine
from services.ai.website_retrieval_service import (
    WebsiteRetrievalService,
)
from services.ai.tool_router_service import ToolRouterService

logger = logging.getLogger("NovaMind.AIOrchestrator")

# ==========================================
# Optional PDF services
# ==========================================

try:
    from services.pdf.pdf_service import PDFService
except Exception:
    PDFService = None

try:
    from services.pdf.pdf_chat_service import PDFChatService
except Exception:
    PDFChatService = None

try:
    from database.pdf_repository import PDFRepository
except Exception:
    PDFRepository = None

# ==========================================
# Optional Database / Chat Repository
# ==========================================

try:
    from database.chat_repository import ChatRepository
except Exception:
    try:
        from services.chat.chat_service import ChatService as ChatRepository
    except Exception:
        ChatRepository = None


# ==========================================
# AI Response
# ==========================================

@dataclass
class AIResponse:
    prompt: str
    intent: str
    confidence: float
    answer: str
    execution_time: str
    success: bool


# ==========================================
# AI Orchestrator
# ==========================================

class AIOrchestrator:

    # ======================================
    # Resilient Gemini Synthesis Call
    # ======================================

    @staticmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _call_gemini_resilient(prompt_text: str) -> str:
        """Call GeminiService with automatic backoff against transient 429/503 errors."""
        gemini = GeminiService()
        return gemini.generate(prompt_text)

    # ======================================
    # MongoDB Turn Persistence Helper
    # ======================================

    @staticmethod
    def _persist_turn_safely(
        email: Optional[str],
        prompt: str,
        answer: str,
        intent: str,
        confidence: float,
        execution_time: str,
    ) -> None:
        """Safely commits the conversational turn to MongoDB without blocking."""
        if not ChatRepository or not email:
            return
        try:
            repo = ChatRepository()
            if hasattr(repo, "save_chat"):
                repo.save_chat(
                    email=email,
                    prompt=prompt,
                    response=answer,
                    intent=intent,
                    confidence=confidence,
                )
            elif hasattr(repo, "save_turn"):
                repo.save_turn(
                    user_id=email,
                    session_id="default_session",
                    user_prompt=prompt,
                    assistant_response=answer,
                    metadata={
                        "intent": intent,
                        "confidence": confidence,
                        "execution_time": execution_time,
                    },
                )
        except Exception as db_err:
            logger.debug(f"Non-blocking MongoDB persistence notice: {db_err}")

    # ======================================
    # URL Detection
    # ======================================

    @staticmethod
    def _extract_url(prompt: str) -> str:
        """Extract the first HTTP/HTTPS URL from a prompt."""

        if not prompt:
            return ""

        match = re.search(
            r"https?://[^\s\]\)>]+",
            prompt,
            re.IGNORECASE,
        )

        if not match:
            return ""

        url = match.group(0).strip()

        return url.rstrip(
            ".,;:!?)]}>\"'"
        )

    # ======================================
    # File Reader
    # ======================================

    @staticmethod
    def _read_uploaded_file(uploaded_file):
        """Extract readable content from PDF, DOCX or TXT."""

        if uploaded_file is None:
            return "", ""

        filename = getattr(
            uploaded_file,
            "name",
            "Uploaded File",
        )

        document_source = filename

        try:
            file_bytes = uploaded_file.getvalue()

            extension = ""

            if "." in filename:
                extension = (
                    filename.rsplit(".", 1)[1]
                    .lower()
                    .strip()
                )

            # ----------------------------------
            # PDF
            # ----------------------------------

            if extension == "pdf":

                reader = PdfReader(
                    io.BytesIO(file_bytes)
                )

                pages = []

                for page_number, page in enumerate(
                    reader.pages,
                    start=1,
                ):

                    try:
                        text = (
                            page.extract_text()
                            or ""
                        )

                        if text.strip():
                            pages.append(
                                f"""
--- Page {page_number} ---

{text}
"""
                            )

                    except Exception as page_error:
                        pages.append(
                            f"""
--- Page {page_number} ---

Unable to extract this page.

Error:
{str(page_error)}
"""
                        )

                extracted_text = (
                    "\n".join(pages).strip()
                )

                if extracted_text:
                    return (
                        document_source,
                        f"""
Uploaded File:
{filename}

File Type:
PDF

Number of Pages:
{len(reader.pages)}

Document Content:
{extracted_text[:30000]}
""",
                    )

                return (
                    document_source,
                    f"""
Uploaded File:
{filename}

File Type:
PDF

The PDF was uploaded successfully,
but no readable text could be extracted.
""",
                )

            # ----------------------------------
            # DOCX
            # ----------------------------------

            if extension == "docx":

                from docx import Document

                document = Document(
                    io.BytesIO(file_bytes)
                )

                parts = []

                for paragraph in document.paragraphs:
                    text = paragraph.text.strip()

                    if text:
                        parts.append(text)

                for table in document.tables:

                    for row in table.rows:

                        cells = []

                        for cell in row.cells:

                            text = (
                                cell.text.strip()
                            )

                            if text:
                                cells.append(text)

                        if cells:
                            parts.append(
                                " | ".join(cells)
                            )

                extracted_text = (
                    "\n".join(parts).strip()
                )

                if extracted_text:
                    return (
                        document_source,
                        f"""
Uploaded File:
{filename}

File Type:
DOCX

Document Content:
{extracted_text[:30000]}
""",
                    )

                return (
                    document_source,
                    f"""
Uploaded File:
{filename}

File Type:
DOCX

The DOCX file was opened successfully,
but no readable text was found.
""",
                )

            # ----------------------------------
            # TXT
            # ----------------------------------

            if extension == "txt":

                extracted_text = file_bytes.decode(
                    "utf-8",
                    errors="replace",
                )

                if extracted_text.strip():
                    return (
                        document_source,
                        f"""
Uploaded File:
{filename}

File Type:
TXT

Document Content:
{extracted_text[:30000]}
""",
                    )

                return (
                    document_source,
                    f"""
Uploaded File:
{filename}

File Type:
TXT

The TXT file is empty.
""",
                )

            # ----------------------------------
            # Unsupported
            # ----------------------------------

            return (
                document_source,
                f"""
Uploaded File:
{filename}

File Type:
.{extension}

This file type is currently not supported
for text extraction.

Currently supported:
PDF, DOCX, TXT
""",
            )

        except Exception as e:

            return (
                document_source,
                f"""
Uploaded File:
{filename}

The file was received, but NovaMind AI
could not extract its contents.

Error:
{str(e)}
""",
            )

    # ======================================
    # PDF RAG
    # ======================================

    @staticmethod
    def _process_pdf(
        prompt: str,
        uploaded_file=None,
        pdf_mode: bool = False,
        pdf_id: str = None,
        email: str = None,
    ):
        """Handle PDF RAG using the dedicated PDF pipeline."""

        if not pdf_mode:
            return None

        if PDFChatService is None:
            return {
                "success": False,
                "answer": "PDFChatService is unavailable.",
                "sources": [],
            }

        try:

            resolved_pdf_id = pdf_id

            if (
                not resolved_pdf_id
                and uploaded_file is not None
                and PDFService is not None
            ):

                if not email:
                    email = "guest"

                upload_result = PDFService.save_pdf(
                    email=email,
                    uploaded_file=uploaded_file,
                )

                if not upload_result.get(
                    "success",
                    False,
                ):
                    return {
                        "success": False,
                        "answer": upload_result.get(
                            "error",
                            "PDF upload failed.",
                        ),
                        "sources": [],
                    }

                resolved_pdf_id = str(
                    upload_result["pdf_id"]
                )

            if not resolved_pdf_id:
                return {
                    "success": False,
                    "answer": (
                        "PDF ID is required for "
                        "PDF question answering."
                    ),
                    "sources": [],
                }

            print("=" * 60)
            print("PDF RAG MODE")
            print("PDF ID :", resolved_pdf_id)
            print("=" * 60)

            result = PDFChatService().ask(
                pdf_id=resolved_pdf_id,
                question=prompt,
                top_k=5,
            )

            return result

        except Exception as e:

            print("=" * 60)
            print("PDF RAG ERROR")
            print(e)
            print("=" * 60)

            return {
                "success": False,
                "answer": (
                    "I could not process the uploaded PDF.\n\n"
                    f"Error: {str(e)}"
                ),
                "sources": [],
            }

    # ======================================
    # URL Retrieval / Multi-page Analysis
    # ======================================

    @staticmethod
    def _process_url(
        url: str,
        query: str = "",
        max_pages=None,
        crawl_timeout=None,
    ):
        """
        Analyze the supplied URL and retrieve relevant grounded content
        from same-domain internal pages with token budget protection.
        """

        if not url:
            return {
                "success": False,
                "url": "",
                "title": "",
                "content": "",
                "error": "No URL supplied.",
            }

        try:

            print("=" * 60)
            print("ADVANCED URL MODE")
            print("URL:", url)
            print("QUERY:", query)
            print("=" * 60)

            analyze_kwargs = {
                "query": query,
                "max_pages": max_pages,
            }
            if crawl_timeout is not None:
                analyze_kwargs["crawl_timeout"] = crawl_timeout

            try:
                page = URLService.analyze(url, **analyze_kwargs)
            except TypeError as compatibility_error:
                if (
                    "crawl_timeout" in str(compatibility_error)
                    or "unexpected keyword" in str(compatibility_error)
                ):
                    analyze_kwargs.pop("crawl_timeout", None)
                    page = URLService.analyze(url, **analyze_kwargs)
                else:
                    raise

            if not isinstance(page, dict):
                return {
                    "success": False,
                    "url": url,
                    "title": "",
                    "content": "",
                    "error": "URLService returned an invalid analysis result.",
                }

            page_success = bool(page.get("success", False))
            content = (page.get("content", "") or "").strip()
            title = (page.get("title", "") or "").strip()
            analyzer_combined = (page.get("combined_content", "") or "").strip()

            resources = (
                page.get("resources", [])
                or page.get("website_resources", [])
                or []
            )
            resources = [item for item in resources if isinstance(item, dict)]

            if not content and not resources and not analyzer_combined:
                error_message = (
                    page.get(
                        "error",
                        "The URL was opened, but no readable content or resources were found.",
                    )
                    or "The URL could not be read."
                )

                if "522" in str(error_message):
                    error_message = (
                        "The website returned HTTP 522 (Cloudflare Connection Timed Out). "
                        "The remote origin did not respond, so NovaMind cannot retrieve grounded website content right now."
                    )

                return {
                    "success": False,
                    "url": url,
                    "title": title,
                    "content": "",
                    "error": error_message,
                    "resources": [],
                    "retrieved_resources": [],
                    "has_retrieved_evidence": False,
                    "page_success": page_success,
                }

            # ----------------------------------
            # Universal Website Content Grounding & Token Budgeting
            # ----------------------------------

            stop_words = {"what", "tell", "about", "give", "show", "where", "which", "how", "who", "the", "and", "for", "with", "this", "is", "are", "me"}
            raw_tokens = [t.lower() for t in re.findall(r"\w+", query or "") if len(t) > 2]
            query_tokens = [t for t in raw_tokens if t not in stop_words]

            temporal_words = {"today", "now", "latest", "new", "schedule", "upcoming", "calendar", "streaming", "current", "list", "all", "what"}
            has_temporal = any(w in (query or "").lower() for w in temporal_words)

            # Score matching subpages based on query token relevance
            scored_resources = []
            if resources:
                for r in resources:
                    c_text = (r.get("content", "") or "").lower()
                    h_text = f"{r.get('title', '')} {r.get('url', '')}".lower()
                    score = 0
                    if query_tokens:
                        for tok in query_tokens:
                            if tok in h_text:
                                score += 25
                            if tok in c_text:
                                score += min(c_text.count(tok), 8)
                    if score > 0:
                        scored_resources.append((score, r))

            scored_resources.sort(key=lambda x: x[0], reverse=True)
            # Cap to top 6 relevant resources to prevent 429 token limits
            matching_resources = [r for _, r in scored_resources[:6]]

            if matching_resources:
                matched_blocks = []
                source_idx = 1
                if (has_temporal or len(matching_resources) < 3) and content:
                    matched_blocks.append(f"[Source {source_idx}]: {title}\nURL: {url}\nCONTENT:\n{content[:10000]}\n")
                    source_idx += 1

                for r in matching_resources:
                    if r.get("url") != url:
                        sub_body = (r.get("content", "") or "")[:10000]
                        matched_blocks.append(
                            f"[Source {source_idx}]: {r.get('title', 'Page')}\nURL: {r.get('url', '')}\nCONTENT:\n{sub_body}\n"
                        )
                        source_idx += 1

                # Hard cap total context to 40,000 characters (~9k tokens)
                retrieved_context = "\n\n".join(matched_blocks)[:40000]
                retrieval = {
                    "success": True,
                    "results": matching_resources,
                    "retrieved_count": len(matching_resources),
                    "has_evidence": True,
                    "fallback_used": False,
                }
            elif has_temporal and (content or analyzer_combined):
                retrieved_context = (content[:35000] if content else analyzer_combined[:35000])
                retrieval = {
                    "success": True,
                    "results": resources[:5],
                    "retrieved_count": len(resources[:5]),
                    "has_evidence": True,
                    "fallback_used": True,
                }
            elif resources:
                retrieval = WebsiteRetrievalService.retrieve(
                    question=query,
                    resources=resources,
                    top_k=6,
                    min_score=0.04,
                )
                retrieved_context = WebsiteRetrievalService.build_context(retrieval)[:35000]
                if not retrieved_context.strip() or len(retrieved_context.strip()) < 200:
                    retrieved_context = (analyzer_combined or content)[:35000]
                    retrieval["fallback_used"] = True
                    retrieval["has_evidence"] = bool(retrieved_context.strip())
            else:
                retrieval = {
                    "success": bool(analyzer_combined or content),
                    "results": [],
                    "retrieved_count": 0,
                    "has_evidence": bool(analyzer_combined or content),
                    "fallback_used": True,
                }
                retrieved_context = (analyzer_combined or content)[:35000]

            analyzed_pages_value = page.get("analyzed_pages", []) or []
            analyzed_pages = analyzed_pages_value if isinstance(analyzed_pages_value, list) else []
            analyzed_page_count = page.get("analyzed_page_count", len(analyzed_pages))
            try:
                analyzed_page_count = int(analyzed_page_count)
            except (TypeError, ValueError):
                analyzed_page_count = len(analyzed_pages)

            source_pages = page.get("source_pages", []) or []
            if not isinstance(source_pages, list):
                source_pages = []

            if retrieved_context and retrieved_context.strip():
                grounded_content = retrieved_context
            elif analyzer_combined and analyzer_combined.strip():
                grounded_content = analyzer_combined[:35000]
            elif content:
                grounded_content = content[:35000]
            else:
                grounded_content = (
                    "No sufficiently relevant evidence was found in the analyzed website resources for this question."
                )

            print("URL ANALYSIS SUCCESS")
            print("Title:", title)
            print("Domain:", page.get("domain", ""))
            print("Analyzed Pages:", analyzed_page_count)
            print("Discovered Resources:", len(resources))
            print("Retrieved Resources:", retrieval.get("retrieved_count", 0))
            print("Evidence Found:", retrieval.get("has_evidence", False))
            print("=" * 60)

            primary_resource = {}
            if retrieval.get("results"):
                primary_resource = retrieval["results"][0]
            elif resources:
                primary_resource = resources[0]

            return {
                "success": True,
                "url": page.get("url", url),
                "final_url": page.get("final_url", url),
                "title": title,
                "description": page.get("description", ""),
                "domain": page.get("domain", ""),
                "canonical_url": page.get("canonical_url", ""),
                "language": page.get("language", ""),
                "content": content,
                "analyzed_pages": analyzed_pages,
                "analyzed_page_count": analyzed_page_count,
                "page_success": page_success,
                "source_pages": source_pages,
                "crawl_query": page.get("crawl_query", page.get("query", query)),
                "headings": page.get("headings", []),
                "internal_links": page.get("internal_links", []),
                "external_links": page.get("external_links", []),
                "word_count": page.get("word_count", 0),
                "content_length": len(grounded_content),
                "status_code": page.get("status_code", 200),
                "content_type": page.get("content_type", ""),
                "strict_source": True,
                "combined_content": grounded_content,
                "retrieval_context": retrieved_context,
                "retrieval_result": retrieval,
                "retrieval_fallback_used": retrieval.get("fallback_used", False),
                "retrieved_resources": retrieval.get("results", []),
                "has_retrieved_evidence": retrieval.get("has_evidence", False),
                "resources": resources,
                "primary_resource": primary_resource,
            }

        except Exception as error:

            print("=" * 60)
            print("URL PROCESSING ERROR")
            print(error)
            print("=" * 60)

            return {
                "success": False,
                "url": url,
                "title": "",
                "content": "",
                "error": str(error),
            }

    # ======================================
    # Direct Website Navigation Detection
    # ======================================

    @staticmethod
    def _is_direct_navigation_request(prompt: str) -> bool:
        """
        Return True only when the user explicitly asks for a website
        destination/link/page/portal/form.
        """
        if not prompt:
            return False

        text = re.sub(r"\s+", " ", prompt.lower()).strip()

        navigation_patterns = (
            r"\blink\b",
            r"\blinks\b",
            r"\burl\b",
            r"\burls\b",
            r"\bwebpage\b",
            r"\bwebpages\b",
            r"\bpage\b",
            r"\bpages\b",
            r"\bwebsite\b.*\bpage\b",
            r"\bportal\b",
            r"\blogin\b",
            r"\bregistration\s+page\b",
            r"\bregistration\s+link\b",
            r"\bapplication\s+form\b",
            r"\bform\s+link\b",
            r"\bdownload\s+link\b",
            r"\bdownload\s+page\b",
            r"\bopen\s+(?:the\s+)?(?:page|link|portal|website)\b",
            r"\bshow\s+(?:me\s+)?(?:the\s+)?(?:page|link|portal|website)\b",
            r"\bgive\s+(?:me\s+)?(?:the\s+)?(?:page|link|url|portal)\b",
            r"\bfind\s+(?:me\s+)?(?:the\s+)?(?:page|link|url|portal)\b",
        )

        return any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in navigation_patterns
        )

    # ======================================
    # Main Process
    # ======================================

    @staticmethod
    def process(
        prompt: str,
        web_search: bool = False,
        uploaded_file=None,
        pdf_mode: bool = False,
        pdf_id: str = None,
        email: str = None,
        active_url: str = None,
        crawl_timeout: int = None,
    ) -> AIResponse:

        # ==================================
        # Validate prompt
        # ==================================

        prompt = (
            prompt or ""
        ).strip()

        if not prompt:

            return AIResponse(
                prompt="",
                intent="unknown",
                confidence=0.0,
                answer="Please enter a question.",
                execution_time="0s",
                success=False,
            )

        # ==================================
        # Step 1 : Reasoning
        # ==================================

        reasoning = ReasoningService.analyze(
            prompt
        )

        # ==================================
        # Dynamic Confidence Gating Intercept (C < 0.60)
        # ==================================

        if getattr(reasoning, "confidence", 1.0) < 0.60 and not pdf_mode and not uploaded_file and not active_url:
            clarification_msg = (
                "Your request appears ambiguous or lacks sufficient detail. "
                "Could you please clarify your objective or provide the exact entity or topic you are asking about?"
            )
            return AIResponse(
                prompt=prompt,
                intent=reasoning.intent,
                confidence=reasoning.confidence,
                answer=clarification_msg,
                execution_time="0.05s",
                success=True,
            )

        # ==================================
        # Step 2 : Tool Router
        # ==================================

        route = ToolRouterService.detect(
            prompt
        )

        # ==================================
        # Step 3 : Context
        # ==================================

        web_context = ""
        url_context = ""
        file_context = ""

        document_source = ""
        url_source = ""
        web_sources = []

        # ==================================
        # Step 4 : URL Detection
        # ==================================

        url_detected = False

        if active_url:

            active_url = (
                active_url.strip()
            )

            if active_url:

                url_source = active_url
                url_detected = True

        if not url_detected:

            detected_url = (
                AIOrchestrator._extract_url(
                    prompt
                )
            )

            if detected_url:

                url_source = detected_url
                url_detected = True

        # ==================================
        # Step 5 : Conversation Context
        # ==================================

        context = ContextService.build(
            prompt
        )

        # ==================================
        # Step 6 : Planner
        # ==================================

        plan = PlannerService.create(
            reasoning
        )

        # ==================================
        # Step 7 : Execution
        # ==================================

        execution = ExecutionService.execute(
            plan
        )

        # ==================================
        # Step 8 : PDF RAG
        # ==================================

        if pdf_mode:

            pdf_result = (
                AIOrchestrator._process_pdf(
                    prompt=prompt,
                    uploaded_file=uploaded_file,
                    pdf_mode=pdf_mode,
                    pdf_id=pdf_id,
                    email=email,
                )
            )

            if pdf_result is not None:

                pdf_answer = (
                    pdf_result.get(
                        "answer",
                        "",
                    )
                    or ""
                ).strip()

                pdf_sources = (
                    pdf_result.get(
                        "sources",
                        [],
                    )
                    or []
                )

                if pdf_result.get(
                    "success",
                    False,
                ):

                    source_text = ""

                    if pdf_sources:

                        source_text = (
                            "\n\n---\n"
                            "📄 **PDF Sources**\n"
                        )

                        for index, source in enumerate(
                            pdf_sources,
                            start=1,
                        ):

                            page = source.get(
                                "page",
                                source.get(
                                    "page_number",
                                    "",
                                ),
                            )

                            chunk = source.get(
                                "chunk",
                                source.get(
                                    "chunk_id",
                                    "",
                                ),
                            )

                            if page != "":
                                source_text += (
                                    f"- Source {index}: "
                                    f"Page {page}"
                                )
                            else:
                                source_text += (
                                    f"- Source {index}"
                                )

                            if chunk != "":
                                source_text += (
                                    f", Chunk {chunk}"
                                )

                            source_text += "\n"

                    final_pdf_answer = (
                        pdf_answer
                        + source_text
                    ).strip()

                    AIOrchestrator._persist_turn_safely(
                        email=email,
                        prompt=prompt,
                        answer=final_pdf_answer,
                        intent=reasoning.intent,
                        confidence=reasoning.confidence,
                        execution_time=execution.execution_time,
                    )

                    return AIResponse(
                        prompt=prompt,
                        intent=reasoning.intent,
                        confidence=reasoning.confidence,
                        answer=final_pdf_answer,
                        execution_time=(
                            execution.execution_time
                        ),
                        success=True,
                    )

                return AIResponse(
                    prompt=prompt,
                    intent=reasoning.intent,
                    confidence=reasoning.confidence,
                    answer=pdf_answer or (
                        "I could not generate an "
                        "answer from the PDF."
                    ),
                    execution_time=(
                        execution.execution_time
                    ),
                    success=False,
                )

        # ==================================
        # Step 9 : Normal Uploaded File
        # ==================================

        if uploaded_file is not None:

            (
                document_source,
                file_context,
            ) = AIOrchestrator._read_uploaded_file(
                uploaded_file
            )

        # ==================================
        # Step 10 : ADVANCED URL MODE
        # ==================================

        current_url = url_source

        if not current_url:

            current_url = (
                AIOrchestrator._extract_url(
                    prompt
                )
            )

        url_detected = bool(
            current_url
        )

        if url_detected:

            url_source = current_url

            url_result = (
                AIOrchestrator._process_url(
                    current_url,
                    query=prompt,
                    max_pages=None,
                    crawl_timeout=crawl_timeout,
                )
            )

            if url_result.get(
                "success",
                False,
            ):

                # ----------------------------------
                # DIRECT WEBSITE NAVIGATION MODE
                # ----------------------------------

                try:
                    is_navigation = (
                        AIOrchestrator._is_direct_navigation_request(
                            prompt
                        )
                    )
                except Exception as navigation_error:
                    print(
                        "Navigation detection error:",
                        navigation_error,
                    )
                    is_navigation = False

                if is_navigation:

                    try:
                        navigation_result = (
                            WebsiteRetrievalService.find_navigation_resource(
                                prompt,
                                url_result.get(
                                    "resources",
                                    [],
                                )
                                or url_result.get(
                                    "website_resources",
                                    [],
                                )
                                or [],
                            )
                        )
                    except Exception as navigation_error:
                        print(
                            "Navigation resource finder error:",
                            navigation_error,
                        )
                        navigation_result = {
                            "found": False,
                            "score": 0.0,
                            "title": "",
                            "url": "",
                        }

                    if navigation_result.get(
                        "found",
                        False,
                    ):

                        navigation_url = (
                            navigation_result.get(
                                "url",
                                "",
                            )
                            or ""
                        ).strip()

                        navigation_title = (
                            navigation_result.get(
                                "title",
                                "",
                            )
                            or ""
                        ).strip()

                        if navigation_url:

                            if navigation_title:
                                navigation_answer = (
                                    "I found the relevant page "
                                    "on the official website:\n\n"
                                    f"**{navigation_title}**\n\n"
                                    f"🔗 {navigation_url}"
                                )
                            else:
                                navigation_answer = (
                                    "I found the relevant page "
                                    "on the official website:\n\n"
                                    f"🔗 {navigation_url}"
                                )

                            print("=" * 60)
                            print("DIRECT WEBSITE NAVIGATION")
                            print("Question:", prompt)
                            print(
                                "Score:",
                                navigation_result.get(
                                    "score",
                                    0.0,
                                ),
                            )
                            print(
                                "Title:",
                                navigation_title,
                            )
                            print(
                                "URL:",
                                navigation_url,
                            )
                            print("=" * 60)

                            final_nav_answer = (
                                navigation_answer
                                + "\n\n"
                                + "🔗 **URL Source**\n"
                                + f"- {url_source}"
                            ).strip()

                            AIOrchestrator._persist_turn_safely(
                                email=email,
                                prompt=prompt,
                                answer=final_nav_answer,
                                intent=reasoning.intent,
                                confidence=reasoning.confidence,
                                execution_time=execution.execution_time,
                            )

                            return AIResponse(
                                prompt=prompt,
                                intent=reasoning.intent,
                                confidence=reasoning.confidence,
                                answer=final_nav_answer,
                                execution_time=(
                                    execution.execution_time
                                ),
                                success=True,
                            )

                headings_text = "\n".join(
                    url_result.get(
                        "headings",
                        [],
                    )
                )

                internal_links = (
                    url_result.get(
                        "internal_links",
                        [],
                    )
                    or []
                )

                internal_links_text = "\n".join(
                    (
                        item.get("url", "")
                        if isinstance(item, dict)
                        else str(item)
                    )
                    for item in internal_links
                    if (
                        isinstance(item, dict)
                        and item.get("url", "")
                    )
                    or (
                        not isinstance(item, dict)
                        and str(item).strip()
                    )
                )

                external_links = (
                    url_result.get(
                        "external_links",
                        [],
                    )
                    or []
                )

                external_links_text = "\n".join(
                    (
                        item.get("url", "")
                        if isinstance(item, dict)
                        else str(item)
                    )
                    for item in external_links
                    if (
                        isinstance(item, dict)
                        and item.get("url", "")
                    )
                    or (
                        not isinstance(item, dict)
                        and str(item).strip()
                    )
                )

                source_pages = (
                    url_result.get(
                        "source_pages",
                        [],
                    )
                    or []
                )

                source_pages_text = "\n".join(
                    (
                        item.get("url", "")
                        if isinstance(item, dict)
                        else str(item)
                    )
                    for item in source_pages
                    if (
                        isinstance(item, dict)
                        and item.get("url", "")
                    )
                    or (
                        not isinstance(item, dict)
                        and str(item).strip()
                    )
                )

                combined_content = (
                    url_result.get(
                        "combined_content",
                        "",
                    )
                    or ""
                ).strip()

                retrieved_resources = (
                    url_result.get(
                        "retrieved_resources",
                        [],
                    )
                    or []
                )

                has_retrieved_evidence = bool(
                    url_result.get(
                        "has_retrieved_evidence",
                        False,
                    )
                )

                retrieved_sources_text = "\n".join(
                    (
                        f"- {item.get('title', 'Untitled')} "
                        f"| {item.get('url', '')} "
                        f"| score={item.get('score', 0)}"
                    )
                    for item in retrieved_resources
                )

                if not combined_content:
                    combined_content = (
                        "No sufficiently relevant evidence "
                        "was found in the analyzed website "
                        "resources for this question."
                    )

                url_context = f"""
STRICT URL ANALYSIS

The user explicitly provided this URL:

URL:
{url_source}

Final URL:
{url_result.get("final_url", url_source)}

Website Title:
{url_result.get("title", "")}

Website Description:
{url_result.get("description", "")}

Website Domain:
{url_result.get("domain", "")}

Language:
{url_result.get("language", "")}

Canonical URL:
{url_result.get("canonical_url", "")}

User Question Used For Retrieval:
{prompt}

Analyzed Page Count:
{url_result.get("analyzed_page_count", 1)}

Discovered Resource Count:
{len(url_result.get("resources", []))}

Retrieved Relevant Resource Count:
{len(retrieved_resources)}

Relevant Evidence Found:
{has_retrieved_evidence}

Analyzed Source Pages:
{source_pages_text}

Retrieved Website Sources:
{retrieved_sources_text}

Primary Page Headings:
{headings_text}

Important Internal Links:
{internal_links_text}

External Links:
{external_links_text}

RETRIEVED WEBSITE CONTENT:
{combined_content}
"""

            else:

                url_source = current_url

                url_error = (
                    url_result.get(
                        "error",
                        "Unknown URL reading error.",
                    )
                    or "The provided URL could not be read."
                )

                url_context = f"""
STRICT URL SOURCE

URL:
{current_url}

The provided URL could not be read.

Reason:
{url_error}
"""

                try:
                    navigation_failed = (
                        WebsiteRetrievalService.is_navigation_query(
                            prompt
                        )
                    )
                except Exception:
                    navigation_failed = False

                if navigation_failed:
                    return AIResponse(
                        prompt=prompt,
                        intent=reasoning.intent,
                        confidence=reasoning.confidence,
                        answer=(
                            "I couldn't retrieve the requested page "
                            "from the provided website.\n\n"
                            f"Reason: {url_error}\n\n"
                            "🔗 **URL Source**\n"
                            f"- {url_source}"
                        ),
                        execution_time=execution.execution_time,
                        success=False,
                    )

        # ==================================
        # Step 11 : Web Search
        # ==================================

        if (
            (web_search or route.use_web)
            and not url_detected
        ):

            try:

                search = WebSearchService.search(
                    prompt,
                    max_results=5,
                )

                if search.get(
                    "success",
                    False,
                ):

                    web_context = (
                        "\nLATEST WEB SEARCH RESULTS\n"
                    )

                    for index, item in enumerate(
                        search.get(
                            "results",
                            [],
                        ),
                        start=1,
                    ):

                        title = (
                            item.get(
                                "title",
                                "",
                            )
                            or ""
                        )

                        source_url = (
                            item.get(
                                "url",
                                "",
                            )
                            or ""
                        )

                        snippet = (
                            item.get(
                                "snippet",
                                "",
                            )
                            or ""
                        )

                        if source_url:

                            web_sources.append(
                                {
                                    "title": title,
                                    "url": source_url,
                                }
                            )

                        web_context += (
                            f"\n{index}. "
                            f"{title}\n"
                            f"URL: {source_url}\n"
                            f"Summary: {snippet}\n"
                        )

                else:

                    web_context = (
                        "Web search was requested, "
                        "but no results were available."
                    )

            except Exception as e:

                web_context = (
                    "Web search could not be "
                    "completed.\n"
                    f"Reason: {str(e)}"
                )

        # ==================================
        # Step 12 : Source Context
        # ==================================

        source_context = ""

        if document_source:

            source_context += f"""
DOCUMENT SOURCE:
{document_source}

This is an uploaded file supplied directly
by the user.
"""

        if url_source:

            source_context += f"""
URL SOURCE:
{url_source}

This is the exact website URL supplied by
the user.

STRICT RULE:
Only the analyzed/retrieved information from
this supplied URL and its relevant same-domain
pages may be used for URL-grounded questions.
"""

        if web_sources:

            source_context += """
WEB SOURCES:
"""

            for index, source in enumerate(
                web_sources,
                start=1,
            ):

                source_context += (
                    f"{index}. "
                    f"{source['title']}\n"
                    f"   {source['url']}\n"
                )

        # ==================================
        # Step 13 : Grounding Rules
        # ==================================

        if url_detected:

            grounding_rules = """
STRICT URL-ONLY MODE

The user supplied a specific URL.

That URL and the relevant same-domain pages
selected by the URL analyzer are the SINGLE
SOURCE OF TRUTH.

You MUST:

1. Answer using ONLY retrieved content from
   the supplied URL and its selected same-domain
   pages.

2. Use the user's question to understand which
   retrieved page content is relevant.

3. Answer the exact question directly.

4. Use information only when supported by the
   retrieved URL evidence.

5. Do NOT use general knowledge to fill gaps.

6. Do NOT use DDGS or unrelated web-search
   results.

7. Do NOT use another domain.

8. Do NOT invent facts.

9. Do NOT infer unsupported information.

10. If the exact answer is not explicitly labeled, summarize the
    available relevant schedule, faculty, department, or related data found
    on the page rather than returning a blank rejection. Only say
    "I couldn't find that information in the provided URL" if the
    page is completely irrelevant to the domain.

11. Do not add unrelated information.

12. Do not cite sources other than the supplied
    URL and its analyzed same-domain pages.

The answer must be grounded entirely in the
retrieved URL evidence.
"""

        elif file_context:

            grounding_rules = """
UPLOADED FILE MODE

Use the uploaded file as the primary source
when the user's question concerns that file.

Do not invent information that is not supported
by the uploaded file.

If the requested information is not present,
say that it could not be found in the
uploaded file.
"""

        elif web_context:

            grounding_rules = """
WEB SEARCH MODE

Use the retrieved web search results for
current information.

Do not invent sources or URLs.

Keep source information separate from
general reasoning.
"""

        else:

            grounding_rules = """
NORMAL CHAT MODE

No external document or URL source is active.

Answer normally using your available knowledge.
"""

        # ==================================
        # Step 14 : AI Prompt
        # ==================================

        ai_prompt = f"""
You are NovaMind AI.

You are an intelligent AI assistant.

========================================
REASONING
========================================

Intent:
{reasoning.intent}

Confidence:
{reasoning.confidence}

Agent:
{reasoning.agent}

Available Tools:
{", ".join(reasoning.tools)}

========================================
EXECUTION PLAN
========================================

{", ".join(plan.steps)}

========================================
CONVERSATION CONTEXT
========================================

{context}

========================================
USER QUESTION
========================================

{prompt}

========================================
UPLOADED FILE CONTEXT
========================================

{file_context}

========================================
URL CONTEXT
========================================

{url_context}

========================================
WEB SEARCH CONTEXT
========================================

{web_context}

========================================
SOURCE INFORMATION
========================================

{source_context}

========================================
GROUNDING RULES
========================================

{grounding_rules}

========================================
ANSWER STYLE
========================================

- Answer the user's exact question.
- Be clear and professional.
- Use headings or bullet points when useful.
- Do not mention internal pipeline details.
- Do not mention unavailable tools unless
  necessary.
- Do not mix unrelated sources.
- Do not fabricate information.
"""

        # ==================================
        # Step 15 : Gemini
        # ==================================

        try:

            answer = AIOrchestrator._call_gemini_resilient(
                ai_prompt
            )

            answer = (
                answer
                if isinstance(answer, str)
                else str(answer)
            ).strip()

            if not answer:

                answer = (
                    "NovaMind AI did not receive "
                    "a readable response."
                )

            success = True

        except Exception as e:

            error_text = str(e)

            if (
                "503" in error_text
                or "UNAVAILABLE"
                in error_text.upper()
                or "high demand"
                in error_text.lower()
            ):

                answer = (
                    "Gemini is temporarily "
                    "unavailable because the model "
                    "is experiencing high demand. "
                    "Please try again shortly."
                )

            else:

                answer = (
                    "I could not generate the "
                    f"answer. Error: {error_text}"
                )

            success = False

        # ==================================
        # Step 16 : Source References
        # ==================================

        source_references = ""

        if document_source:

            source_references += (
                "\n\n---\n"
                "📄 **Document Source**\n"
                f"- `{document_source}`\n"
            )

        if url_detected and url_source:

            source_references += (
                "\n"
                "🔗 **URL Source**\n"
                f"- {url_source}\n"
            )

        elif web_sources:

            source_references += (
                "\n"
                "🌐 **Web Sources**\n"
            )

            for index, source in enumerate(
                web_sources,
                start=1,
            ):

                source_references += (
                    f"{index}. "
                    f"{source['title']}\n"
                    f"   {source['url']}\n"
                )

        if source_references:

            answer = (
                answer.strip()
                + source_references
            )

        # ==================================
        # MongoDB Turn State Persistence
        # ==================================

        AIOrchestrator._persist_turn_safely(
            email=email,
            prompt=prompt,
            answer=answer.strip(),
            intent=reasoning.intent,
            confidence=reasoning.confidence,
            execution_time=execution.execution_time,
        )

        # ==================================
        # Step 17 : Final Response
        # ==================================

        return AIResponse(
            prompt=prompt,
            intent=reasoning.intent,
            confidence=reasoning.confidence,
            answer=answer.strip(),
            execution_time=(
                execution.execution_time
            ),
            success=success,
        )