"""
Automated Learning Resource Recommendation Engine
Provides easy-to-understand free learning paths, documentation, and practice ideas
for missing skills identified in the resume in both English and Hindi.
"""
from typing import Dict, List, Any

# Curated skill learning knowledgebase with simple, human-friendly wording and Hindi translations
SKILL_RESOURCES: Dict[str, Dict[str, Any]] = {
    "kubernetes": {
        "title": "Learn Kubernetes (K8s) Step-by-Step",
        "title_hi": "कुबेरनेट्स (Kubernetes) सीखें",
        "provider": "Linux Foundation / freeCodeCamp",
        "url": "https://kubernetes.io/docs/home/",
        "level": "Intermediate",
        "level_hi": "मध्यम स्तर",
        "duration": "3-4 weeks",
        "duration_hi": "3-4 सप्ताह",
        "project": "Deploy a multi-service web app on cloud servers with automatic scaling.",
        "project_hi": "क्लाउड सर्वर पर एक वेब ऍप डिप्लॉय करें जो जरूरत पड़ने पर खुद बड़ा हो सके।"
    },
    "docker": {
        "title": "Docker for Beginners: Container Basics",
        "title_hi": "डॉकर (Docker) सीखें: कंटेनर बेसिक्स",
        "provider": "Docker Official / freeCodeCamp",
        "url": "https://docs.docker.com/get-started/",
        "level": "Beginner",
        "level_hi": "शुरुआती स्तर",
        "duration": "1-2 weeks",
        "duration_hi": "1-2 सप्ताह",
        "project": "Package your web project into a Docker container so it runs anywhere without errors.",
        "project_hi": "अपने वेब प्रोजेक्ट को डॉकर में पैक करें ताकि वह किसी भी कंप्यूटर पर बिना एरर चले।"
    },
    "aws": {
        "title": "AWS Cloud Foundations & Essentials",
        "title_hi": "एडब्ल्यूएस (AWS) क्लाउड फंडामेंटल्स",
        "provider": "AWS Training & Certification",
        "url": "https://aws.amazon.com/training/",
        "level": "Beginner to Intermediate",
        "level_hi": "शुरुआती से मध्यम",
        "duration": "3-4 weeks",
        "duration_hi": "3-4 सप्ताह",
        "project": "Host a live website with database and cloud storage on Amazon Web Services.",
        "project_hi": "अमेज़ॉन वेब सर्विसेज पर एक लाइव वेबसाइट और डेटाबेस होस्ट करें।"
    },
    "terraform": {
        "title": "Terraform: Automated Cloud Infrastructure",
        "title_hi": "टेराफॉर्म (Terraform) सीखें: कोड से क्लाउड बनाएं",
        "provider": "HashiCorp Official",
        "url": "https://developer.hashicorp.com/terraform/tutorials",
        "level": "Intermediate",
        "level_hi": "मध्यम स्तर",
        "duration": "2-3 weeks",
        "duration_hi": "2-3 सप्ताह",
        "project": "Set up cloud servers automatically using simple code files.",
        "project_hi": "कोड फाइलों का उपयोग करके स्वचालित रूप से क्लाउड सर्वर तैयार करें।"
    },
    "pytorch": {
        "title": "PyTorch for Deep Learning & Neural Networks",
        "title_hi": "पाइटॉर्च (PyTorch) सीखें: डीप लर्निंग",
        "provider": "DeepLearning.AI / PyTorch Org",
        "url": "https://pytorch.org/tutorials/",
        "level": "Intermediate",
        "level_hi": "मध्यम स्तर",
        "duration": "4 weeks",
        "duration_hi": "4 सप्ताह",
        "project": "Train an image recognition or text classifier AI model with PyTorch.",
        "project_hi": "पाइटॉर्च का उपयोग करके फोटो पहचानने या टेक्स्ट का विश्लेषण करने वाला एआई मॉडल बनाएं।"
    },
    "tensorflow": {
        "title": "TensorFlow Machine Learning Crash Course",
        "title_hi": "टेंसरफ्लो (TensorFlow) मशीन लर्निंग गाइड",
        "provider": "Google TensorFlow / Coursera",
        "url": "https://www.tensorflow.org/tutorials",
        "level": "Intermediate",
        "level_hi": "मध्यम स्तर",
        "duration": "4 weeks",
        "duration_hi": "4 सप्ताह",
        "project": "Build and test a predictive AI model using TensorFlow and Keras.",
        "project_hi": "टेंसरफ्लो से डेटा के आधार पर भविष्यवाणी करने वाला मॉडल बनाएं।"
    },
    "llm": {
        "title": "AI & Large Language Models (LLMs) Guide",
        "title_hi": "लार्ज लैंग्वेज मॉडल्स (LLMs) और जनरेटिव एआई",
        "provider": "DeepLearning.AI",
        "url": "https://www.deeplearning.ai/courses/generative-ai-with-llms/",
        "level": "Intermediate",
        "level_hi": "मध्यम स्तर",
        "duration": "2-3 weeks",
        "duration_hi": "2-3 सप्ताह",
        "project": "Build an intelligent chatbot that answers questions from your own PDF documents.",
        "project_hi": "एक स्मार्ट चैटबॉट बनाएं जो आपके अपने पीडीएफ डॉक्यूमेंट्स पढ़कर उत्तर दे।"
    },
    "fastapi": {
        "title": "FastAPI: Fast Python Web APIs",
        "title_hi": "फास्टएपीआई (FastAPI): सुपर-फास्ट पायथन बैकएंड",
        "provider": "FastAPI Official Docs",
        "url": "https://fastapi.tiangolo.com/tutorial/",
        "level": "Beginner",
        "level_hi": "शुरुआती स्तर",
        "duration": "1-2 weeks",
        "duration_hi": "1-2 सप्ताह",
        "project": "Create a clean backend API with user login, data validation, and automated Swagger docs.",
        "project_hi": "यूजर लॉगिन और डेटाबेस के साथ एक सुरक्षित और तेज बैकएंड सर्वर तैयार करें।"
    },
    "react": {
        "title": "Modern React & Web App Development",
        "title_hi": "मॉडर्न रिएक्ट (React) सीखें: शानदार वेबसाइट बनाएं",
        "provider": "React Official Docs / freeCodeCamp",
        "url": "https://react.dev/learn",
        "level": "Beginner",
        "level_hi": "शुरुआती स्तर",
        "duration": "3 weeks",
        "duration_hi": "3 सप्ताह",
        "project": "Build an interactive, responsive web dashboard with clean UI components.",
        "project_hi": "एक सुंदर और इंटरेक्टिव वेब डैशबोर्ड तैयार करें।"
    },
    "typescript": {
        "title": "TypeScript Basics & Safe JavaScript",
        "title_hi": "टाइपस्क्रिप्ट (TypeScript) सीखें: सुरक्षित कोड",
        "provider": "Microsoft TypeScript Docs",
        "url": "https://www.typescriptlang.org/docs/",
        "level": "Beginner to Intermediate",
        "level_hi": "शुरुआती से मध्यम",
        "duration": "2 weeks",
        "duration_hi": "2 सप्ताह",
        "project": "Add type safety to a JavaScript app to prevent common bugs and crashes.",
        "project_hi": "जावास्क्रिप्ट प्रोजेक्ट में टाइप सुरक्षा जोड़कर कोड में गलतियों को रोकें।"
    },
    "redis": {
        "title": "Redis Fast In-Memory Caching",
        "title_hi": "रेडिस (Redis) सीखें: सुपर-फास्ट कैशिंग",
        "provider": "Redis University",
        "url": "https://university.redis.io/",
        "level": "Beginner to Intermediate",
        "level_hi": "शुरुआती से मध्यम",
        "duration": "1-2 weeks",
        "duration_hi": "1-2 सप्ताह",
        "project": "Speed up website database lookups by storing frequent queries in Redis memory.",
        "project_hi": "रेडिस का उपयोग करके वेबसाइट की स्पीड 5 गुना तेज करें।"
    },
    "postgresql": {
        "title": "PostgreSQL & Relational Database Essentials",
        "title_hi": "पोस्टग्रेएसक्यूएल (PostgreSQL) डेटाबेस गाइड",
        "provider": "PostgreSQL Official Docs",
        "url": "https://www.postgresql.org/docs/",
        "level": "Beginner",
        "level_hi": "शुरुआती स्तर",
        "duration": "2-3 weeks",
        "duration_hi": "2-3 सप्ताह",
        "project": "Design clean tables, write SQL queries, and link them to your web backend.",
        "project_hi": "टेबल्स बनाएं, तेज SQL क्वेरी लिखें और अपने वेब बैकएंड से जोड़ें।"
    },
    "ci/cd": {
        "title": "GitHub Actions & Automated Testing (CI/CD)",
        "title_hi": "गिटहब एक्शन्स और ऑटोमेशन (CI/CD)",
        "provider": "GitHub Skills",
        "url": "https://docs.github.com/en/actions",
        "level": "Beginner to Intermediate",
        "level_hi": "शुरुआती से मध्यम",
        "duration": "1 week",
        "duration_hi": "1 सप्ताह",
        "project": "Automatically test and deploy your code whenever you push to GitHub.",
        "project_hi": "गिटहब पर कोड अपलोड होते ही अपने आप टेस्टिंग और डिप्लॉयमेंट सेट करें।"
    },
    "system design": {
        "title": "System Design: Building Scalable Websites",
        "title_hi": "सिस्टम डिजाइन: बड़े पैमाने की वेबसाइट्स का आर्किटेक्चर",
        "provider": "System Design Primer",
        "url": "https://github.com/donnemartin/system-design-primer",
        "level": "Intermediate",
        "level_hi": "मध्यम स्तर",
        "duration": "3-4 weeks",
        "duration_hi": "3-4 सप्ताह",
        "project": "Draw architecture diagrams for a high-traffic app like Instagram or Twitter.",
        "project_hi": "लाखों यूजर्स को संभालने वाली वेबसाइट (जैसे इंस्टाग्राम) का आर्किटेक्चर समझें और बनाएं।"
    }
}

