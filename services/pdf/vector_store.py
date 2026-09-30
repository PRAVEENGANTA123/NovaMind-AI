"""
=========================================
NovaMind AI - Vector Store Service
=========================================

Stores and retrieves PDF embeddings
using ChromaDB.

Supports page-aware PDF metadata.
"""

import chromadb


class VectorStoreService:
    """
    ChromaDB Vector Store Service.
    """

    def __init__(self):

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
            # Store in ChromaDB
            # ---------------------------------

            self.collection.add(
                ids=ids,
                documents=chunks,
                embeddings=embeddings.tolist(),
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

            results = self.collection.query(
                query_embeddings=[
                    embedding.tolist()
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