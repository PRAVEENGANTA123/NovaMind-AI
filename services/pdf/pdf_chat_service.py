"""
=========================================
NovaMind AI - PDF Chat Service
=========================================

Retrieval-Augmented Generation (RAG)

Question
    ↓
Hybrid Retriever
    ↓
Relevant PDF Chunks
    ↓
Gemini
    ↓
Answer + Sources
"""

import os
import time

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from services.pdf.retriever import RetrieverService


# =========================================
# Load Environment
# =========================================

load_dotenv()


class PDFChatService:
    """
    AI Chat Service for PDF Question Answering.
    """

    # =========================================
    # Configuration
    # =========================================

    MODEL_NAME = "gemini-3.5-flash"

    MAX_RETRIES = 3

    RETRY_DELAY = 3

    # =========================================
    # Initialize
    # =========================================

    def __init__(self):

        self.retriever = RetrieverService()

        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:

            raise ValueError(
                "GOOGLE_API_KEY not found."
            )

        self.api_key = api_key

        self.llm = ChatGoogleGenerativeAI(
            model=self.MODEL_NAME,
            temperature=0.2,
            google_api_key=api_key,
        )

    # =========================================
    # Normalize Gemini Response
    # =========================================

    @staticmethod
    def _normalize_response(content) -> str:
        """
        Convert Gemini/LangChain response content
        into a normal string.
        """

        if content is None:
            return ""

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, str):

                    text_parts.append(item)

                elif isinstance(item, dict):

                    text = item.get("text")

                    if text:
                        text_parts.append(
                            str(text)
                        )

            return "\n".join(
                text_parts
            ).strip()

        if isinstance(content, dict):

            text = content.get("text")

            if text:
                return str(text).strip()

        return str(content).strip()

    # =========================================
    # Generate Gemini Response
    # =========================================

    def _generate_answer(
        self,
        prompt: str,
    ):
        """
        Generate an answer with retry handling.

        Temporary Gemini 503/UNAVAILABLE errors
        are retried automatically.
        """

        last_error = None

        for attempt in range(
            1,
            self.MAX_RETRIES + 1,
        ):

            try:

                print("=" * 60)
                print("GEMINI PDF GENERATION")
                print(
                    f"Model   : {self.MODEL_NAME}"
                )
                print(
                    f"Attempt : {attempt}/{self.MAX_RETRIES}"
                )
                print("=" * 60)

                response = self.llm.invoke(
                    prompt
                )

                answer = (
                    self._normalize_response(
                        response.content
                    )
                )

                if answer:

                    return {
                        "success": True,
                        "answer": answer,
                    }

                last_error = (
                    "Gemini returned an empty response."
                )

            except Exception as e:

                last_error = e

                error_text = str(e)

                print("=" * 60)
                print("GEMINI PDF GENERATION ERROR")
                print(error_text)
                print("=" * 60)

                # ---------------------------------
                # Retry temporary server errors
                # ---------------------------------

                temporary_error = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                    or "high demand" in error_text.lower()
                )

                if not temporary_error:

                    break

                if attempt < self.MAX_RETRIES:

                    print(
                        f"Retrying Gemini in "
                        f"{self.RETRY_DELAY} seconds..."
                    )

                    time.sleep(
                        self.RETRY_DELAY
                    )

        # -------------------------------------
        # All attempts failed
        # -------------------------------------

        return {
            "success": False,
            "answer": (
                "Gemini is temporarily unavailable. "
                "The PDF was successfully retrieved, "
                "but the AI response could not be "
                "generated right now. Please try again "
                "in a moment."
            ),
            "error": str(last_error),
        }

    # =========================================
    # Ask Question
    # =========================================

    def ask(
        self,
        pdf_id: str,
        question: str,
        top_k: int = 4,
    ):
        """
        Ask a question about a selected PDF.
        """

        try:

            # ---------------------------------
            # Validate Input
            # ---------------------------------

            if not pdf_id:

                return {
                    "success": False,
                    "answer": "PDF ID is required.",
                    "sources": [],
                }

            if not question or not question.strip():

                return {
                    "success": False,
                    "answer": "Please enter a question.",
                    "sources": [],
                }

            question = question.strip()

            # ---------------------------------
            # Retrieve Relevant Chunks
            # ---------------------------------

            sources = self.retriever.search(
                pdf_id=pdf_id,
                query=question,
                top_k=top_k,
            )

            if not sources:

                return {
                    "success": False,
                    "answer": (
                        "I couldn't find any relevant "
                        "information in the uploaded PDF."
                    ),
                    "sources": [],
                }

            # ---------------------------------
            # Build PDF Context
            # ---------------------------------

            context_parts = []

            for source in sources:

                text = source.get(
                    "text",
                    "",
                ).strip()

                if text:

                    context_parts.append(text)

            context = "\n\n".join(
                context_parts
            )

            if not context:

                return {
                    "success": False,
                    "answer": (
                        "I couldn't find any readable "
                        "content in the uploaded PDF."
                    ),
                    "sources": sources,
                }

            # ---------------------------------
            # Prompt
            # ---------------------------------

            prompt = f"""
You are NovaMind AI.

You are an intelligent PDF assistant.

Answer the user's question using ONLY
the information contained in the PDF context.

Rules:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not present in the PDF,
   say exactly:

"I couldn't find that information
in the uploaded PDF."

4. Answer clearly and professionally.
5. Use bullet points when appropriate.
6. Keep the answer concise unless
   the user asks for details.
7. Base the answer only on the supplied
   PDF context.

=========================================
PDF CONTEXT
=========================================

{context}

=========================================
USER QUESTION
=========================================

{question}

=========================================
ANSWER
=========================================
"""

            # ---------------------------------
            # Generate Response
            # ---------------------------------

            generation = self._generate_answer(
                prompt
            )

            # ---------------------------------
            # Gemini temporarily unavailable
            # ---------------------------------

            if not generation["success"]:

                return {
                    "success": False,
                    "answer": generation["answer"],
                    "sources": sources,
                }

            answer = generation["answer"]

            # ---------------------------------
            # Final Result
            # ---------------------------------

            return {
                "success": True,
                "answer": answer,
                "sources": sources,
            }

        except Exception as e:

            print("=" * 60)
            print("PDF CHAT ERROR")
            print("=" * 60)
            print(e)
            print("=" * 60)

            return {
                "success": False,
                "answer": (
                    "I could not generate an answer "
                    "from the PDF."
                ),
                "sources": [],
            }