"""
Integration tests for FastAPI endpoints using unittest
"""
import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    def test_roles_endpoint(self):
        response = self.client.get("/api/roles")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(len(data["roles"]), 5)

    def test_analyze_endpoint(self):
        payload = {
            "resume_text": "Alex Dev. alex@dev.io. (555) 382-9102. 6 years experience in Python, React, Docker, FastAPI, PostgreSQL.",
            "target_role": "Senior Full Stack Developer"
        }
        response = self.client.post("/api/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("fit_analysis", data)
        self.assertIn("salary_prediction", data)
        self.assertIn("recommendations", data)

    def test_export_pdf_endpoint(self):
        payload = {
            "resume_text": "Alex Dev. alex@dev.io. 6 years experience in Python, React, Docker, FastAPI, PostgreSQL.",
            "target_role": "Senior Full Stack Developer"
        }
        analyze_resp = self.client.post("/api/analyze", json=payload)
        self.assertEqual(analyze_resp.status_code, 200)
        
        pdf_resp = self.client.post("/api/export-pdf", json=analyze_resp.json())
        self.assertEqual(pdf_resp.status_code, 200)
        self.assertEqual(pdf_resp.headers["content-type"], "application/pdf")
        self.assertGreater(len(pdf_resp.content), 1000)

    def test_hindi_api_and_pdf(self):
        payload = {
            "resume_text": "अमित शर्मा। ईमेल: amit@dev.in। 3 साल का अनुभव। कौशल: पायथन, रिएक्ट, डॉकर, फास्टएपीआई।",
            "target_role": "Senior Full Stack Developer",
            "language": "hi"
        }
        analyze_resp = self.client.post("/api/analyze", json=payload)
        self.assertEqual(analyze_resp.status_code, 200)
        data = analyze_resp.json()
        self.assertEqual(data["detected_language"], "hi")
        
        pdf_resp = self.client.post("/api/export-pdf", json=data)
        self.assertEqual(pdf_resp.status_code, 200)
        self.assertEqual(pdf_resp.headers["content-type"], "application/pdf")
        self.assertGreater(len(pdf_resp.content), 1000)

if __name__ == "__main__":
    unittest.main()
