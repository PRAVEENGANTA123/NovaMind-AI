"""
=====================================================
NovaMind AI - Live URL Scraper & AI Grounding Tester
=====================================================

Run this script to test any URL with the SafeAsyncURLEngine and AI Orchestrator:
    python test_url_flow.py
"""

import sys
from services.ai.url_engine import SafeAsyncURLEngine
from services.ai.orchestrator_service import AIOrchestrator

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def test_url(url: str, query: str = ""):
    print("\n" + "=" * 70)
    print(f"🌐 TESTING URL: {url}")
    print(f"❓ USER QUERY : {query or 'General Summary'}")
    print("=" * 70)

    print("\n[Step 1] Running SafeAsyncURLEngine...")
    scrape_result = SafeAsyncURLEngine.analyze(url, query=query)

    print(f"-> Success        : {scrape_result.get('success')}")
    print(f"-> Title          : {scrape_result.get('title')}")
    print(f"-> Analyzed Pages : {scrape_result.get('page_count', 0)}")
    print(f"-> Total Sources  : {len(scrape_result.get('sources', []))}")

    if not scrape_result.get("success"):
        print(f"❌ Scraping Notice: {scrape_result.get('error')}")
    else:
        print("\n📄 Extracted Content Preview (first 400 chars):")
        print("-" * 50)
        content_preview = scrape_result.get("content", "").strip()[:400]
        print(content_preview if content_preview else "[No main text body found]")
        print("-" * 50)

    print("\n[Step 2] Processing full prompt through AI Orchestrator...")
    prompt = f"{query} {url}".strip() if query else f"Summarize {url}"
    ai_response = AIOrchestrator.process(prompt)

    print("\n" + "=" * 70)
    print("🤖 NOVAMIND AI FINAL ANSWER:")
    print("=" * 70)
    print(ai_response.answer)
    print("=" * 70)


if __name__ == "__main__":
    test_target = sys.argv[1] if len(sys.argv) > 1 else "https://www.netflix.com/in/"
    test_question = sys.argv[2] if len(sys.argv) > 2 else "What new movies and shows are streaming?"

    test_url(test_target, test_question)
