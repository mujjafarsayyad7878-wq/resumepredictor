"""
Comprehensive Skill Taxonomy and Standard Job Role Profiles
Supports English and Hindi tech taxonomy mapping and simple explanations.
"""
from typing import Dict, List, Set, Any

SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Programming Languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "c", "go", "golang", 
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "shell", "bash", "powershell"
    ],
    "Frontend Development": [
        "react", "react.js", "reactjs", "next.js", "nextjs", "vue", "vue.js", "vuejs", 
        "angular", "svelte", "html", "html5", "css", "css3", "tailwind", "tailwind css", 
        "bootstrap", "sass", "scss", "redux", "zustand", "webpack", "vite", "responsive design",
        "web components", "jquery"
    ],
    "Backend & APIs": [
        "fastapi", "flask", "django", "node.js", "nodejs", "express", "express.js",
        "spring boot", "spring", "asp.net", ".net core", "ruby on rails", "rails",
        "nestjs", "graphql", "rest api", "restful apis", "microservices", "grpc", 
        "celery", "websockets", "api design"
    ],
    "AI, ML & Data Science": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "llm", "large language models", "rag", "retrieval augmented generation",
        "generative ai", "langchain", "transformers", "hugging face", "pytorch", 
        "tensorflow", "keras", "scikit-learn", "sklearn", "spacy", "nltk", "opencv",
        "pandas", "numpy", "scipy", "xgboost", "lightgbm", "data analysis", "data visualization",
        "feature engineering", "model deployment", "reinforcement learning"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud", 
        "docker", "kubernetes", "k8s", "terraform", "ansible", "helm", "ci/cd", 
        "github actions", "gitlab ci", "jenkins", "linux", "bash scripting", "serverless", 
        "aws lambda", "cloudformation", "prometheus", "grafana", "nginx", "elk stack"
    ],
    "Databases & Storage": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", 
        "cassandra", "dynamodb", "sqlite", "oracle", "mariadb", "neo4j", "supabase", 
        "firebase", "prisma", "sqlalchemy", "sql", "nosql"
    ],
    "Data Engineering & Big Data": [
        "apache spark", "spark", "apache kafka", "kafka", "apache airflow", "airflow",
        "etl", "data pipelines", "hadoop", "snowflake", "bigquery", "databricks", 
        "dbt", "tableau", "power bi", "looker", "data warehousing"
    ],
    "Cybersecurity & Infrastructure": [
        "penetration testing", "ethical hacking", "siem", "soc", "wireshark", 
        "cryptography", "owasp", "network security", "iam", "vulnerability assessment", 
        "firewalls", "zero trust", "cissp", "soc 2", "incident response"
    ],
    "Software Engineering & Tools": [
        "git", "github", "gitlab", "jira", "docker", "unit testing", "pytest", 
        "jest", "cypress", "system design", "distributed systems", "agile", 
        "scrum", "tdd", "clean code", "design patterns", "ci/cd"
    ]
}

# Inverted mapping: skill -> category
SKILL_TO_CATEGORY: Dict[str, str] = {}
for category, skills in SKILL_TAXONOMY.items():
    for skill in skills:
        SKILL_TO_CATEGORY[skill.lower()] = category

# Hindi / Devanagari transliteration to English tech skills
HINDI_SKILL_MAPPINGS: Dict[str, str] = {
    "पायथन": "python",
    "पाइथन": "python",
    "जावा": "java",
    "जावास्क्रिप्ट": "javascript",
    "टाइपस्क्रिप्ट": "typescript",
    "रिएक्ट": "react",
    "नोड": "node.js",
    "नोड.जेएस": "node.js",
    "एचटीएमएल": "html",
    "सीएसएस": "css",
    "फास्टएपीआई": "fastapi",
    "फ्लास्क": "flask",
    "जांगो": "django",
    "डॉकर": "docker",
    "कुबेरनेट्स": "kubernetes",
    "गिट": "git",
    "गिटहब": "github",
    "एसक्यूएल": "sql",
    "पोस्टग्रेएसक्यूएल": "postgresql",
    "माइएसक्यूएल": "mysql",
    "मोंगोडीबी": "mongodb",
    "एडब्ल्यूएस": "aws",
    "क्लाउड": "aws",
    "लिनक्स": "linux",
    "मशीन लर्निंग": "machine learning",
    "डीप लर्निंग": "deep learning",
    "डेटा साइंस": "data analysis",
    "डेटा विश्लेषण": "data analysis",
    "डेटा एनालिसिस": "data analysis",
    "आर्टिफिशियल इंटेलिजेंस": "machine learning",
    "सिस्टम डिजाइन": "system design",
    "एपीआई": "rest api",
    "माइक्रोसर्विसेज": "microservices",
    "टेलविंड": "tailwind",
    "रेडिस": "redis",
    "टेबलू": "tableau",
    "पॉवर बीआई": "power bi",
    "साइबर सुरक्षा": "network security",
    "नेटवर्क सुरक्षा": "network security"
}

