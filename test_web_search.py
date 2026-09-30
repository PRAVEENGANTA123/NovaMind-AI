from services.ai.web_search_service import WebSearchService

print("=" * 60)
print("NovaMind AI - Web Search Test")
print("=" * 60)

response = WebSearchService.search(
    "Latest AI news",
    max_results=5,
)

if response["success"]:

    print("\nSearch Query :", response["query"])
    print("Results      :", response["count"])

    for i, result in enumerate(response["results"], start=1):

        print("\n" + "=" * 60)
        print(f"Result {i}")
        print("=" * 60)

        print("Title   :", result["title"])
        print("URL     :", result["url"])
        print("Snippet :", result["snippet"])

else:

    print("Search Failed")
    print(response["error"])