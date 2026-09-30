from services.pdf.retriever import RetrieverService


retriever = RetrieverService()


results = retriever.search(
    pdf_id="UDP_REPORT_TEST_001",
    query="What is the future scope of this project?",
    top_k=5,
)


print()
print("=" * 70)
print("RETRIEVAL TEST")
print("=" * 70)
print("RESULTS:", len(results))
print("=" * 70)


for index, result in enumerate(results, start=1):


    metadata = result["metadata"]

    print()
    print(f"RESULT {index}")
    print(f"PAGE     : {metadata['page']}")
    print(f"CHUNK    : {metadata['chunk']}")
    print(f"DISTANCE : {result['distance']}")
    print()
    print(result["text"][:1000])
    print("-" * 70)