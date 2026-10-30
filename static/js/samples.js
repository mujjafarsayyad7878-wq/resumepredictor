/**
 * Pre-configured Sample Resumes and Benchmark Job Profiles for 1-Click Testing
 */
const SAMPLE_PROFILES = {
    fullstack: {
        role: "Senior Full Stack Developer",
        title: "Senior Full Stack Engineer (Alex Chen)",
        resumeText: `ALEXANDER CHEN
alex.chen.dev@gmail.com | (555) 382-9102 | San Francisco, CA
LinkedIn: linkedin.com/in/alexchen-dev | GitHub: github.com/alexchen-fullstack

PROFESSIONAL SUMMARY
Senior Full Stack Engineer with 6+ years of experience engineering high-scale web platforms, distributed cloud microservices, and reactive user interfaces. Proven track record migrating monolithic architectures to containerized microservices and optimizing PostgreSQL query latencies by 42%.

EDUCATION
Master of Science in Computer Science - University of California, Berkeley (2018)
Bachelor of Science in Software Engineering - University of Washington (2016)

TECHNICAL SKILLS
- Programming Languages: Python, JavaScript, TypeScript, Go, SQL, HTML5, CSS3
- Frontend: React, Next.js, Redux, Tailwind CSS, Responsive Design, Webpack, Vite
- Backend & APIs: FastAPI, Node.js, Express, REST APIs, Microservices, GraphQL, Celery
- Databases: PostgreSQL, Redis, MongoDB, SQLAlchemy
- Cloud & DevOps: Docker, AWS (EC2, S3, RDS), GitHub Actions, CI/CD, Linux, Nginx
- Engineering: System Design, Git, Agile, Scrum, Unit Testing, PyTest, Jest

PROFESSIONAL EXPERIENCE

Senior Software Engineer | CloudScale Systems (2021 – Present)
- Architected and delivered resilient customer dashboard using React, TypeScript, and FastAPI serving 1.8M active monthly users.
- Redesigned backend persistence layer utilizing PostgreSQL and Redis caching, cutting P99 API response times from 450ms to 65ms.
- Implemented automated CI/CD deployment pipelines using GitHub Actions and Docker, reducing build-to-production cycles by 60%.
- Led cross-functional team of 6 engineers across sprint planning, system design reviews, and TDD code reviews.

Full Stack Web Developer | InnovateTech Labs (2018 – 2021)
- Developed responsive web interfaces using React, Redux, and Tailwind CSS.
- Built scalable RESTful microservices with Node.js, Express, and MongoDB.
- Created unit and integration test suites using Jest and PyTest, achieving 88% test coverage.
- Integrated Stripe billing and Webhook event listeners for automated subscription lifecycle management.`
    },

    aiml: {
        role: "AI / Machine Learning Engineer",
        title: "AI / ML Engineer (Dr. Elena Rostova)",
        resumeText: `DR. ELENA ROSTOVA
elena.rostova.ai@gmail.com | (555) 714-8839 | Seattle, WA
LinkedIn: linkedin.com/in/elena-rostova-ml | GitHub: github.com/erostova-ai

PROFESSIONAL SUMMARY
AI/Machine Learning Engineer with 4+ years of specialized experience training, fine-tuning, and deploying deep learning and NLP architectures. Passionate about Retrieval-Augmented Generation (RAG), Transformers, and high-throughput model inference pipelines.

EDUCATION
Ph.D. in Computer Science (Artificial Intelligence) - Stanford University (2020)
Bachelor of Science in Mathematics & Statistics - University of Michigan (2016)

TECHNICAL SKILLS
- Languages: Python, C++, SQL, Bash
- AI & Deep Learning: PyTorch, TensorFlow, Keras, Scikit-learn, Transformers, Hugging Face, OpenCV
- Generative AI & NLP: Large Language Models (LLM), RAG, LangChain, spaCy, NLTK, Vector Databases, ChromaDB
- Data Engineering & Math: Pandas, NumPy, SciPy, Matplotlib, Feature Engineering, Statistics
- Deployment & MLOps: Docker, FastAPI, Git, Linux, AWS, Model Deployment, ONNX, MLflow

PROFESSIONAL EXPERIENCE

Lead Machine Learning Engineer | CogniTech AI (2021 – Present)
- Engineered enterprise RAG solution with LangChain, PyTorch, and ChromaDB vector database, improving knowledge extraction accuracy by 34%.
- Fine-tuned open-source LLM architectures (Llama 3, Mistral) using LoRA and Hugging Face Transformers for domain-specific medical summaries.
- Deployed asynchronous model inference endpoints using FastAPI and Docker, handling 500+ requests/sec with under 40ms latency.
- Built automated evaluation benchmarks comparing model hallucinations, BLEU scores, and semantic cosine similarity.

Data Scientist & ML Researcher | DeepVision Analytics (2020 – 2021)
- Developed computer vision convolutional networks in PyTorch for defect detection in industrial manufacturing.
- Implemented scikit-learn random forests and gradient boosted trees for predictive maintenance forecasting.
- Authored 3 peer-reviewed research papers in natural language processing and transformer attention mechanisms.`
    },

    devops: {
        role: "Cloud & DevOps Architect",
        title: "Cloud & DevOps Architect (Marcus Vance)",
        resumeText: `MARCUS VANCE
marcus.vance.cloud@gmail.com | (555) 902-3341 | Austin, TX
LinkedIn: linkedin.com/in/marcus-vance-devops | GitHub: github.com/mvance-cloud

PROFESSIONAL SUMMARY
Cloud Infrastructure and DevOps Architect with 7+ years of hands-on expertise building multi-region Kubernetes clusters, automated zero-downtime CI/CD workflows, and Infrastructure as Code (IaC) on AWS and Azure.

EDUCATION
Bachelor of Science in Information Technology - Texas A&M University (2017)
Certifications: AWS Certified Solutions Architect Professional, Certified Kubernetes Administrator (CKA)

TECHNICAL SKILLS
- Cloud Platforms: AWS, Azure, Google Cloud (GCP)
- Orchestration & Containers: Kubernetes (K8s), Docker, Helm, Docker Compose
- Infrastructure as Code: Terraform, Ansible, CloudFormation
- CI/CD & Automation: GitHub Actions, GitLab CI, Jenkins, ArgoCD
- Monitoring & Telemetry: Prometheus, Grafana, ELK Stack, CloudWatch
- Programming & Scripting: Python, Bash, Shell, Go, Linux administration
- Security & Standards: Zero Trust, IAM, SOC 2, OWASP, Network Security

PROFESSIONAL EXPERIENCE

Principal Cloud Architect | Apex Financial Technologies (2021 – Present)
- Designed and maintained PCI-DSS compliant AWS infrastructure spanning 3 global regions with 99.99% uptime SLA.
- Spearheaded Kubernetes cluster migration managing 140+ microservices using Terraform, Helm, and ArgoCD GitOps.
- Deployed real-time cluster telemetry monitoring stack utilizing Prometheus and Grafana dashboards with PagerDuty alerting.
- Cut annual AWS cloud spend by $280,000 via spot instance orchestration and DynamoDB auto-scaling optimizations.

Senior DevOps Engineer | NextGen Cloud Solutions (2017 – 2021)
- Automated deployment pipelines using GitHub Actions and Jenkins for 25+ development squads.
- Implemented Docker container security scanning, reducing container vulnerabilities by 75%.
- Maintained Linux infrastructure across 200+ instances with automated Ansible playbooks.`
    },

    datascientist: {
        role: "Senior Data Scientist",
        title: "Senior Data Scientist (Maya Patel)",
        resumeText: `MAYA PATEL
maya.patel.ds@gmail.com | (555) 420-7719 | New York, NY
LinkedIn: linkedin.com/in/maya-patel-data | GitHub: github.com/mayapatel-analytics

PROFESSIONAL SUMMARY
Senior Data Scientist with 5+ years of experience extracting commercial intelligence from petabyte-scale data, building predictive machine learning models, and conducting high-impact statistical A/B experimentation.

EDUCATION
Master of Science in Data Science - Columbia University (2019)
Bachelor of Science in Statistics & Economics - NYU (2017)

TECHNICAL SKILLS
- Statistical Analysis: A/B Testing, Regression, Time-Series Forecasting, Hypothesis Testing
- Programming: Python, SQL, R, Bash
- ML & Modeling: Scikit-learn, XGBoost, LightGBM, Pandas, NumPy, Feature Engineering
- Big Data & BI: Snowflake, BigQuery, Tableau, Power BI, Apache Spark
- Version Control & Tools: Git, Jupyter, Docker, Agile

PROFESSIONAL EXPERIENCE

Senior Data Scientist | FinEdge Global (2021 – Present)
- Built customer churn prediction model in Python with XGBoost and Scikit-learn, lowering client churn rate by 18%.
- Designed and executed 45+ statistical A/B tests on conversion funnels, generating $4.2M in incremental revenue.
- Created executive Snowflake and Tableau dashboards monitoring customer lifetime value (LTV) and CAC.

Data Analyst / Scientist | MarketPulse Media (2019 – 2021)
- Analyzed large relational databases utilizing advanced SQL window functions and BigQuery.
- Built automated ETL scripts in Python and Pandas to clean and merge disparate advertising performance feeds.`
    },

    hindi: {
        role: "Senior Full Stack Developer",
        title: "हिंदी रिज्यूमे (अमित शर्मा - फुल स्टैक)",
        resumeText: `अमित शर्मा
ईमेल: amit.sharma.dev@gmail.com | फोन: +91 98765 43210 | नई दिल्ली, भारत
लिंक्डइन: linkedin.com/in/amitsharma-dev | गिटहब: github.com/amitsharma

पेशेवर सारांश (Summary):
3+ वर्ष का अनुभव फुल स्टैक सॉफ्टवेयर डेवलपमेंट में। React, Python, FastAPI और PostgreSQL का उपयोग करके तेज और मजबूत वेब एप्लीकेशन्स बनाने में कुशल।

शिक्षा (Education):
बी.टेक कंप्यूटर साइंस (B.Tech in Computer Science) - दिल्ली विश्वविद्यालय (2021)

तकनीकी कौशल (Technical Skills):
- प्रोग्रामिंग भाषाएं: पायथन (Python), जावास्क्रिप्ट (JavaScript), टाइपस्क्रिप्ट (TypeScript), एचटीएमएल (HTML5), सीएसएस (CSS3)
- फ्रंटएंड: रिएक्ट (React), टेलविंड सीएसएस (Tailwind CSS), रिस्पॉन्सिव वेब डिजाइन
- बैकएंड व सर्वर: फास्टएपीआई (FastAPI), नोड.जेएस (Node.js), रेस्ट एपीआई (REST APIs)
- डेटाबेस: पोस्टग्रेएसक्यूएल (PostgreSQL), एसक्यूएल (SQL), रेडिस (Redis)
- टूल्स और क्लाउड: गिट (Git), गिटहब (GitHub), डॉकर (Docker), लिनक्स (Linux)

कार्य अनुभव (Experience):
सॉफ्टवेयर इंजीनियर | टेकइनोवेट प्राइवेट लिमिटेड (2021 – वर्तमान)
- React और FastAPI का उपयोग करके तेज और रिस्पॉन्सिव वेब डैशबोर्ड तैयार किया।
- PostgreSQL डेटाबेस क्वेरी और इंडेक्सिंग में सुधार किया जिससे स्पीड 40% बढ़ गई।
- डॉकर और गिटहब का उपयोग करके कोड टेस्टिंग और ऑटोमेशन को आसान बनाया।`
    }
};

window.SAMPLE_PROFILES = SAMPLE_PROFILES;
