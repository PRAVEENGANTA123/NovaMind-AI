from database.chats import save_chat, get_chat_history

save_chat(
    "praveen@gmail.com",
    "Hello",
    "Hi Praveen!"
)

history = get_chat_history("praveen@gmail.com")

print(history)