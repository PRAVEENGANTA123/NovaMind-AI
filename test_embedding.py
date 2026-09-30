from services.pdf.embedding_service import EmbeddingService

chunks = [

    "Artificial Intelligence is changing the world.",

    "Machine Learning is a subset of Artificial Intelligence.",

    "Python is widely used for AI development.",

]

embeddings = EmbeddingService.create_embeddings(chunks)

print("=" * 60)
print("TOTAL CHUNKS :", len(chunks))
print("EMBEDDINGS   :", len(embeddings))
print("VECTOR SIZE  :", len(embeddings[0]))
print("=" * 60)