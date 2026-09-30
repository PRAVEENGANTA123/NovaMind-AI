from services.ai.url_service import URLService

print("=" * 60)
print("NovaMind AI - URL Reader Test")
print("=" * 60)

url = "https://openai.com"

result = URLService.read(url)

if result["success"]:

    print("\nTitle:")
    print(result["title"])

    print("\nContent Preview:\n")
    print(result["content"][:1000])

else:

    print("Error:")
    print(result["error"])