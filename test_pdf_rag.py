from services.pdf.pdf_rag_service import PDFRAGService


rag = PDFRAGService()


result = rag.ask(
    pdf_id="UDP_REPORT_TEST_001",
    question="What is the future scope of this project?",
    top_k=5,
)


print()
print("=" * 70)
print("PDF RAG TEST")
print("=" * 70)

print("SUCCESS:", result["success"])

print()
print("ANSWER:")
print(result["answer"])

print()
print("SOURCES:")

for source in result["sources"]:

    print(
        f"Page {source['page']} "
        f"| Chunk {source['chunk']}"
    )

print("=" * 70)