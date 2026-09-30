"""
=========================================
NovaMind AI - Embedding Service
=========================================

Creates local embeddings for PDF chunks.

Model:
    all-MiniLM-L6-v2

Embedding Dimension:
    384

The model is loaded locally so the
application does not need network access
during normal runtime.
"""

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Local Embedding Service.

    Responsibilities:
        1. Load the local embedding model once.
        2. Create embeddings for text chunks.
        3. Provide the embedding dimension.
        4. Allow the cached model to be reset.
    """

    # =====================================
    # Configuration
    # =====================================

    MODEL_NAME = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    _model = None

    # =====================================
    # Load Model
    # =====================================

    @classmethod
    def get_model(cls):
        """
        Load the embedding model once.

        local_files_only=True prevents the
        application from contacting Hugging Face
        during runtime.
        """

        if cls._model is None:

            print("=" * 60)
            print("Loading Local Embedding Model...")
            print("=" * 60)

            try:

                cls._model = SentenceTransformer(
                    cls.MODEL_NAME,
                    local_files_only=True,
                )

                print(
                    "Local Embedding Model Loaded"
                )

                print(
                    "Embedding Dimension:",
                    cls._model.get_embedding_dimension(),
                )

                print("=" * 60)

            except Exception as e:

                cls._model = None

                print("=" * 60)
                print("EMBEDDING MODEL ERROR")
                print("=" * 60)
                print(e)
                print("=" * 60)

                raise RuntimeError(
                    "Local embedding model could not "
                    "be loaded. Make sure "
                    "all-MiniLM-L6-v2 is available "
                    "in the local Hugging Face cache."
                ) from e

        return cls._model

    # =====================================
    # Create Embeddings
    # =====================================

    @classmethod
    def create_embeddings(cls, chunks):
        """
        Convert text chunks into embeddings.

        Parameters
        ----------
        chunks : list[str] or str
            Text chunks to embed.

        Returns
        -------
        numpy.ndarray
            Embedding vectors.
        """

        if not chunks:

            raise ValueError(
                "No text chunks were provided "
                "for embedding."
            )

        # ---------------------------------
        # Accept a single string
        # ---------------------------------

        if isinstance(chunks, str):

            chunks = [chunks]

        # ---------------------------------
        # Validate input
        # ---------------------------------

        if not isinstance(
            chunks,
            (list, tuple),
        ):

            raise TypeError(
                "chunks must be a list or "
                "tuple of strings."
            )

        # ---------------------------------
        # Clean chunks
        # ---------------------------------

        cleaned_chunks = []

        for chunk in chunks:

            if chunk is None:
                continue

            chunk = str(chunk).strip()

            if chunk:

                cleaned_chunks.append(
                    chunk
                )

        if not cleaned_chunks:

            raise ValueError(
                "All provided chunks are empty."
            )

        # ---------------------------------
        # Load model
        # ---------------------------------

        model = cls.get_model()

        # ---------------------------------
        # Generate embeddings
        # ---------------------------------

        print(
            "Creating embeddings for "
            f"{len(cleaned_chunks)} chunk(s)..."
        )

        embeddings = model.encode(
            cleaned_chunks,
            show_progress_bar=True,
            convert_to_numpy=True,
        )

        print(
            "Embeddings created:",
            embeddings.shape,
        )

        return embeddings

    # =====================================
    # Get Embedding Dimension
    # =====================================

    @classmethod
    def get_dimension(cls):
        """
        Return the embedding vector dimension.
        """

        model = cls.get_model()

        return model.get_embedding_dimension()

    # =====================================
    # Reset Model
    # =====================================

    @classmethod
    def reset_model(cls):
        """
        Clear the cached embedding model.

        Useful during development/testing.
        """

        cls._model = None

        print(
            "Embedding model cache cleared."
        )