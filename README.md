# Intelligent Recruitment and Candidate Matching System Using Multi-Source Profile Analysis

An AI-powered, explainable recruitment and candidate matching platform that analyzes software engineering candidates using verifiable multi-source profile intelligence rather than relying on unverified resumes alone.

---

## 1. Project Overview & Problem Statement

Traditional Applicant Tracking Systems (ATS) rely almost exclusively on parsing static text from resume files. This creates significant problems:
1. **Keyword Stuffing**: Candidates can inflate resumes with keywords they do not actually understand or apply.
2. **Lack of Verifiable Evidence**: Conventional resumes state skills without connecting them to measurable public artifacts (repositories, solved algorithmic problems, competitive modeling, or deployed portfolios).
3. **Black-Box AI Decisions**: Many modern platforms use opaque machine learning models that generate arbitrary scores without transparent, deterministic explanations.

### The Solution: Recruit360
Recruit360 is a transparent **recruitment-support and candidate-analysis system** (not an autonomous decision engine) that constructs a unified **Candidate 360° Profile**. It aggregates and analyzes evidence across:
* **Resume**: Extracted via PyMuPDF / python-docx (contact, education, work history, skill keywords, structural sections).
* **GitHub**: Public repositories, programming languages, commit activity, topics, and framework detection.
* **LeetCode**: Public algorithmic stats (Easy, Medium, Hard problem counts and DSA competencies).
* **Kaggle**: Data science competitions, public notebooks, and machine learning models.
* **Portfolio Websites**: Public HTML extraction of about sections, skills, and deployed web apps.
* **LinkedIn, HackerRank, CodeChef, GeeksforGeeks**: Transparent profile storage and compliant linking.

---

## 2. Key Features

* **Candidate 360° Profile**: Unified view linking every detected competency back to verifiable multi-source proof (Resume ✓, GitHub ✓, LeetCode ✓, Portfolio ✓).
* **Multi-Source Skill Evidence**: A dedicated relational evidence table tracking source types, confidence, and contextual snippets.
* **Explainable ATS Scoring Engine**: Calculates deterministic scores based on 5 weighted pillars:
  $$\text{ATS Score} = (0.40 \times \text{Skill}) + (0.20 \times \text{Keyword}) + (0.15 \times \text{Exp}) + (0.15 \times \text{Edu}) + (0.10 \times \text{Structure})$$
* **Job Matching Engine**: Combines set-theoretic skill overlap and NLP TF-IDF cosine similarity:
  $$\text{Job Match Score} = (0.70 \times \text{Skill Overlap}) + (0.30 \times \text{TF-IDF Cosine Similarity})$$
* **Target Skill Gap Analysis**:
  $$\text{Missing Skills} = \text{Required Job Skills} - \text{Candidate Verified Skills}$$
* **Personalized Learning Roadmaps**: Actionable 3-week study pathways with weekly milestones and capstone practice projects for every missing skill.
* **Role-Based Portals**:
  * **Candidate**: Resume parsing, profile management, job discovery, ATS evaluation, skill gap remediation, application tracking.
  * **Recruiter**: Job posting with automatic NLP requirement extraction, candidate screening/ranking, 360° candidate review, and application status updates with audit logs.

---

## 3. System Architecture

```text
                    CANDIDATE
                        |
        +---------------+----------------+
        |               |                |
      Resume       Professional       Coding
                     Profiles          Profiles
        |               |                |
        |        +------+-------+   +----+-----+
        |        |      |       |   |    |     |
        |     LinkedIn GitHub Portfolio LeetCode
        |                         Kaggle HackerRank
        |                              CodeChef
        |                              GFG
        +---------------+----------------+
                        |
                DATA NORMALIZATION
                        |
                 SKILL EXTRACTION
                        |
              CANDIDATE 360 PROFILE
                        |
                JOB DESCRIPTION (NLP)
                        |
                 MATCHING ENGINE
                        |
        +---------------+----------------+
        |               |                |
      ATS Score      Job Match       Skill Gap
        |               |                |
        +---------------+----------------+
                        |
               LEARNING ROADMAP
```

---

## 4. Technology Stack

