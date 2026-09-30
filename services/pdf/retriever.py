"""
=========================================
NovaMind AI - PDF Retriever Service
=========================================

Hybrid PDF retrieval using:

1. Semantic vector similarity
2. Keyword matching
3. Page metadata

This improves retrieval accuracy for
OCR-generated PDF documents.
"""

import re

from services.pdf.embedding_service import EmbeddingService
from services.pdf.vector_store import VectorStoreService


class RetrieverService:
    """
    Retrieve relevant chunks for one PDF.
    """

    def __init__(self):

        self.vector_db = VectorStoreService()

    # =====================================
    # Normalize Text
    # =====================================

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize text for keyword matching.
        """

        if not text:

            return ""

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # =====================================
    # Extract Keywords
    # =====================================

    @classmethod
    def _keywords(cls, query: str):
        """
        Extract meaningful keywords from query.
        """

        stop_words = {
            "what",
            "is",
            "are",
            "the",
            "a",
            "an",
            "of",
            "this",
            "that",
            "for",
            "to",
            "in",
            "on",
            "and",
            "or",
            "with",
            "from",
            "does",
            "do",
            "how",
            "why",
            "which",
            "who",
        }

        normalized = cls._normalize(
            query
        )

        words = normalized.split()

        return [
            word
            for word in words
            if word not in stop_words
            and len(word) > 2
        ]

    # =====================================
    # Keyword Score
    # =====================================

    @classmethod
    def _keyword_score(
        cls,
        query: str,
        text: str,
    ):
        """
        Calculate keyword overlap score.
        """

        keywords = cls._keywords(
            query
        )

        if not keywords:

            return 0.0

        normalized_text = cls._normalize(
            text
        )

        matches = 0

        for keyword in keywords:

            if keyword in normalized_text:

                matches += 1

        return matches / len(keywords)

    # =====================================
    # Search
    # =====================================

    def search(
        self,
        pdf_id: str,
        query: str,
        top_k: int = 4,
    ):
        """
        Hybrid retrieval.

        First retrieves semantic candidates
        from ChromaDB, then re-ranks them
        using keyword overlap.
        """

        try:

            # ---------------------------------
            # Validate
            # ---------------------------------

            if not pdf_id:

                print(
                    "RETRIEVER ERROR: PDF ID is required."
                )

                return []

            if not query or not query.strip():

                print(
                    "RETRIEVER ERROR: Query is empty."
                )

                return []

            # ---------------------------------
            # Query embedding
            # ---------------------------------

            embedding = (
                EmbeddingService.create_embeddings(
                    [query]
                )[0]
            )

            # ---------------------------------
            # Retrieve more candidates
            # ---------------------------------

            candidate_count = max(
                top_k * 3,
                10,
            )

            results = self.vector_db.search(
                pdf_id=pdf_id,
                embedding=embedding,
                top_k=candidate_count,
            )

            if not results:

                print(
                    "RETRIEVER: No matching chunks found."
                )

                return []

            # ---------------------------------
            # Re-rank results
            # ---------------------------------

            ranked = []

            for result in results:

                if not isinstance(
                    result,
                    dict,
                ):

                    continue

                text = result.get(
                    "text",
                    "",
                )

                metadata = result.get(
                    "metadata",
                    {},
                )

                distance = result.get(
                    "distance",
                    999.0,
                )

                if not text:

                    continue

                if not isinstance(
                    metadata,
                    dict,
                ):

                    metadata = {}

                # -----------------------------
                # Keyword matching
                # -----------------------------

                keyword_score = (
                    self._keyword_score(
                        query,
                        text,
                    )
                )

                # -----------------------------
                # Semantic score
                #
                # Lower distance is better.
                # Convert it into a simple
                # similarity-like score.
                # -----------------------------

                semantic_score = (
                    1.0 / (1.0 + float(distance))
                )

                # -----------------------------
                # Combined score
                # -----------------------------

                combined_score = (
                    semantic_score * 0.60
                    +
                    keyword_score * 0.40
                )

                ranked.append(
                    {
                        "text": text,
                        "metadata": {
                            "pdf_id": metadata.get(
                                "pdf_id",
                                str(pdf_id),
                            ),
                            "chunk": int(
                                metadata.get(
                                    "chunk",
                                    0,
                                )
                            ),
                            "page": int(
                                metadata.get(
                                    "page",
                                    0,
                                )
                            ),
                        },
                        "distance": distance,
                        "keyword_score": keyword_score,
                        "semantic_score": semantic_score,
                        "score": combined_score,
                    }
                )

            # ---------------------------------
            # Sort
            # ---------------------------------

            ranked.sort(
                key=lambda item: item["score"],
                reverse=True,
            )

            output = ranked[:top_k]

            # ---------------------------------
            # Debug
            # ---------------------------------

            print("=" * 60)
            print("HYBRID PDF RETRIEVER")
            print(f"PDF ID     : {pdf_id}")
            print(f"Query      : {query}")
            print(
                f"Candidates : {len(ranked)}"
            )
            print(
                f"Results    : {len(output)}"
            )
            print("=" * 60)

            for index, item in enumerate(
                output,
                start=1,
            ):

                print(
                    f"{index}. "
                    f"Page={item['metadata']['page']} "
                    f"Chunk={item['metadata']['chunk']} "
                    f"Distance={item['distance']:.4f} "
                    f"Keyword={item['keyword_score']:.4f} "
                    f"Score={item['score']:.4f}"
                )

            return output

        except Exception as e:

            print("=" * 60)
            print("RETRIEVER ERROR")
            print("=" * 60)
            print(e)
            print("=" * 60)

            return []