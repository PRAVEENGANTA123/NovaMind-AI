from services.chat_service import ChatService

response = ChatService.ask(
    "praveen@gmail.com",
    "Explain Machine Learning in simple words."
)

print(response)

print("\nHistory:\n")

history = ChatService.history("praveen@gmail.com")

for chat in history:
    print(chat["question"])