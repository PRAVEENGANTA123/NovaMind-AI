import os
import unittest
import time

from database.url_repository import URLRepository
from services.ai.url_service import URLService
from services.ai.httrack_service import HTTrackService
from services.ai.orchestrator_service import AIOrchestrator
from services.ai.document_export_service import DocumentExportService


class TestNovaMindIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_domain = "example.com"
        cls.test_url = "https://example.com"

    def test_01_crawler_to_mongodb_ingestion(self):
        """Verify URLService writes results directly to MongoDB repository."""
        # 1. Fetch via URL discovery
        res = URLService.analyze(self.test_url, query="test domain")
        self.assertTrue(res.get("success"), "URL discovery failed.")
        
        # 2. Verify record exists in MongoDB
        db_record = URLRepository.get_cached_site(self.test_domain)
        self.assertIsNotNone(db_record, "Data was not persisted to MongoDB.")
        self.assertIn("data", db_record, "MongoDB record missing 'data' key.")
        self.assertGreaterEqual(len(db_record["data"].get("resources", [])), 1)

    def test_02_database_caching_speed(self):
        """Verify second access loads from cache with low latency."""
        t0 = time.time()
        cached_res = URLService.analyze(self.test_url)
        elapsed = time.time() - t0

        self.assertTrue(cached_res.get("success"))
        # Cache access should be near instantaneous (< 0.5s)
        self.assertLess(elapsed, 0.5, f"Cache retrieval too slow: {elapsed}s")

    def test_03_httrack_cli_mirror_integration(self):
        """Verify HTTrack CLI interacts properly with the local system."""
        if not HTTrackService.is_httrack_available():
            self.skipTest("HTTrack binary not available on system.")

        result = HTTrackService.mirror_site(self.test_url, depth=1, max_pages=2, timeout=30)
        self.assertTrue(result.get("success"), "HTTrack execution failed.")
        self.assertGreaterEqual(result.get("mirrored_pages", 0), 1)
        self.assertTrue(len(result.get("resources", [])) > 0)

    def test_04_ai_orchestration_grounding(self):
        """Verify AI Orchestrator receives URL context and returns a grounded response."""
        res = AIOrchestrator.process(
            prompt="What is this website about?",
            active_url=self.test_url
        )
        self.assertTrue(res.success, f"Orchestration failed: {getattr(res, 'error', '')}")
        self.assertIsNotNone(res.answer)
        self.assertGreater(len(res.answer), 20)

    def test_05_document_export_pipeline(self):
        """Verify cached data can be exported into a valid printable HTML document."""
        cached = URLRepository.get_cached_site(self.test_domain)
        self.assertIsNotNone(cached)
        
        data = cached.get("data", {})
        html_doc = DocumentExportService.generate_website_summary_document(
            url=self.test_url,
            title=data.get("title", "Test"),
            domain=self.test_domain,
            query="Domain verification",
            ai_answer="This domain is for use in illustrative examples.",
            resources=data.get("resources", [])
        )

        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("example.com", html_doc)

        output_file = "test_output_report.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_doc)
        
        self.assertTrue(os.path.exists(output_file))
        if os.path.exists(output_file):
            os.remove(output_file)


if __name__ == "__main__":
    unittest.main(verbosity=2)
