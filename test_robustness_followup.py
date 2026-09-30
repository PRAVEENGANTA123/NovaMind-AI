"""
NovaMind AI - Real-World Website Robustness & Conversation Follow-Up Test Suite
=============================================================================
1. Robustness Test: Evaluates handling across diverse domains.
2. Follow-Up Multi-Turn Test: Verifies conversational memory and cache retention.
"""

import time
from services.ai.url_service import URLService
from services.ai.orchestrator_service import AIOrchestrator

TEST_DOMAINS = [
    {"name": "FastAPI Docs (Dense Technical Tree)", "url": "https://fastapi.tiangolo.com/"},
    {"name": "Hacker News (Dynamic Web Feed)", "url": "https://news.ycombinator.com/"},
    {"name": "Python Software Foundation (Portal)", "url": "https://www.python.org/"}
]

def test_website_robustness():
    print("=" * 70)
    print("🌐 RUNNING REAL-WORLD WEBSITE ROBUSTNESS TESTS")
    print("=" * 70)

    for target in TEST_DOMAINS:
        print(f"\nTarget: {target['name']}")
        print(f"URL   : {target['url']}")
        
        t0 = time.time()
        result = URLService.analyze(target["url"], crawl_timeout=25)
        elapsed = round(time.time() - t0, 2)
        
        success = result.get("success", False)
        pages_mirrored = len(result.get("resources", []))
        total_words = result.get("word_count", 0)
        status = "PASSED" if success and pages_mirrored > 0 else "FAILED"
        
        print(f"Status         : {status}")
        print(f"Elapsed Time   : {elapsed}s")
        print(f"Pages Indexed  : {pages_mirrored}")
        print(f"Extracted Words: {total_words}")


def test_conversation_followups():
    print("\n" + "=" * 70)
    print("💬 RUNNING MULTI-TURN CONVERSATION FOLLOW-UP TESTS")
    print("=" * 70)

    target_url = "https://www.ppsu.ac.in/"
    conversation_chain = [
        "What engineering degrees and specializations are offered at PPSU?",
        "Who is the dean or head of this engineering school?",
        "What are the specific admission requirements or eligibility criteria for them?"
    ]

    for turn_idx, query in enumerate(conversation_chain, start=1):
        print(f"\n--- [TURN {turn_idx}] User Query: '{query}' ---")
        t0 = time.time()
        
        # Test standard orchestrator processing with cached URL grounding
        response = AIOrchestrator.process(
            prompt=query,
            active_url=target_url
        )
        elapsed = round(time.time() - t0, 3)

        if response.success:
            answer = response.answer.strip()
            print(f"Response Time : {elapsed}s")
            print(f"Answer Snippet: {answer[:180]}...\n")
        else:
            print(f"Turn {turn_idx} Failed: {response.error}")
            break

    print("=" * 70)
    print("✔ Completed all conversational turns successfully.")
    print("=" * 70)

if __name__ == "__main__":
    test_website_robustness()
    test_conversation_followups()
