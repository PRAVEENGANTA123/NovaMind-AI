from services.ai.link_finder import WebsiteLinkFinder

def test_link_resolution():
    print("=" * 60)
    print("🧪 TESTING DIRECT LINK FINDER & NAVIGATION INTENT")
    print("=" * 60)

    # Simulated crawled resources
    mock_resources = [
        {"title": "RVR & JC College of Engineering - Home", "url": "https://rvrjcce.ac.in/"},
        {"title": "Examination Results Portal", "url": "https://rvrjcce.ac.in/examination-results.php"},
        {"title": "Hostel Fee Structure & Rules", "url": "https://rvrjcce.ac.in/facilities/hostels.php"},
        {"title": "Training & Placement Cell", "url": "https://rvrjcce.ac.in/placements/statistics.php"},
        {"title": "Contact Us & Campus Map", "url": "https://rvrjcce.ac.in/about/contact.php"},
        {"title": "Python 3.11 Documentation", "url": "https://docs.python.org/3/"},
        {"title": "Download Python Releases", "url": "https://www.python.org/downloads/"}
    ]

    queries = [
        "Where can I check the result? please give link",
        "how to see hostel fee structure",
        "give me the placement portal url",
        "What is Python used for?"
    ]

    for q in queries:
        is_nav = WebsiteLinkFinder.is_navigation_intent(q)
        links = WebsiteLinkFinder.find_direct_links(q, mock_resources, top_k=2) if is_nav else []
        
        print(f"\nQuery         : \"{q}\"")
        print(f"Nav Intent    : {'✅ TRUE' if is_nav else '❌ FALSE'}")
        if links:
            print("Matched Links :")
            for l in links:
                print(f"  - [{l['category']}] {l['title']} -> {l['url']} (Score: {l['score']})")
        else:
            print("Matched Links : None (Routes to standard RAG content chunking)")

    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_link_resolution()
    