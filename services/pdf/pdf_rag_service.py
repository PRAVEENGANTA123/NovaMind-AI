"""
=========================================
NovaMind AI - PDF RAG Service
=========================================

Retrieval-Augmented Generation for PDFs.

Flow:

User Question
      ↓
Retriever
      ↓
Relevant PDF Chunks
      ↓
Context Builder
      ↓
Gemini
      ↓
Answer + Sources
"""

from services.pdf.retriever import RetrieverService
from services.ai.gemini_service import GeminiService


class PDFRAGService:
    """
    PDF Retrieval-Augmented Generation service.
    """

    def __init__(self):

        self.retriever = RetrieverService()
        self.gemini = GeminiService()

    # =====================================
    # Build Context
    # =====================================

    @staticmethod
    def build_context(results):
        """
        Convert retrieved PDF chunks into
        a clean context for Gemini.
        """

        if not results:

            return ""

        context_parts = []

        for index, result in enumerate(
            results,
            start=1,
        ):

            text = result.get(
                "text",
                "",
            )

            metadata = result.get(
                "metadata",
                {},
            )

            page = metadata.get(
                "page",
                0,
            )

            chunk = metadata.get(
                "chunk",
                0,
            )

            if not text:

                continue

            context_parts.append(
                f"""
--- SOURCE {index} ---
Page: {page}
Chunk: {chunk}

{text}
"""
            )

        return "\n".join(
            context_parts
        )

    # =====================================
    # Ask PDF
    # =====================================

    def ask(
        self,
        pdf_id: str,
        question: str,
        top_k: int = 5,
    ):
        """
        Ask a question about one PDF.

        Returns:

        {
            "success": True,
            "answer": "...",
            "sources": [...],
            "retrieved_chunks": [...]
        }
        """

        try:

            # ---------------------------------
            # Validate question
            # ---------------------------------

            if not question or not question.strip():

                return {
                    "success": False,
                    "answer": (
                        "Please enter a question."
                    ),
                    "sources": [],
                    "retrieved_chunks": [],
                }

            # ---------------------------------
            # Retrieve relevant chunks
            # ---------------------------------

            results = self.retriever.search(
                pdf_id=pdf_id,
                query=question,
                top_k=top_k,
            )

            if not results:

                return {
                    "success": False,
                    "answer": (
                        "I could not find relevant "
                        "information in the uploaded PDF."
                    ),
                    "sources": [],
                    "retrieved_chunks": [],
                }

            # ---------------------------------
            # Build PDF context
            # ---------------------------------

            context = self.build_context(
                results
            )

            if not context.strip():

                return {
                    "success": False,
                    "answer": (
                        "No readable information "
                        "was retrieved from the PDF."
                    ),
                    "sources": [],
                    "retrieved_chunks": [],
                }

            # ---------------------------------
            # Gemini prompt
            # ---------------------------------

            prompt = f"""
You are NovaMind AI, a document question-answering assistant.

Answer the user's question using ONLY the information
provided in the PDF context below.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the answer is not supported by the PDF context,
   clearly say that the information was not found
   in the uploaded document.
4. Give a clear and simple answer.
5. When useful, organize the answer using numbered
   points or bullet points.
6. Do not mention the retrieval system, embeddings,
   ChromaDB, or internal implementation details.
7. Preserve the meaning of the original document.

USER QUESTION:
{question}

PDF CONTEXT:
{context}

Now answer the user's question.
"""

            # ---------------------------------
            # Generate answer
            # ---------------------------------

            answer = self.gemini.generate(
                prompt
            )

            # ---------------------------------
            # Build source list
            # ---------------------------------

            sources = []

            seen_pages = set()

            for result in results:

                metadata = result.get(
                    "metadata",
                    {},
                )

                page = metadata.get(
                    "page",
                    0,
                )

                if page not in seen_pages:

                    seen_pages.add(page)

                    sources.append(
                        {
                            "page": page,
                            "chunk": metadata.get(
                                "chunk",
                                0,
                            ),
                        }
                    )

            # ---------------------------------
            # Return
            # ---------------------------------

            return {
                "success": True,
                "answer": answer,
                "sources": sources,
                "retrieved_chunks": results,
            }

        except Exception as e:

            print("=" * 60)
            print("PDF RAG ERROR")
            print("=" * 60)
            print(e)
            print("=" * 60)

            return {
                "success": False,
                "answer": (
                    f"PDF analysis failed: {str(e)}"
                ),
                "sources": [],
                "retrieved_chunks": [],
            }