"""
Unit tests for NLP and ML components using Python unittest
"""
import unittest
from app.nlp.preprocessor import clean_text, tokenize
from app.nlp.entity_extractor import extractor
from app.nlp.tfidf_engine import compute_similarity
from app.nlp.salary_predictor import salary_model
from app.services.analyzer_service import analyzer_service

class TestAnalyzer(unittest.TestCase):
    def test_clean_text(self):
        raw = "Senior Dev • Python, C++, Docker... \n\n fast-paced."
        cleaned = clean_text(raw)
        self.assertIn("Python", cleaned)
        self.assertIn("C++", cleaned)
        self.assertNotIn("•", cleaned)

    def test_entity_extraction(self):
        sample_text = """
        John Doe
        john.doe@example.com | (555) 123-4567
        LinkedIn: linkedin.com/in/johndoe
        
        5+ years of experience in backend development.
        Bachelor of Science in Computer Science.
        
        Skills: Python, FastAPI, Docker, PostgreSQL, Kubernetes, Redis, AWS.
        """
        profile = extractor.extract_all(sample_text)
        
        self.assertEqual(profile["candidate_name"], "John Doe")
        self.assertEqual(profile["contact_info"]["email"], "john.doe@example.com")
        self.assertTrue(any("Bachelor" in edu for edu in profile["education"]))
        self.assertGreaterEqual(profile["experience"]["estimated_years"], 5.0)
        
        skills = profile["skills"]["all_skills"]
        self.assertIn("python", skills)
        self.assertIn("fastapi", skills)
        self.assertIn("docker", skills)
        self.assertIn("postgresql", skills)

    def test_tfidf_similarity(self):
        doc1 = "Python developer building machine learning models with PyTorch and Pandas."
        doc2 = "Seeking a Python machine learning engineer experienced in PyTorch and deep learning."
        res = compute_similarity(doc1, doc2)
        
        self.assertGreater(res["similarity_score"], 0.20)
        self.assertGreater(res["percentage"], 20.0)

    def test_salary_prediction(self):
        res = salary_model.predict_salary(
            role_name="Senior Full Stack Developer",
            matched_skills=["React", "TypeScript", "FastAPI", "Docker", "PostgreSQL", "AWS"],
            experience_years=5.0
        )
        
        self.assertGreater(res["estimated_min"], 90000)
        self.assertGreater(res["estimated_median"], res["estimated_min"])
        self.assertGreater(res["estimated_max"], res["estimated_median"])
        self.assertGreaterEqual(res["market_percentile"], 50)

    def test_end_to_end_analyzer(self):
        resume = """
        Jane Smith
        jane.smith@tech.com | (555) 987-6543
        4 years of experience as Full Stack Developer.
        Bachelor of Technology in Computer Science.
        Skills: React, TypeScript, Node.js, FastAPI, PostgreSQL, Docker, Git.
        """
        result = analyzer_service.analyze_resume(
            resume_text=resume,
            target_role="Senior Full Stack Developer"
        )
        
        self.assertEqual(result["status"], "success")
        self.assertGreater(result["fit_analysis"]["overall_match_score"], 40.0)
        self.assertGreater(len(result["fit_analysis"]["matched_skills"]), 0)
        self.assertGreater(len(result["recommendations"]), 0)
        self.assertGreater(len(result["alternative_roles"]), 0)

    def test_hindi_extraction_and_analysis(self):
        hindi_resume = """
        अमित कुमार
        ईमेल: amit.kumar@example.com | फोन: 9876543210
        अनुभव: 3 वर्ष का अनुभव
        शिक्षा: बी.टेक कंप्यूटर साइंस
        कौशल: पायथन, रिएक्ट, डॉकर, फास्टएपीआई, पोस्टग्रेएसक्यूएल, गिट
        """
        result = analyzer_service.analyze_resume(
            resume_text=hindi_resume,
            target_role="Senior Full Stack Developer"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["detected_language"], "hi")
        self.assertEqual(result["profile"]["candidate_name"], "अमित कुमार")
        self.assertEqual(result["profile"]["experience"]["estimated_years"], 3.0)
        self.assertIn("Bachelor of Technology (B.Tech)", result["profile"]["education"])
        self.assertIn("python", result["profile"]["skills"]["all_skills"])
        self.assertIn("react", result["profile"]["skills"]["all_skills"])
        self.assertIn("docker", result["profile"]["skills"]["all_skills"])
        # Check that active summary is in Hindi
        self.assertTrue(any(c in result["active_summary"] for c in "अआइईउऊऋएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह"))

if __name__ == "__main__":
    unittest.main()
