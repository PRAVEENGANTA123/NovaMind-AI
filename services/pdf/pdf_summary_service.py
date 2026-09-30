"""
=========================================
NovaMind AI - PDF Summary Service
=========================================

Generates AI summaries for PDFs.
"""

from langchain_google_genai import ChatGoogleGenerativeAI

from services.pdf.retriever import RetrieverService


class PDFSummaryService:
    """
    Generate AI summaries for PDFs.
    """

    def __init__(self):

        self.retriever = RetrieverService()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.2,
        )

    # =====================================
    # Generate Summary
    # =====================================

    def summarize(
        self,
        pdf_id: str,
    ):
        """
        Generate an AI summary.
        """

        try:

            sources = self.retriever.search(
                pdf_id=pdf_id,
                query="Summarize the entire document.",
                top_k=20,
            )

            if not sources:

                return {
                    "success": False,
                    "summary": "No content found.",
                }

            context = "\n\n".join(
                source["text"]
                for source in sources
            )

            prompt = f"""
You are NovaMind AI.

Create a professional summary.

Use this structure:

# Executive Summary

# Key Points

# Important Definitions

# Technologies Mentioned

# Conclusion

Document:

{context}
"""

            response = self.llm.invoke(prompt)

            return {

                "success": True,

                "summary": response.content,

            }

        except Exception as e:

            return {

                "success": False,

                "summary": str(e),

            }