* **Backend**: Python 3.11+, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug
* **NLP & Data Analysis**: scikit-learn (`TfidfVectorizer`, `cosine_similarity`), numpy, PyMuPDF (`fitz`), python-docx, BeautifulSoup4
* **Database**: MySQL (production-ready) with automatic SQLite fallback (`instance/recruitment.db`)
* **Frontend**: HTML5, CSS3, Bootstrap 5, Bootstrap Icons, JavaScript
* **Testing**: pytest (20 automated unit and integration tests)

---

## 5. Project Directory Structure

```text
├── app.py                     # Flask application factory and server entrypoint
├── config.py                  # Environment and database configuration (MySQL / SQLite fallback)
├── requirements.txt           # Python package dependencies
├── .env                       # Environment configuration
├── .env.example               # Template for environment variables
├── seed.py                    # Database seeding with realistic candidate & recruiter records
├── README.md                  # Comprehensive technical documentation
│
├── models/                    # SQLAlchemy database models
│   ├── __init__.py            # DB initialization and model exports
│   ├── user.py                # User account and password hashing
│   ├── candidate.py           # Candidate profile details
│   ├── recruiter.py           # Recruiter and company profiles
│   ├── profile.py             # Education, Experience, Project, Certification
│   ├── resume.py              # Uploaded resumes and parsed JSON payloads
│   ├── skill.py               # Skill taxonomy, CandidateSkill, and SkillEvidence
│   ├── job.py                 # Job postings, required and preferred skills
│   ├── application.py         # Job applications and status audit history
│   ├── external_profile.py    # Multi-source integrations (GitHub, LeetCode, etc.)
│   └── roadmap.py             # SkillGap and personalized Learning Roadmaps
│
├── routes/                    # Modular Flask Blueprints
│   ├── __init__.py            # Blueprint registry
│   ├── auth.py                # Registration, Login, Logout, and Role Decorators
│   ├── candidate.py           # Candidate Dashboard, 360°, ATS, and Profiles
│   ├── recruiter.py           # Recruiter Dashboard, Job creation, Candidate detail
│   ├── jobs.py                # Public & Candidate job search and comparison
│   ├── applications.py        # Application submission and candidate tracker
│   ├── resume.py              # Resume upload and parsing
│   ├── profiles.py            # External profile connection and analysis
│   └── api.py                 # Protected JSON endpoints
│
├── services/                  # Core Business & NLP Logic
│   ├── resume_parser.py       # PDF, DOCX, TXT parser with regex and PyMuPDF
│   ├── skill_extractor.py     # Boundary-aware keyword & taxonomy matcher
│   ├── skill_normalizer.py    # 250+ skill alias and canonical mapper
│   ├── ats_engine.py          # Deterministic 5-pillar ATS calculation
│   ├── matching_engine.py     # 70% skill overlap + 30% TF-IDF cosine similarity
│   ├── recommendation_engine.py # Candidate job recommendation ranker
│   ├── roadmap_engine.py      # Weekly learning roadmap synthesis
│   ├── job_description_analyzer.py # NLP JD requirements extractor
│   ├── candidate_profile_aggregator.py # Unified Candidate 360° builder
│   │
│   └── profile_sources/       # Multi-source profile adapters
│       ├── __init__.py
│       ├── github_service.py  # Public GitHub repository and language analyzer
│       ├── linkedin_service.py # Transparent URL link handler (privacy-compliant)
│       ├── leetcode_service.py # LeetCode GraphQL stats parser
│       ├── kaggle_service.py  # Kaggle public competition/notebook parser
│       ├── hackerrank_service.py # HackerRank profile adapter
│       ├── codechef_service.py   # CodeChef profile adapter
│       ├── geeksforgeeks_service.py # GeeksforGeeks adapter
│       └── portfolio_service.py # Safe public HTML parser
│
├── data/
│   ├── skills.json            # 250+ technical skills taxonomy with aliases
│   └── roadmap_data.json      # Structured weekly learning curriculum
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Base layout with navbar, alerts, footer
│   ├── index.html             # Landing page with architecture & job cards
│   ├── auth/                  # Login, candidate registration, recruiter registration
│   ├── candidate/             # Dashboard, 360°, Resume, ATS, Jobs, Roadmaps
│   ├── recruiter/             # Dashboard, Create Job, Screening Queue, Review
│   └── errors/                # Custom 403, 404, 500 pages
│
├── static/
│   ├── css/style.css          # Modern dashboard styling and badges
│   └── js/app.js              # Client-side interactions
│
├── uploads/                   # Secure candidate resume file storage
└── tests/                     # Automated pytest suite
    ├── conftest.py            # Fixtures (app, client, candidate, recruiter)
    ├── test_auth.py           # Authentication and authorization tests
    ├── test_resume.py         # PDF, DOCX, TXT extraction tests
    ├── test_skills.py         # Normalization and evidence tests
    ├── test_ats.py            # ATS 5-pillar formula verification
    ├── test_matching.py       # TF-IDF and skill overlap tests
    ├── test_jobs.py           # Job posting and status toggle tests
    ├── test_applications.py   # Applications and audit history tests
    └── test_profiles.py       # Multi-source adapter tests
```

