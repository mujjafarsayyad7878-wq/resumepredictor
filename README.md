# Smart Resume Matcher & Career Guide | स्मार्ट रिज्यूमे प्रेडिक्टर

> A modern, free, full-stack AI web application featuring a **Python FastAPI** backend paired with an **NLP pipeline** for skill matching, skill-gap analysis, and salary estimation, paired with a sleek **dark-themed glassmorphism dashboard** built with HTML5, Tailwind CSS, and Chart.js.
> 
> **Supports both English and Hindi resumes seamlessly with automatic language detection.**

---

## 🌟 Key Highlights

### 📄 3-Page Clean Multi-Page Interface
- **Page 1: 🏠 Home & Resume Upload (होम और अपलोड)**:
  - Friendly introduction in plain words (no confusing tech jargon).
  - 3-step guide: Upload Resume &rarr; Choose Target Job &rarr; Get Free Report.
  - Drag-and-drop file uploader (PDF, TXT, MD) and paste box.
  - 1-Click quick test sample resumes (Full Stack, AI/ML, Cloud DevOps, Data Science, and **अमित शर्मा - हिंदी रिज्यूमे**).
- **Page 2: 📊 Analysis Report & Output (रिजल्ट और रिपोर्ट)**:
  - Overall Job Match Score semi-doughnut gauge with simple match tier status.
  - Candidate profile card (experience in years, seniority level, contact info).
  - Clear **Skills You Have** vs. **Skills to Learn (Skill Gap)** badges.
  - **Estimated Salary Band** (both in USD and ₹ INR Lakhs Per Annum).
  - **Skills Balance Radar Chart**.
  - **Free Learning Courses & Practice Steps** for each missing skill.
  - **Other Jobs You Fit** (alternative career recommendations).
  - Download PDF report button.
- **Page 3: 🎯 Job Roles Guide & Free Render Hosting (नौकरी गाइड और रेंडर सेटअप)**:
  - Catalog of popular tech jobs (Full Stack, AI/ML, Cloud/DevOps, Data Scientist, Cybersecurity, Backend).
  - Step-by-step guide to hosting this website for free on **Render.com**.

### 🇮🇳 Automatic Hindi Resume Detection & Hindi Output
- If a candidate uploads or pastes a resume in **Hindi** (Devanagari script), the system **automatically detects Hindi** and outputs the report in simple, natural Hindi (सरल हिंदी)!
- Extracts Hindi names, experience (e.g. `3 वर्ष का अनुभव`), education (e.g. `बी.टेक`, `मास्टर्स`), and Hindi tech skills (e.g. `पायथन`, `रिएक्ट`, `डॉकर`, `एसक्यूएल`, `फास्टएपीआई`).
- Includes a 1-click **English | हिंदी** language toggle button in the navbar.

### 💡 Simple, Everyday Language
- All dense academic jargon (such as "dual-engine TF-IDF sublinear scaling") has been replaced with plain, understandable words:
  - "Overall Match Score" (नौकरी मैच स्कोर)
  - "Skills You Have" (आपके पास मौजूद कौशल)
  - "Skills to Learn" (सीखने योग्य कौशल)
  - "Estimated Salary" (अनुमानित वेतन पैकेज)

---

## 🚀 How to Deploy on Render (100% Free Tier)

You can host this website live on the internet using **Render.com**'s free tier with zero cost:

### Method 1: Using the Pre-configured `render.yaml` Blueprint
1. Push this project code to your GitHub repository.
2. Log in to [Render.com](https://render.com) (free account).
3. On your Render Dashboard, click **New +** &rarr; **Blueprint**.
4. Connect your GitHub repository.
5. Render will automatically read `render.yaml` and configure everything.
6. Click **Apply** &mdash; your website is live in ~2 minutes!

### Method 2: Manual Web Service Setup on Render
1. Push this project code to your GitHub repository.
2. Go to [Render Dashboard](https://dashboard.render.com/) and click **New +** &rarr; **Web Service**.
3. Select your GitHub repository.
4. Set the following settings:
   - **Environment**: `Python`
   - **Plan**: `Free`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**.
6. Render will assign you a free public HTTPS web address (e.g., `https://resumepredictor.onrender.com`).

---

## 💻 Running Locally

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.13)
- Modern web browser

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Server
```bash
# On Windows
py run.py

# Or run the batch file
start_website.bat

# On Linux / macOS
python3 run.py
```

Open your browser at **http://127.0.0.1:8000**:
- 🌐 **Web Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📖 **Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📋 **Health Check**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 🧪 Running Automated Tests

Run the complete test suite:

```bash
py -m unittest discover -s tests -p "test_*.py"
```

All 11 unit and integration tests will validate:
- Text normalization & Devanagari Hindi tokenization
- Entity extraction for English and Hindi resumes
- Vectorized skill matching & score calculation
- Bilingual salary prediction (USD & INR LPA)
- Hindi end-to-end analysis & summary generation
- PDF report generation (with safe unicode handling)
- REST API integration endpoints

---

## 🏗️ Architecture & Directory Structure

```
resumepredictor/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI entrypoint & static mounting
│   ├── config.py                  # Host & $PORT configuration
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py              # REST API endpoints (/api/analyze, /api/roles, etc.)
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── preprocessor.py        # Bilingual tokenizer & language detection
│   │   ├── tfidf_engine.py        # Content similarity engine
│   │   ├── entity_extractor.py    # Name, contacts, exp & Hindi/English skill extractor
│   │   ├── skill_taxonomy.py      # 600+ skills taxonomy with Hindi transliterations
│   │   ├── career_classifier.py   # Match score, skill gap, and plain-language classifier
│   │   └── salary_predictor.py    # Compensation model (USD + INR LPA)
│   └── services/
│       ├── __init__.py
│       ├── pdf_parser.py          # PDF & file byte parser
│       ├── recommendation_engine.py # Free course & practice recommender (EN & HI)
│       ├── pdf_report_generator.py  # ReportLab PDF builder with unicode safety
│       ├── analyzer_service.py    # Central pipeline orchestrator
│       └── db_service.py          # SQLite / Postgres database service
├── static/
│   ├── css/
│   │   └── custom.css             # Glassmorphism tokens & badge glows
│   ├── js/
│   │   ├── samples.js             # Sample profiles (EN & Hindi)
│   │   └── app.js                 # Multi-page controller & I18N dictionary
│   └── index.html                 # 3-Page modern responsive dashboard
├── tests/
│   ├── test_analyzer.py           # NLP extraction & Hindi analysis unit tests
│   └── test_api.py                # FastAPI REST endpoint integration tests
├── render.yaml                    # Render Blueprint free tier deployment configuration
├── Procfile                       # Render / Heroku start command
├── requirements.txt               # Dependencies (fastapi, uvicorn, pydantic, pypdf, etc.)
├── run.py                         # Local launch script
└── README.md                      # Documentation
```

---

## 📄 License
MIT License.
