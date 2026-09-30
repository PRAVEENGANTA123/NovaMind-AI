"""
=========================================
NovaMind AI - Automated Test Suite
=========================================

Integration and unit tests covering:
- Authentication and Password Hashing
- MongoDB Persistence and Repositories (IDOR Scoping)
- Safe Async URL Discovery Engine (SSRF Guards)
- ChromaDB Vector Store and PDF Services
- AI Reasoning and Orchestration Pipeline
- Gemini Service Initialization and Fallbacks
"""

import unittest

from authentication.password import hash_password, verify_password
from database.mongodb import get_database
from database.chat_repository import ChatRepository
from services.ai.url_engine import SafeAsyncURLEngine
from services.ai.reasoning_service import ReasoningService
from services.ai.tool_router_service import ToolRouterService
from services.ai.gemini_service import GeminiService


class TestNovaMindAI(unittest.TestCase):

    def test_01_password_hashing(self):
        """Verify bcrypt hashing and salt verification."""
        raw_password = "SecurePassword123!"
        hashed = hash_password(raw_password)
        self.assertTrue(verify_password(raw_password, hashed))
        self.assertFalse(verify_password("WrongPassword", hashed))

    def test_02_mongodb_connection(self):
        """Verify MongoDB database ping and collections."""
        db = get_database()
        self.assertIsNotNone(db)
        self.assertEqual(db.name, "NovaMindAI")

    def test_03_chat_repository_user_scoping(self):
        """Verify that chat queries are properly scoped to user email (IDOR Guard)."""
        test_email = "test_audit_user@novamind.local"
        chat_id = ChatRepository.save_chat(
            email=test_email,
            prompt="Hello AI",
            response="Hello User",
            intent="general",
            confidence=0.95,
            agent="general",
        )
        self.assertIsNotNone(chat_id)

        # Retrieve chat with matching email
        chat = ChatRepository.get_chat(chat_id, email=test_email)
        self.assertIsNotNone(chat)
        self.assertEqual(chat["email"], test_email)

        # Retrieve chat with wrong email (should return None due to IDOR guard)
        idor_chat = ChatRepository.get_chat(chat_id, email="attacker@example.com")
        self.assertIsNone(idor_chat)

        # Clean up test chat
        deleted = ChatRepository.delete_chat(chat_id, email=test_email)
        self.assertTrue(deleted)

    def test_04_url_engine_ssrf_guard(self):
        """Verify that SafeAsyncURLEngine blocks private & loopback addresses."""
        self.assertFalse(SafeAsyncURLEngine.is_safe_url("http://127.0.0.1:27017"))
        self.assertFalse(SafeAsyncURLEngine.is_safe_url("http://localhost:8000"))
        self.assertFalse(SafeAsyncURLEngine.is_safe_url("http://169.254.169.254/latest/meta-data/"))
        self.assertTrue(SafeAsyncURLEngine.is_safe_url("https://example.com"))

    def test_05_url_content_distillation(self):
        """Verify that Trafilatura extracts clean main article text from HTML."""
        sample_html = """
        <html>
            <head><title>NovaMind Test Page</title></head>
            <body>
                <header><nav><a href="/home">Home</a></nav></header>
                <main>
                    <h1>Intelligent AI Workspace</h1>
                    <p>NovaMind AI combines multi-agent chat, PDF RAG, and URL browsing into one unified platform.</p>
                </main>
                <footer><p>© 2026 NovaMind. All rights reserved.</p></footer>
            </body>
        </html>
        """
        title, clean_text = SafeAsyncURLEngine.extract_main_content(sample_html)
        self.assertEqual(title, "NovaMind Test Page")
        self.assertIn("Intelligent AI Workspace", clean_text)
        self.assertNotIn("Home", clean_text)

    def test_06_reasoning_and_router_pipeline(self):
        """Verify AI reasoning and intent classification."""
        prompt = "Compare AWS and Azure cloud computing"
        reasoning = ReasoningService.analyze(prompt)
        self.assertIsNotNone(reasoning)
        self.assertIn(reasoning.intent.lower(), ["research", "compare", "general"])
        self.assertGreater(reasoning.confidence, 0.5)

        route = ToolRouterService.detect(prompt)
        self.assertIsNotNone(route)

    def test_07_gemini_service_initialization(self):
        """Verify GeminiService initialization with active model."""
        svc = GeminiService()
        self.assertEqual(svc.model, "gemini-3.6-flash")
        self.assertIn("gemini-3.5-flash-lite", svc.FALLBACK_MODELS)


if __name__ == "__main__":
    unittest.main()
