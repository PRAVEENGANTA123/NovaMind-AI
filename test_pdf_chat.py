from services.pdf.pdf_chat_service import PDFChatService

chat = PDFChatService()

question = input("Ask: ")

result = chat.ask(question)

print("\n")

print("=" * 60)

print(result["answer"])

print("=" * 60)

print("\nSources\n")

for source in result["sources"]:

    print("-" * 40)

    print(source)