---

## 6. Installation & Setup

### A. Windows (PowerShell)

```powershell
# 1. Clone repository or navigate to project directory
cd intelligent_recruitment_system

# 2. Create virtual environment
python -m venv venv

# If execution policy blocks script execution, run:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 4. Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. Populate database with demo accounts and taxonomy
python seed.py

# 6. Run test suite
pytest

# 7. Start the application
python app.py
```

### B. Linux / macOS (Bash)

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Populate database with demo accounts
python3 seed.py

# 4. Run test suite
python3 -m pytest tests/ -v

# 5. Start the application
python3 app.py
```

The application will start on:
```text
http://127.0.0.1:5000/
```

---

## 7. Demo Credentials

The database seeder (`seed.py`) configures two ready-to-test demo accounts:

| Role | Email | Password | Features Accessible |
|---|---|---|---|
| **Candidate** | `candidate@example.com` | `Candidate@123` | Candidate 360°, ATS scoring, Job Applications, Skill Gap, Roadmaps |
| **Recruiter** | `recruiter@example.com` | `Recruiter@123` | Post Jobs, NLP JD Analyzer, Candidate Screening Queue, 360° Candidate Review |

---

## 8. Database Configuration (MySQL & SQLite)

The system automatically supports MySQL with seamless SQLite fallback.

To use MySQL, set the following in your `.env`:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=intelligent_recruitment
```

If MySQL is unavailable or unconfigured, the application automatically uses SQLite:
```env
DATABASE_URL=sqlite:///recruitment.db
```

---

## 9. Verification & Test Results

Run all unit and integration tests with:
```bash
pytest tests/ -v
```

All 20 test cases pass with 100% success:
* `test_auth.py`: Candidate registration, recruiter registration, duplicate email rejection, login/logout, role isolation (403 forbidden).
* `test_resume.py`: PDF, DOCX, TXT extraction, section detection, invalid format rejection.
* `test_skills.py`: Taxonomy normalization (e.g. `reactjs` $\to$ `React`, `sklearn` $\to$ `Scikit-learn`), multi-source evidence linking.
* `test_ats.py`: 5-pillar ATS mathematical formula verification, breakdown accuracy, and explainable feedback.
* `test_matching.py`: Skill overlap calculation and TF-IDF cosine similarity.
* `test_jobs.py`: Job creation, editing, publishing, unpublishing, closing.
* `test_applications.py`: Duplicate application prevention, status updating, audit history timeline.
* `test_profiles.py`: Privacy-compliant LinkedIn handling, Kaggle/LeetCode adapters, connection and deletion.

---

## 10. Security & Ethical Boundaries

* **No Illegal Web Scraping**: The system does not bypass CAPTCHAs, authentication barriers, or platform terms of service. Platforms that do not provide permitted open APIs display honest notices (`Profile linked. Automatic analysis unavailable for this source.`).
* **Upload Sanitization**: Uploaded files are verified by extension (`.pdf`, `.docx`, `.txt`), assigned randomized UUID filenames, and saved in an isolated directory. Executable uploads are strictly rejected.
* **SQL Injection & XSS Protection**: All queries are executed via SQLAlchemy ORM with parameterized binding; all user output is escaped in Jinja2 templates.
* **Decision Support, Not Autonomous Decisions**: The system is transparently engineered as an explainable decision-support tool. It makes no claims of measuring personality or guaranteeing hiring success.
