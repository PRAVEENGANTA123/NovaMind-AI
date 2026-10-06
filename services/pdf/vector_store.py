"""
=========================================
NovaMind AI - Vector Store Service
=========================================

Stores and retrieves PDF embeddings
using ChromaDB.

Supports page-aware PDF metadata.
"""

import os
import chromadb


class VectorStoreService:
    """
    ChromaDB Vector Store Service.
    """

    def __init__(self):

        os.makedirs("database/chroma", exist_ok=True)

        self.client = chromadb.PersistentClient(
            path="database/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="novamind_pdf"
        )

    # =====================================
    # Store PDF
    # =====================================

    def add_pdf(
        self,
        pdf_id,
        chunks,
        embeddings,
        pages=None,
    ):
        """
        Store PDF chunks and embeddings.

        pages:
            Optional list containing the page number
            corresponding to every chunk.
        """

        try:

            # ---------------------------------
            # Validate
            # ---------------------------------

            if not chunks:

                return False

            if len(chunks) != len(embeddings):

                print(
                    "VECTOR STORE ERROR: "
                    "Chunks and embeddings count mismatch."
                )

                return False

            # ---------------------------------
            # Default page numbers
            # ---------------------------------

            if pages is None:

                pages = [0] * len(chunks)

            if len(pages) != len(chunks):

                print(
                    "VECTOR STORE ERROR: "
                    "Chunks and pages count mismatch."
                )

                return False

            # ---------------------------------
            # Create IDs and metadata
            # ---------------------------------

            ids = []

            metadatas = []

            for index, chunk in enumerate(chunks):

                ids.append(
                    f"{pdf_id}_{index}"
                )

                page_number = pages[index]

                # ChromaDB does not accept None
                if page_number is None:

                    page_number = 0

                metadatas.append(
                    {
                        "pdf_id": str(pdf_id),
                        "chunk": int(index),
                        "page": int(page_number),
                    }
                )

            # ---------------------------------
            # Normalize Embeddings
            # ---------------------------------

            if hasattr(embeddings, "tolist"):
                normalized_embeddings = embeddings.tolist()
            elif isinstance(embeddings, list):
                normalized_embeddings = [
                    e.tolist() if hasattr(e, "tolist") else e for e in embeddings
                ]
            else:
                normalized_embeddings = list(embeddings)

            # ---------------------------------
            # Store in ChromaDB
            # ---------------------------------

            self.collection.add(
                ids=ids,
                documents=chunks,
                embeddings=normalized_embeddings,
                metadatas=metadatas,
            )

            print("=" * 60)
            print("VECTOR STORE SUCCESS")
            print(f"PDF ID   : {pdf_id}")
            print(f"Chunks   : {len(chunks)}")
            print("=" * 60)

            return True

        except Exception as e:

            print("=" * 60)
            print("VECTOR STORE ERROR")
            print(e)
            print("=" * 60)

            return False

    # =====================================
    # Add Chunks Alias
    # =====================================

    def add_chunks(
        self,
        pdf_id,
        chunks,
        embeddings=None,
        metadatas=None,
        pages=None,
    ):
        """
        Backward-compatible alias for add_pdf.
        Automatically generates embeddings if omitted.
        """

        if embeddings is None:
            try:
                from services.pdf.embedding_service import EmbeddingService
                embeddings = EmbeddingService.create_embeddings(chunks)
            except Exception as emb_err:
                print(f"VECTOR STORE ERROR (Embedding generation failed): {emb_err}")
                return False

        if pages is None and metadatas:
            pages = [
                m.get("page", 0) if isinstance(m, dict) else 0
                for m in metadatas
            ]

        return self.add_pdf(
            pdf_id=pdf_id,
            chunks=chunks,
            embeddings=embeddings,
            pages=pages,
        )

    # =====================================
    # Search
    # =====================================

    def search(
        self,
        pdf_id,
        embedding,
        top_k=5,
    ):
        """
        Search only inside one PDF.
        """

        try:

            query_embedding_list = (
                embedding.tolist()
                if hasattr(embedding, "tolist")
                else list(embedding)
            )

            results = self.collection.query(
                query_embeddings=[
                    query_embedding_list
                ],
                n_results=top_k,
                where={
                    "pdf_id": str(pdf_id)
                },
            )

            documents = results.get(
                "documents",
                [[]],
            )[0]

            metadatas = results.get(
                "metadatas",
                [[]],
            )[0]

            distances = results.get(
                "distances",
                [[]],
            )[0]

            output = []

            for index, (doc, meta) in enumerate(
                zip(documents, metadatas)
            ):

                distance = None

                if index < len(distances):

                    distance = distances[index]

                output.append(
                    {
                        "text": doc,
                        "metadata": meta,
                        "distance": distance,
                    }
                )

            return output

        except Exception as e:

            print("=" * 60)
            print("VECTOR SEARCH ERROR")
            print(e)
            print("=" * 60)

            return []

    # =====================================
    # Delete PDF
    # =====================================

    def delete_pdf(
        self,
        pdf_id,
    ):
        """
        Delete all vectors belonging
        to one PDF.
        """

        try:

            self.collection.delete(
                where={
                    "pdf_id": str(pdf_id)
                }
            )

            print(
                f"Deleted vectors for PDF: {pdf_id}"
            )

            return True

        except Exception as e:

            print("=" * 60)
            print("VECTOR DELETE ERROR")
            print(e)
            print("=" * 60)

            return False

    # =====================================
    # Total Vectors
    # =====================================

    def total_vectors(self):
        """
        Return total vectors stored.
        """

        return self.collection.count()

    # =====================================
    # Collection Info
    # =====================================

    def collection_info(self):
        """
        Return collection statistics.
        """

        return {
            "name": self.collection.name,
            "vectors": self.collection.count(),
        }