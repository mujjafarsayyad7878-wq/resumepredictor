"""
Career Role Classifier and Skill Gap Analyzer
Uses simple, human-friendly wording and supports both English and Hindi output.
"""
from typing import Dict, List, Set, Any, Optional
from app.config import settings
from app.nlp.skill_taxonomy import JOB_ROLES, SKILL_TO_CATEGORY
from app.nlp.tfidf_engine import compute_similarity
from app.nlp.entity_extractor import extractor

class CareerClassifier:
    def __init__(self):
        pass

    def evaluate_role_fit(
        self,
        resume_text: str,
        resume_profile: Dict[str, Any],
        target_role_name: Optional[str] = None,
        custom_jd_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculates exact match score, matched skills, missing skills, and career fit.
        Supports both pre-configured standard roles or custom Job Descriptions.
        """
        candidate_skills = set(resume_profile["skills"]["all_skills"])
        candidate_exp = resume_profile["experience"]["estimated_years"]
        candidate_education = resume_profile["education"]

        # Determine target requirements
        display_title_hi = "टारगेट जॉब रोल"
        if target_role_name and target_role_name in JOB_ROLES:
            role_def = JOB_ROLES[target_role_name]
            required_skills = set(role_def["primary_skills"])
            secondary_skills = set(role_def["secondary_skills"])
            all_target_skills = required_skills | secondary_skills
            min_exp = role_def["min_experience_years"]
            target_description = f"{role_def['title']}. {role_def['summary']} Required skills: {', '.join(role_def['primary_skills'] + role_def['secondary_skills'])}"
            display_title = role_def["title"]
            display_title_hi = role_def.get("title_hi", role_def["title"])
        elif custom_jd_text and custom_jd_text.strip():
            # Extract skills directly from custom job description
            jd_extracted = extractor.extract_skills(custom_jd_text)
            all_target_skills = set(jd_extracted["all_skills"])
            required_skills = set(list(all_target_skills)[:max(1, len(all_target_skills) // 2)])
            secondary_skills = all_target_skills - required_skills
            min_exp = 3.0
            target_description = custom_jd_text
            display_title = "Custom Job Description"
            display_title_hi = "कस्टम जॉब विवरण (Custom JD)"
        else:
            role_def = JOB_ROLES["Senior Full Stack Developer"]
            required_skills = set(role_def["primary_skills"])
            secondary_skills = set(role_def["secondary_skills"])
            all_target_skills = required_skills | secondary_skills
            min_exp = role_def["min_experience_years"]
            target_description = role_def["summary"]
            display_title = role_def["title"]
            display_title_hi = role_def.get("title_hi", role_def["title"])

        # 1. Matched vs Missing Skills
        matched_primary = sorted(list(candidate_skills & required_skills))
        matched_secondary = sorted(list(candidate_skills & secondary_skills))
        all_matched = sorted(list(candidate_skills & all_target_skills))
        
        missing_primary = sorted(list(required_skills - candidate_skills))
        missing_secondary = sorted(list(secondary_skills - candidate_skills))
        all_missing = sorted(list(all_target_skills - candidate_skills))

        extra_skills = sorted(list(candidate_skills - all_target_skills))

        # Skill match percentage (hard skills coverage)
        if all_target_skills:
            primary_coverage = len(matched_primary) / max(1, len(required_skills))
            secondary_coverage = len(matched_secondary) / max(1, len(secondary_skills)) if secondary_skills else 1.0
            skill_score = (primary_coverage * 0.75 + secondary_coverage * 0.25) * 100.0
        else:
            skill_score = 70.0

        # 2. Text Similarity Match
        similarity_res = compute_similarity(resume_text, target_description)
        tfidf_score = similarity_res["percentage"]

        # 3. Experience Match
        if candidate_exp >= min_exp:
            exp_score = 100.0
            exp_status = "Meets or exceeds requirement"
            exp_status_hi = "आवश्यकता के अनुसार पर्याप्त अनुभव"
        else:
            exp_score = max(20.0, (candidate_exp / max(1.0, min_exp)) * 100.0)
            diff = round(min_exp - candidate_exp, 1)
            exp_status = f"{diff} yrs below target"
            exp_status_hi = f"टारगेट से {diff} वर्ष कम अनुभव"

        # 4. Education Match
        edu_score = 100.0 if candidate_education else 75.0

        # Weighted Overall Composite Match Score (0 - 100)
        overall_score = (
            (skill_score * settings.WEIGHT_EXACT_SKILLS) +
            (tfidf_score * settings.WEIGHT_TFIDF) +
            (exp_score * settings.WEIGHT_EXPERIENCE) +
            (edu_score * settings.WEIGHT_EDUCATION)
        )
        overall_score = round(max(5.0, min(99.0, overall_score)), 1)

        # Categorize Match Level in Plain Language (English and Hindi)
        if overall_score >= 80:
            match_tier = "Excellent Fit"
            match_tier_hi = "उत्कृष्ट मेल (शानदार तैयारी)"
            tier_color = "emerald"
            summary_en = f"Outstanding match! Your resume matches {overall_score}% with this job. You have most of the primary skills required."
            summary_hi = f"शानदार! आपका रिज्यूमे इस नौकरी के लिए {overall_score}% उपयुक्त है। आपके पास आवश्यक अधिकांश मुख्य कौशल मौजूद हैं।"
        elif overall_score >= 65:
            match_tier = "Good Match"
            match_tier_hi = "अच्छा मेल (तैयारी अच्छी है)"
            tier_color = "blue"
            summary_en = f"Good match! You have {overall_score}% compatibility. Learning the few missing skills below will make your profile stand out."
            summary_hi = f"अच्छा मेल! आपका प्रोफाइल {overall_score}% मेल खाता है। नीचे दिए गए कुछ छूटे हुए कौशल सीखकर आप पूरी तरह तैयार हो सकते हैं।"
        elif overall_score >= 45:
            match_tier = "Moderate Skill Gap"
            match_tier_hi = "औसत मेल (कुछ कौशल सीखने होंगे)"
            tier_color = "amber"
            summary_en = f"Fair match ({overall_score}%). You have a solid base, but learning the missing tools listed below will help you land interviews."
            summary_hi = f"औसत मेल ({overall_score}%)। आपके पास अच्छा आधार है, लेकिन नीचे दिए गए छूटे हुए कौशल सीखने से आपकी नौकरी मिलने की संभावना काफी बढ़ जाएगी।"
        else:
            match_tier = "Substantial Skill Gap"
            match_tier_hi = "कौशल अंतर (नई चीजें सीखनी होंगी)"
            tier_color = "rose"
            summary_en = f"Current match is {overall_score}%. This role requires foundational skills you haven't listed yet. Check the free courses below to get started!"
            summary_hi = f"वर्तमान स्कोर {overall_score}% है। इस पद के लिए कुछ नई तकनीकों की जरूरत है। नीचे दिए गए मुफ्त कोर्सेज से शुरुआत करें!"

        return {
            "target_role": display_title,
            "target_role_hi": display_title_hi,
            "overall_match_score": overall_score,
            "match_tier": match_tier,
            "match_tier_hi": match_tier_hi,
            "tier_color": tier_color,
            "summary_en": summary_en,
            "summary_hi": summary_hi,
            "tfidf_similarity": round(tfidf_score, 1),
            "skill_match_percentage": round(skill_score, 1),
            "experience_match_score": round(exp_score, 1),
            "experience_status": exp_status,
            "experience_status_hi": exp_status_hi,
            "education_match_score": round(edu_score, 1),
            "matched_skills": [s.title() for s in all_matched],
            "missing_skills": [s.title() for s in all_missing],
            "missing_primary_skills": [s.title() for s in missing_primary],
            "missing_secondary_skills": [s.title() for s in missing_secondary],
            "extra_skills": [s.title() for s in extra_skills[:15]],
            "weights_used": {
                "skills": settings.WEIGHT_EXACT_SKILLS,
                "tfidf": settings.WEIGHT_TFIDF,
                "experience": settings.WEIGHT_EXPERIENCE,
                "education": settings.WEIGHT_EDUCATION
            }
        }

    def predict_alternative_roles(self, candidate_skills: Set[str], candidate_exp: float) -> List[Dict[str, Any]]:
        """
        Evaluates candidate against all pre-configured industry roles and returns ranked matches in simple language.
        """
        rankings = []
        lower_skills = {s.lower() for s in candidate_skills}

        for role_name, role_data in JOB_ROLES.items():
            req = set(role_data["primary_skills"])
            sec = set(role_data["secondary_skills"])
            all_req = req | sec
            
            matched = lower_skills & all_req
            missing = all_req - lower_skills

            match_pct = (len(matched) / max(1, len(all_req))) * 100.0
            
            # Simple seniority suitability
            exp_diff = candidate_exp - role_data["min_experience_years"]
            if exp_diff >= 0:
                fit_text = "Experienced Enough"
                fit_text_hi = "पर्याप्त अनुभव"
            elif exp_diff >= -1.5:
                fit_text = "Almost Ready"
                fit_text_hi = "लगभग तैयार"
            else:
                fit_text = "Junior for this role"
                fit_text_hi = "अनुभव की जरूरत"

            rankings.append({
                "role_title": role_name,
                "role_title_hi": role_data.get("title_hi", role_name),
                "category": role_data["category"],
                "category_hi": role_data.get("category_hi", role_data["category"]),
                "match_percentage": round(match_pct, 1),
                "matched_count": len(matched),
                "missing_count": len(missing),
                "seniority_fit": fit_text,
                "seniority_fit_hi": fit_text_hi,
                "salary_range": role_data["salary_range"]
            })

        rankings.sort(key=lambda x: x["match_percentage"], reverse=True)
        return rankings

classifier = CareerClassifier()
