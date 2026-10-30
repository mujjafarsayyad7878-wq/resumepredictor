"""
Salary Predictor Model
Estimates market compensation in USD and INR based on skills, experience level, and tech stack demand.
Uses simple, human-friendly wording so anyone can understand.
"""
from typing import Dict, List, Any
from app.nlp.skill_taxonomy import JOB_ROLES

PREMIUM_SKILLS = {
    "kubernetes": 0.08, "pytorch": 0.09, "terraform": 0.06, "aws": 0.06,
    "rag": 0.10, "llm": 0.10, "generative ai": 0.10, "langchain": 0.08,
    "rust": 0.08, "distributed systems": 0.07, "system design": 0.07,
    "apache spark": 0.06, "go": 0.06, "kafka": 0.07
}

class SalaryPredictor:
    @staticmethod
    def predict_salary(
        role_name: str,
        matched_skills: List[str],
        experience_years: float,
        has_advanced_degree: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates predicted salary package breakdown and market percentile in USD and INR.
        """
        role_info = JOB_ROLES.get(role_name)
        if not role_info:
            base_min = 100000
            base_median = 135000
            base_max = 175000
            inr_base_min = 10.0
            inr_base_max = 24.0
            min_exp = 3.0
        else:
            base_min = role_info["salary_range"]["min"]
            base_median = role_info["salary_range"]["median"]
            base_max = role_info["salary_range"]["max"]
            inr_base_min = float(role_info["salary_range"].get("inr_lpa_min", 12.0))
            inr_base_max = float(role_info["salary_range"].get("inr_lpa_max", 28.0))
            min_exp = float(role_info["min_experience_years"])

        # 1. Experience factor
        exp_diff = experience_years - min_exp
        exp_multiplier = 1.0 + max(-0.25, min(0.35, exp_diff * 0.04))

        # 2. Skill match bonus
        skill_bonus = 0.0
        matched_lower = {s.lower() for s in matched_skills}
        for p_skill, bonus in PREMIUM_SKILLS.items():
            if p_skill in matched_lower:
                skill_bonus += bonus
        skill_bonus = min(skill_bonus, 0.25)

        # 3. Advanced degree bonus
        degree_bonus = 0.05 if has_advanced_degree else 0.0

        total_multiplier = exp_multiplier + skill_bonus + degree_bonus

        predicted_min = int(round(base_min * (total_multiplier * 0.95), -2))
        predicted_median = int(round(base_median * total_multiplier, -2))
        predicted_max = int(round(base_max * (total_multiplier * 1.05), -2))

        # INR Lakhs Per Annum (LPA)
        inr_min_lpa = round(inr_base_min * total_multiplier * 0.95, 1)
        inr_median_lpa = round(((inr_base_min + inr_base_max) / 2) * total_multiplier, 1)
        inr_max_lpa = round(inr_base_max * total_multiplier * 1.05, 1)

        # Percentile estimate
        percentile = min(98, max(15, int(50 + (total_multiplier - 1.0) * 100)))

        # Simple explanations
        explanation_en = (
            f"Estimated market salary based on your {experience_years} years of experience "
            f"and matching skills. High-demand skills give an extra bonus in the job market."
        )
        explanation_hi = (
            f"आपके {experience_years} वर्ष के अनुभव और कौशल के आधार पर यह वार्षिक वेतन का सटीक अनुमान है।"
        )

        return {
            "currency": "USD",
            "estimated_min": predicted_min,
            "estimated_median": predicted_median,
            "estimated_max": predicted_max,
            "formatted_range": f"${predicted_min:,} - ${predicted_max:,}",
            "formatted_median": f"${predicted_median:,} / yr",
            "inr_min_lpa": inr_min_lpa,
            "inr_median_lpa": inr_median_lpa,
            "inr_max_lpa": inr_max_lpa,
            "formatted_inr": f"₹{inr_min_lpa} - ₹{inr_max_lpa} लाख / वर्ष",
            "formatted_inr_median": f"₹{inr_median_lpa} लाख / वर्ष",
            "market_percentile": percentile,
            "explanation_en": explanation_en,
            "explanation_hi": explanation_hi,
            "factors": {
                "experience_multiplier": round(exp_multiplier, 2),
                "premium_skills_bonus_pct": round(skill_bonus * 100, 1),
                "degree_bonus_pct": round(degree_bonus * 100, 1)
            },
            "confidence": "High" if len(matched_skills) >= 5 else "Moderate",
            "confidence_hi": "उच्च (विश्वसनीय)" if len(matched_skills) >= 5 else "मध्यम"
        }

salary_model = SalaryPredictor()
