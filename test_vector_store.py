from services.pdf.embedding_service import EmbeddingService
from services.pdf.vector_store import VectorStoreService

chunks = [
    "Artificial Intelligence is changing the world.",
    "Machine Learning is a subset of Artificial Intelligence.",
    "Python is widely used for AI development."
]

embeddings = EmbeddingService.create_embeddings(chunks)

db = VectorStoreService()

db.add_pdf(
    pdf_id="demo_pdf",
    chunks=chunks,
    embeddings=embeddings,
)

print("✅ Stored in ChromaDB")