class RecommendationEngine:
    @staticmethod
    def get_recommendations_for_missing_skills(missing_skills: List[str], max_results: int = 6) -> List[Dict[str, Any]]:
        """
        Matches missing skill list against curated learning courses and generates custom learning roadmap.
        """
        recommendations = []
        lower_missing = [s.lower() for s in missing_skills]

        for skill in lower_missing:
            matched_key = None
            if skill in SKILL_RESOURCES:
                matched_key = skill
            else:
                for key in SKILL_RESOURCES:
                    if key in skill or skill in key:
                        matched_key = key
                        break

            if matched_key:
                info = SKILL_RESOURCES[matched_key]
                recommendations.append({
                    "skill": skill.title(),
                    "title": info["title"],
                    "title_hi": info.get("title_hi", f"{skill.title()} सीखें"),
                    "provider": info["provider"],
                    "url": info["url"],
                    "level": info["level"],
                    "level_hi": info.get("level_hi", "मध्यम"),
                    "duration": info["duration"],
                    "duration_hi": info.get("duration_hi", "2-3 सप्ताह"),
                    "capstone_project": info["project"],
                    "capstone_project_hi": info.get("project_hi", f"{skill.title()} पर एक छोटा प्रैक्टिस प्रोजेक्ट बनाएं।")
                })
            else:
                recommendations.append({
                    "skill": skill.title(),
                    "title": f"Learn {skill.title()} (Tutorials & Official Guide)",
                    "title_hi": f"{skill.title()} सीखें: ट्यूटोरियल व गाइड",
                    "provider": f"Official {skill.title()} Community Guides",
                    "url": f"https://www.google.com/search?q={skill.replace(' ', '+')}+tutorial+for+beginners",
                    "level": "Beginner to Intermediate",
                    "level_hi": "शुरुआती से मध्यम",
                    "duration": "2 weeks",
                    "duration_hi": "2 सप्ताह",
                    "project": f"Build a small hands-on project using {skill.title()} to add to your resume.",
                    "project_hi": f"अपने रिज्यूमे में जोड़ने के लिए {skill.title()} का उपयोग करके एक छोटा प्रोजेक्ट बनाएं।"
                })

            if len(recommendations) >= max_results:
                break

        return recommendations

recommendation_engine = RecommendationEngine()
