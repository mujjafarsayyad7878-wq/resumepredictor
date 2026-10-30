"""
Analyzer Service: Central Orchestrator
Coordinates NLP extraction, scoring, role fit classification,
salary estimation, and learning recommendations in simple language.
Supports both English and Hindi seamlessly.
"""
from typing import Dict, Any, Optional

from app.nlp.entity_extractor import extractor
from app.nlp.career_classifier import classifier
from app.nlp.salary_predictor import salary_model
from app.services.recommendation_engine import recommendation_engine

class AnalyzerService:
    @staticmethod
    def analyze_resume(
        resume_text: str,
        target_role: Optional[str] = "Senior Full Stack Developer",
        custom_jd: Optional[str] = None,
        language_preference: Optional[str] = "auto"
    ) -> Dict[str, Any]:
        """
        Executes complete end-to-end analysis on candidate resume with language detection.
        """
        if not resume_text or len(resume_text.strip()) < 10:
            raise ValueError("Resume text is too short or empty. Please provide valid resume content.")

        # 1. Feature & Entity Extraction (with language detection)
        profile = extractor.extract_all(resume_text)
        detected_lang = profile.get("detected_language", "en")
        if language_preference in ["hi", "en"]:
            active_lang = language_preference
        else:
            active_lang = detected_lang

        # 2. Fit Evaluation & Skill Gap Calculation
        fit_results = classifier.evaluate_role_fit(
            resume_text=resume_text,
            resume_profile=profile,
            target_role_name=target_role,
            custom_jd_text=custom_jd
        )

        # 3. Salary & Compensation Prediction (USD + INR LPA)
        has_advanced = any("master" in str(edu).lower() or "phd" in str(edu).lower() for edu in profile["education"])
        salary_results = salary_model.predict_salary(
            role_name=fit_results["target_role"],
            matched_skills=fit_results["matched_skills"],
            experience_years=profile["experience"]["estimated_years"],
            has_advanced_degree=has_advanced
        )

        # 4. Learning Resource Recommendations for Missing Skills
        recommendations = recommendation_engine.get_recommendations_for_missing_skills(
            missing_skills=fit_results["missing_skills"],
            max_results=6
        )

        # 5. Alternative Career Match Rankings
        alternative_roles = classifier.predict_alternative_roles(
            candidate_skills=set(profile["skills"]["all_skills"]),
            candidate_exp=profile["experience"]["estimated_years"]
        )

        # Active language summary and badges
        is_hindi = (active_lang == "hi")
        active_summary = fit_results["summary_hi"] if is_hindi else fit_results["summary_en"]
        active_match_tier = fit_results["match_tier_hi"] if is_hindi else fit_results["match_tier"]
        active_seniority = profile["experience"].get("seniority_level_hi", profile["experience"]["seniority_level"]) if is_hindi else profile["experience"]["seniority_level"]

        return {
            "status": "success",
            "detected_language": detected_lang,
            "active_language": active_lang,
            "active_summary": active_summary,
            "active_match_tier": active_match_tier,
            "active_seniority": active_seniority,
            "profile": profile,
            "fit_analysis": fit_results,
            "salary_prediction": salary_results,
            "recommendations": recommendations,
            "alternative_roles": alternative_roles
        }

analyzer_service = AnalyzerService()
