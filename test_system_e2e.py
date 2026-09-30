"""
NovaMind AI - Full System End-to-End (E2E) Test Suite
===================================================
Executes a comprehensive, full-lifecycle validation across all layers:
Database Persistence, Discovery Engines, Token Safety, LLM Grounding, and Document Export.
"""

import os
import sys
import time
from typing import Any, Dict

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def log_step(step_num: int, title: str):
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}[STEP {step_num}] {title}{Colors.ENDC}")
    print("=" * 70)


def log_success(message: str):
    print(f"{Colors.OKGREEN}✔ SUCCESS:{Colors.ENDC} {message}")


def log_failure(message: str):
    print(f"{Colors.FAIL}✖ FAILED:{Colors.ENDC} {message}")
    sys.exit(1)


def run_full_system_test():
    start_total_time = time.time()
    test_url = "https://example.com"
    test_domain = "example.com"
    test_query = "What is the primary purpose of this domain?"
    
    print(f"{Colors.HEADER}{Colors.BOLD}======================================================================{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}           NOVAMIND AI — FULL SYSTEM END-TO-END VERIFICATION          {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}======================================================================{Colors.ENDC}")

    # -------------------------------------------------------------
    # STEP 1: Database Connectivity Check
    # -------------------------------------------------------------
    log_step(1, "Testing MongoDB Connection & Repositories")
    try:
        from database.url_repository import URLRepository
        
        # Test query execution directly against MongoDB
        _ = URLRepository.get_cached_site("ping_test.com")
        log_success("Connected to MongoDB and queried 'NovaMindAI' repository successfully.")
    except Exception as e:
        log_failure(f"Database validation exception: {str(e)}")

    # -------------------------------------------------------------
    # STEP 2: Live Multi-Worker Scraper & MongoDB Ingestion
    # -------------------------------------------------------------
    log_step(2, "Testing Multi-Worker Python Scraper & Database Ingestion")
    try:
        from services.ai.url_service import URLService
        
        t0 = time.time()
        discovery_res = URLService.analyze(test_url, query=test_query)
        t_crawl = time.time() - t0

        if not discovery_res.get("success"):
            log_failure(f"URL Discovery failed on {test_url}: {discovery_res.get('error')}")
        
        resources = discovery_res.get("resources", [])
        log_success(f"Discovered {len(resources)} resources in {round(t_crawl, 3)}s.")

        # Verify record in MongoDB
        db_record = URLRepository.get_cached_site(test_domain)
        if not db_record or "data" not in db_record:
            log_failure("Crawled structure was not persisted into MongoDB 'cached_websites'.")
        log_success("Crawled document successfully persisted into MongoDB.")
    except Exception as e:
        log_failure(f"Scraping & Ingestion exception: {str(e)}")

    # -------------------------------------------------------------
    # STEP 3: Multi-Tier Cache Verification (RAM & DB Hits)
    # -------------------------------------------------------------
    log_step(3, "Testing Sub-Second Cache Retrieval (RAM + DB Hierarchy)")
    try:
        t0 = time.time()
        cached_res = URLService.analyze(test_url, query=test_query)
        t_cache = time.time() - t0

        if not cached_res.get("success"):
            log_failure("Cached retrieval returned success=False.")
        if t_cache > 0.5:
            log_failure(f"Cache response exceeded latency limit: {round(t_cache, 4)}s (Expected < 0.5s)")
        
        log_success(f"Cache resolved in {round(t_cache, 4)}s (< 0.5s threshold).")
    except Exception as e:
        log_failure(f"Cache hierarchy exception: {str(e)}")

    # -------------------------------------------------------------
    # STEP 4: HTTrack Desktop CLI Mirroring Engine
    # -------------------------------------------------------------
    log_step(4, "Testing HTTrack CLI Engine Mirroring")
    try:
        from services.ai.httrack_service import HTTrackService
        
        if not HTTrackService.is_httrack_available():
            print(f"{Colors.WARNING}⚠ WARNING:{Colors.ENDC} HTTrack binary not found. Skipping CLI test.")
        else:
            t0 = time.time()
            httrack_res = HTTrackService.mirror_site(test_url, depth=1, max_pages=3, timeout=30)
            t_httrack = time.time() - t0
            
            if not httrack_res.get("success"):
                log_failure(f"HTTrack execution failed: {httrack_res.get('error')}")
            
            pages_count = httrack_res.get("mirrored_pages", 0)
            log_success(f"HTTrack binary executed & mirrored {pages_count} pages in {round(t_httrack, 2)}s.")
    except Exception as e:
        log_failure(f"HTTrack service exception: {str(e)}")

    # -------------------------------------------------------------
    # STEP 5: Token Compactor & Gemini LLM Orchestration
    # -------------------------------------------------------------
    log_step(5, "Testing LLM Synthesis & Token Budgeting")
    try:
        from services.ai.orchestrator_service import AIOrchestrator
        
        t0 = time.time()
        orchestration_res = AIOrchestrator.process(
            prompt=test_query,
            active_url=test_url
        )
        t_ai = time.time() - t0

        if not orchestration_res.success:
            log_failure(f"AI Orchestration failed: {orchestration_res.error}")
        
        answer_text = orchestration_res.answer or ""
        if len(answer_text) < 20:
            log_failure("AI synthesized response is unexpectedly short or empty.")
        
        log_success(f"LLM Response synthesized in {round(t_ai, 2)}s.")
        print(f"\n{Colors.BOLD}AI Synthesis Preview:{Colors.ENDC}")
        print(f"\"{answer_text[:180].strip()}...\"\n")
    except Exception as e:
        log_failure(f"LLM Orchestration exception: {str(e)}")

    # -------------------------------------------------------------
    # STEP 6: Printable Document & Summary Generation
    # -------------------------------------------------------------
    log_step(6, "Testing Document Export Pipeline (Ctrl+P / Print View)")
    try:
        from services.ai.document_export_service import DocumentExportService
        
        html_report = DocumentExportService.generate_website_summary_document(
            url=test_url,
            title="Example Domain",
            domain=test_domain,
            query=test_query,
            ai_answer=orchestration_res.answer,
            resources=discovery_res.get("resources", [])
        )

        test_export_filename = "e2e_test_report.html"
        with open(test_export_filename, "w", encoding="utf-8") as f:
            f.write(html_report)
        
        if not os.path.exists(test_export_filename) or os.path.getsize(test_export_filename) == 0:
            log_failure("Report file was not created or is empty.")
        
        # Cleanup test artifact
        os.remove(test_export_filename)
        log_success("Document Export Pipeline generated valid HTML summary.")
    except Exception as e:
        log_failure(f"Document export exception: {str(e)}")

    # -------------------------------------------------------------
    # Summary of Execution
    # -------------------------------------------------------------
    total_elapsed = round(time.time() - start_total_time, 2)
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}{Colors.OKGREEN}🎉 FULL SYSTEM TEST PASSED SUCCESSFULLY IN {total_elapsed}s!{Colors.ENDC}")
    print("=" * 70)


if __name__ == "__main__":
    run_full_system_test()
