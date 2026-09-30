"""
NovaMind AI - In-Memory Semantic URL RAG
Provides instant vector search across scraped webpage chunks.
"""

import numpy as np
from services.pdf.embedding_service import EmbeddingService


class URLSemanticRAG:
    @staticmethod
    def retrieve_relevant_chunks(combined_text: str, query: str, top_k: int = 4) -> str:
        if not combined_text or not query:
            return combined_text[:15000]

        # Chunk text into ~300-word blocks
        paragraphs = [p.strip() for p in combined_text.split("\n\n") if len(p.strip()) > 80]
        if not paragraphs or len(paragraphs) <= top_k:
            return combined_text[:25000]

        # Embed paragraphs and query
        chunk_embeddings = EmbeddingService.create_embeddings(paragraphs)
        query_embedding = EmbeddingService.create_embeddings([query])[0]

        # Compute Cosine Similarities
        scores = np.dot(chunk_embeddings, query_embedding) / (
            np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-9
        )
        
        top_indices = np.argsort(scores)[::-1][:top_k]
        top_chunks = [paragraphs[i] for i in top_indices]
        return "\n\n---\n\n".join(top_chunks)