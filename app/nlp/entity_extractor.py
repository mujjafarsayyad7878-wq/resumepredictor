"""
Resume Entity Extractor: Contact Info, Skills, Education, Experience & Seniority
Supports both English and Hindi candidate resumes with bilingual normalization.
"""
import re
from datetime import datetime
from typing import Dict, List, Set, Any, Optional

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
    except Exception:
        nlp = None
        SPACY_AVAILABLE = False
except ImportError:
    nlp = None
    SPACY_AVAILABLE = False

from app.nlp.preprocessor import clean_text, detect_language
from app.nlp.skill_taxonomy import SKILL_TAXONOMY, SKILL_TO_CATEGORY, HINDI_SKILL_MAPPINGS

class EntityExtractor:
    def __init__(self):
        # Email regex
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        
        # Phone regex (supports international, US, and Indian numbers)
        self.phone_pattern = re.compile(
            r'(?:(?:\+?91[\-\s]?)?[6-9]\d{9})|(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?|\b\d{10}\b|\b\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b'
        )

        # Links
        self.linkedin_pattern = re.compile(r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/([a-zA-Z0-9_-]+)', re.IGNORECASE)
        self.github_pattern = re.compile(r'(?:https?:\/\/)?(?:www\.)?github\.com\/([a-zA-Z0-9_-]+)', re.IGNORECASE)

        # Education degree patterns (English and Hindi)
        self.degrees_map = {
            "phd": "Ph.D. / Doctorate",
            "doctorate": "Ph.D. / Doctorate",
            "डॉक्टरेट": "Ph.D. / Doctorate",
            "पीएचडी": "Ph.D. / Doctorate",
            "master": "Master's Degree",
            "मास्टर्स": "Master's Degree",
            "परास्नातक": "Master's Degree",
            "m.s": "Master of Science (M.S.)",
            "m.tech": "Master of Technology (M.Tech)",
            "mtech": "Master of Technology (M.Tech)",
            "एम.टेक": "Master of Technology (M.Tech)",
            "एमटेक": "Master of Technology (M.Tech)",
            "msc": "Master of Science",
            "एम.एससी": "Master of Science",
            "एमएससी": "Master of Science",
            "mba": "MBA",
            "एमबीए": "MBA",
            "bachelor": "Bachelor's Degree",
            "स्नातक": "Bachelor's Degree",
            "b.s": "Bachelor of Science (B.S.)",
            "b.tech": "Bachelor of Technology (B.Tech)",
            "btech": "Bachelor of Technology (B.Tech)",
            "बी.टेक": "Bachelor of Technology (B.Tech)",
            "बीटेक": "Bachelor of Technology (B.Tech)",
            "b.e": "Bachelor of Engineering (B.E.)",
            "be": "Bachelor of Engineering (B.E.)",
            "bsc": "Bachelor of Science",
            "बी.एससी": "Bachelor of Science",
            "बीएससी": "Bachelor of Science",
            "इंजीनियरिंग": "Bachelor of Engineering (B.E.)",
            "डिप्लोमा": "Diploma / Associate",
            "associate": "Associate Degree"
        }

        # Experience pattern: e.g. "5+ years", "3 years of experience", "8 years in software"
        self.exp_years_pattern = re.compile(
            r'(\b\d{1,2}(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+(?:professional|industry|relevant))?\s*(?:experience|exp)?\b',
            re.IGNORECASE
        )

        # Hindi Experience patterns: "3 वर्ष का अनुभव", "अनुभव: 4 साल", "5 साल का अनुभव"
        self.hindi_exp_pattern = re.compile(
            r'(?:अनुभव\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)\s*(?:वर्ष|साल)?)|(?:(\d{1,2}(?:\.\d+)?)\s*(?:वर्ष|साल)\s*(?:का)?\s*अनुभव)',
            re.IGNORECASE
        )

        # Year range pattern: e.g. "2018 - 2023", "2019 to Present", "2021 – current"
        self.year_range_pattern = re.compile(
            r'\b(19\d{2}|20\d{2})\s*(?:-|–|—|to)\s*(19\d{2}|20\d{2}|present|current|now)\b',
            re.IGNORECASE
        )

    def extract_name(self, text: str) -> Optional[str]:
        """
        Extracts candidate's full name from the top portion of the resume.
        Supports both English and Devanagari Hindi names.
        """
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # Check first line for explicit "नाम: अमित शर्मा"
        for line in lines[:4]:
            name_prefix_match = re.search(r'^(?:नाम|Name)\s*[:\-]\s*(.+)$', line, re.IGNORECASE)
            if name_prefix_match:
                candidate = name_prefix_match.group(1).strip()
                if 2 <= len(candidate.split()) <= 4:
                    return candidate

        # Check for Hindi Devanagari full name in first 3 lines
        for line in lines[:3]:
            # If line is only Devanagari words and spaces
            cleaned_line = line.strip()
            dev_chars = len(re.findall(r'[\u0900-\u097F]', cleaned_line))
            if dev_chars >= 4 and not any(kw in cleaned_line for kw in ["ईमेल", "फोन", "लिंक्डइन", "कौशल", "अनुभव", "शिक्षा", "रिज्यूमे"]):
                words = cleaned_line.split()
                if 1 <= len(words) <= 4:
                    return cleaned_line

        if SPACY_AVAILABLE and nlp:
            doc = nlp(text[:800])
            for ent in doc.ents:
                if ent.label_ == "PERSON" and 2 <= len(ent.text.split()) <= 4:
                    cleaned_name = ent.text.strip().replace("\n", " ")
                    if not any(kw in cleaned_name.lower() for kw in ["resume", "curriculum", "vitae", "summary", "experience"]):
                        return cleaned_name

        # Heuristic fallback: check first 5 non-empty lines
        for line in lines[:5]:
            if (not self.email_pattern.search(line) and 
                not self.phone_pattern.search(line) and 
                not any(kw in line.lower() for kw in ["http", "github", "linkedin", "curriculum", "resume", "summary", "profile", "contact", "developer", "engineer"])):
                words = line.split()
                if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
                    return line
        
        return "Candidate Profile"

    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """
        Extracts email, phone, LinkedIn, and GitHub links.
        """
        emails = self.email_pattern.findall(text)
        email = emails[0] if emails else None

        phones = self.phone_pattern.findall(text)
        phone = None
        if phones:
            match = phones[0]
            if isinstance(match, tuple):
                phone = "".join(filter(None, match)).strip()
            else:
                phone = str(match).strip()

        linkedin_match = self.linkedin_pattern.search(text)
        linkedin = f"https://linkedin.com/in/{linkedin_match.group(1)}" if linkedin_match else None

        github_match = self.github_pattern.search(text)
        github = f"https://github.com/{github_match.group(1)}" if github_match else None

        return {
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github
        }

    def extract_education(self, text: str) -> List[str]:
        """
        Identifies degree mentions in the text in English and Hindi.
        """
        lower_text = text.lower()
        detected_degrees = set()
        for key, standard_name in self.degrees_map.items():
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(key) + r'(?![a-zA-Z0-9])'
            if re.search(pattern, lower_text):
                detected_degrees.add(standard_name)

        return sorted(list(detected_degrees))

    def extract_experience_years(self, text: str) -> Dict[str, Any]:
        """
        Estimates total years of professional experience and seniority level.
        Supports both English and Hindi expressions.
        """
        detected_years = []
        for match in self.exp_years_pattern.finditer(text):
            try:
                val = float(match.group(1))
                if 0.5 <= val <= 35:
                    detected_years.append(val)
            except ValueError:
                pass

        # Check Hindi experience regex
        for match in self.hindi_exp_pattern.finditer(text):
            g1, g2 = match.groups()
            matched_val = g1 or g2
            if matched_val:
                try:
                    val = float(matched_val)
                    if 0.5 <= val <= 35:
                        detected_years.append(val)
                except ValueError:
                    pass

        # Also calculate span from date ranges
        current_year = datetime.now().year
        spans = []
        for match in self.year_range_pattern.finditer(text):
            start = int(match.group(1))
            end_str = match.group(2).lower()
            end = current_year if end_str in ["present", "current", "now"] else int(end_str)
            if start <= end and (end - start) <= 30:
                spans.append(end - start)

        total_exp = 0.0
        if detected_years:
            total_exp = max(detected_years)
        elif spans:
            total_exp = min(sum(spans), 25.0)

        # Seniority Level Classification (Plain Language & Hindi Friendly)
        if total_exp < 2:
            seniority = "Junior / Entry-Level"
            seniority_hi = "शुरुआती स्तर / फ्रेशर (Entry-Level)"
        elif total_exp < 5:
            seniority = "Mid-Level Professional"
            seniority_hi = "मध्यम स्तर (Mid-Level, 2-5 वर्ष)"
        elif total_exp < 8:
            seniority = "Senior Professional"
            seniority_hi = "वरिष्ठ पेशेवर (Senior, 5+ वर्ष)"
        elif total_exp < 12:
            seniority = "Staff / Lead Engineer"
            seniority_hi = "लीड / मुख्य इंजीनियर (Lead / Staff)"
        else:
            seniority = "Principal / Architect"
            seniority_hi = "प्रिंसिपल / आर्किटेक्ट (Principal / Architect)"

        return {
            "estimated_years": round(total_exp, 1),
            "seniority_level": seniority,
            "seniority_level_hi": seniority_hi
        }

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """
        Matches resume content against 600+ skills taxonomy and Hindi transliterations.
        """
        lower_text = " " + clean_text(text).lower() + " "
        matched_skills: Set[str] = set()
        categorized_skills: Dict[str, List[str]] = {cat: [] for cat in SKILL_TAXONOMY.keys()}

        # 1. Standard English Skill Taxonomy
        for skill, category in SKILL_TO_CATEGORY.items():
            escaped_skill = re.escape(skill)
            plural_suffix = r's?' if not skill.endswith(('+', '#', 's')) else r''
            pattern = r'(?<![a-zA-Z0-9])' + escaped_skill + plural_suffix + r'(?![a-zA-Z0-9])'
            if re.search(pattern, lower_text):
                matched_skills.add(skill)
                if skill.title() not in categorized_skills[category]:
                    categorized_skills[category].append(skill.title())

        # 2. Hindi Devanagari Skill Mappings
        for hindi_word, mapped_skill in HINDI_SKILL_MAPPINGS.items():
            if hindi_word in lower_text:
                matched_skills.add(mapped_skill)
                cat = SKILL_TO_CATEGORY.get(mapped_skill, "Software Engineering & Tools")
                if mapped_skill.title() not in categorized_skills[cat]:
                    categorized_skills[cat].append(mapped_skill.title())

        categorized_clean = {cat: skills for cat, skills in categorized_skills.items() if skills}

        return {
            "all_skills": sorted(list(matched_skills)),
            "skills_count": len(matched_skills),
            "categorized": categorized_clean
        }

    def extract_all(self, text: str) -> Dict[str, Any]:
        """
        Full extraction pipeline with language detection.
        """
        lang = detect_language(text)
        clean_doc = clean_text(text)
        return {
            "candidate_name": self.extract_name(text),
            "contact_info": self.extract_contact_info(text),
            "education": self.extract_education(clean_doc),
            "experience": self.extract_experience_years(clean_doc),
            "skills": self.extract_skills(clean_doc),
            "word_count": len(clean_doc.split()),
            "detected_language": lang
        }

extractor = EntityExtractor()