# Category names in simple Hindi
CATEGORY_HI: Dict[str, str] = {
    "Programming Languages": "प्रोग्रामिंग भाषाएं (Programming Languages)",
    "Frontend Development": "वेबसाइट डिजाइन और फ्रंटएंड (Frontend)",
    "Backend & APIs": "बैकएंड और सर्वर एपीआई (Backend & APIs)",
    "AI, ML & Data Science": "आर्टिफिशियल इंटेलिजेंस व डेटा (AI/ML)",
    "Cloud & DevOps": "क्लाउड और सर्वर टूल्स (Cloud & DevOps)",
    "Databases & Storage": "डेटाबेस और स्टोरेज (Databases)",
    "Data Engineering & Big Data": "डेटा इंजीनियरिंग (Data Engineering)",
    "Cybersecurity & Infrastructure": "साइबर सुरक्षा (Cybersecurity)",
    "Software Engineering & Tools": "सॉफ्टवेयर टूल्स (Software Tools)"
}

# Standard Pre-configured Industry Job Roles with benchmark requirements and bilingual friendly text
JOB_ROLES: Dict[str, Dict[str, Any]] = {
    "Senior Full Stack Developer": {
        "title": "Senior Full Stack Developer",
        "title_hi": "वरिष्ठ फुल स्टैक डेवलपर (Full Stack)",
        "category": "Software Engineering",
        "category_hi": "सॉफ्टवेयर इंजीनियरिंग",
        "min_experience_years": 4,
        "required_education": ["bachelor", "master", "computer science"],
        "primary_skills": [
            "react", "typescript", "javascript", "node.js", "fastapi", "python", 
            "postgresql", "docker", "rest api", "git", "ci/cd", "system design"
        ],
        "secondary_skills": [
            "next.js", "tailwind css", "redis", "aws", "microservices", "unit testing", "graphql"
        ],
        "salary_range": {"min": 115000, "median": 145000, "max": 185000, "currency": "USD", "inr_lpa_min": 12, "inr_lpa_max": 28},
        "summary": "Builds both the website screens (Frontend) and the server/database logic (Backend), ensuring fast and secure user experiences.",
        "summary_hi": "यह डेवलपर वेबसाइट के सामने दिखने वाले हिस्से (Frontend) और पीछे के सर्वर व डेटाबेस (Backend) दोनों को तैयार करता है।"
    },
    "AI / Machine Learning Engineer": {
        "title": "AI / Machine Learning Engineer",
        "title_hi": "एआई और मशीन लर्निंग इंजीनियर (AI/ML)",
        "category": "Artificial Intelligence",
        "category_hi": "आर्टिफिशियल इंटेलिजेंस",
        "min_experience_years": 3,
        "required_education": ["bachelor", "master", "phd", "data science", "computer science"],
        "primary_skills": [
            "python", "pytorch", "tensorflow", "machine learning", "deep learning", 
            "nlp", "scikit-learn", "pandas", "numpy", "transformers", "docker", "git"
        ],
        "secondary_skills": [
            "llm", "rag", "langchain", "hugging face", "fastapi", "aws", "kubernetes", "opencv", "model deployment"
        ],
        "salary_range": {"min": 130000, "median": 165000, "max": 215000, "currency": "USD", "inr_lpa_min": 15, "inr_lpa_max": 35},
        "summary": "Builds smart AI models, trains algorithms on data, and connects AI features into apps and systems.",
        "summary_hi": "स्मार्ट कंप्यूटर मॉडल बनाता है, डेटा से चीजें सीखने वाले एल्गोरिदम तैयार करता है और नए एआई फीचर्स को ऐप्स में जोड़ता है।"
    },
    "Cloud & DevOps Architect": {
        "title": "Cloud & DevOps Architect",
        "title_hi": "क्लाउड और डेवऑप्स इंजीनियर (Cloud & DevOps)",
        "category": "Cloud Infrastructure",
        "category_hi": "क्लाउड इंफ्रास्ट्रक्चर",
        "min_experience_years": 5,
        "required_education": ["bachelor", "computer science", "engineering"],
        "primary_skills": [
            "aws", "kubernetes", "docker", "terraform", "ci/cd", "linux", 
            "python", "bash", "github actions", "prometheus", "grafana"
        ],
        "secondary_skills": [
            "azure", "gcp", "ansible", "helm", "serverless", "microservices", "security", "api design"
        ],
        "salary_range": {"min": 135000, "median": 170000, "max": 220000, "currency": "USD", "inr_lpa_min": 16, "inr_lpa_max": 38},
        "summary": "Manages online servers and cloud platforms (like AWS) so that apps run without crashing and update automatically.",
        "summary_hi": "क्लाउड सर्वर (जैसे AWS) को संभालता है ताकि वेबसाइट कभी बंद न हो और नए बदलाव तुरंत इंटरनेट पर लाइव हो सकें।"
    },
    "Senior Data Scientist": {
        "title": "Senior Data Scientist",
        "title_hi": "वरिष्ठ डेटा साइंटिस्ट (Data Scientist)",
        "category": "Data Science",
        "category_hi": "डेटा साइंस",
        "min_experience_years": 4,
        "required_education": ["master", "phd", "bachelor", "statistics", "mathematics"],
        "primary_skills": [
            "python", "sql", "machine learning", "pandas", "numpy", "scikit-learn", 
            "data analysis", "data visualization", "statistics", "feature engineering"
        ],
        "secondary_skills": [
            "deep learning", "tableau", "power bi", "bigquery", "apache spark", "git", "nlp"
        ],
        "salary_range": {"min": 120000, "median": 150000, "max": 190000, "currency": "USD", "inr_lpa_min": 14, "inr_lpa_max": 32},
        "summary": "Studies company data and charts to discover patterns, predict user behavior, and help make profitable business choices.",
        "summary_hi": "कंपनी के डेटा का विश्लेषण करके महत्वपूर्ण रुझान खोजता है और बेहतर निर्णय लेने में मदद करता है।"
    },
    "Cybersecurity Specialist": {
        "title": "Cybersecurity Specialist",
        "title_hi": "साइबर सुरक्षा विशेषज्ञ (Cybersecurity)",
        "category": "Information Security",
        "category_hi": "सूचना सुरक्षा",
        "min_experience_years": 3,
        "required_education": ["bachelor", "cybersecurity", "computer science"],
        "primary_skills": [
            "network security", "penetration testing", "siem", "wireshark", "linux", 
            "owasp", "incident response", "vulnerability assessment", "python"
        ],
        "secondary_skills": [
            "soc", "cryptography", "iam", "cloud security", "docker", "bash", "cissp"
        ],
        "salary_range": {"min": 110000, "median": 140000, "max": 175000, "currency": "USD", "inr_lpa_min": 11, "inr_lpa_max": 26},
        "summary": "Protects company servers and confidential user data from hackers, malicious bugs, and unauthorized access.",
        "summary_hi": "कंपनी के कंप्यूटर, नेटवर्क और डेटा को हैकर्स व साइबर हमलों से सुरक्षित रखता है।"
    },
    "Backend Systems Engineer": {
        "title": "Backend Systems Engineer",
        "title_hi": "बैकएंड सिस्टम्स इंजीनियर (Backend Systems)",
        "category": "Software Engineering",
        "category_hi": "सॉफ्टवेयर इंजीनियरिंग",
        "min_experience_years": 3,
        "required_education": ["bachelor", "computer science"],
        "primary_skills": [
            "python", "go", "java", "fastapi", "postgresql", "redis", 
            "rest api", "microservices", "docker", "git", "system design"
        ],
        "secondary_skills": [
            "grpc", "kafka", "kubernetes", "aws", "unit testing", "ci/cd", "mongodb"
        ],
        "salary_range": {"min": 115000, "median": 145000, "max": 180000, "currency": "USD", "inr_lpa_min": 12, "inr_lpa_max": 29},
        "summary": "Focuses on the database, server architecture, and lightning-fast APIs that power modern apps behind the scenes.",
        "summary_hi": "सर्वर की स्पीड, डेटाबेस और अंदरूनी प्रोग्राम्स को सुपर-फास्ट और मजबूत बनाने का काम करता है।"
    }
}
