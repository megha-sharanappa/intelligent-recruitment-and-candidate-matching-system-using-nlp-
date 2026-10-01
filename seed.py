import os
import json
from datetime import datetime
from app import create_app
from models import (
    db, User, Candidate, Recruiter, CandidateProfile, Education, Experience,
    Project, Certification, Achievement, Skill, CandidateSkill, SkillEvidence,
    Job, JobSkill, JobPreferredSkill, ExternalProfile, ExternalProfileData, ProfessionalLink, Application
)
from services.skill_normalizer import SkillNormalizer

def seed_database():
    app = create_app()
    with app.app_context():
        print("🌱 Seeding database tables...")
        db.create_all()

        normalizer = SkillNormalizer()

        # Seed Skills from taxonomy
        skills_file = os.path.join(os.path.dirname(__file__), 'data', 'skills.json')
        if os.path.exists(skills_file):
            with open(skills_file, 'r', encoding='utf-8') as f:
                tax = json.load(f)
                for item in tax.get('skills', []):
                    name = item.get('name')
                    cat = item.get('category', 'General')
                    if name and not Skill.query.filter_by(name=name).first():
                        db.session.add(Skill(name=name, category=cat, normalized_name=name))
            db.session.commit()
            print(f"✓ Skills taxonomy seeded ({Skill.query.count()} total skills).")

        # 1. Create Demo Recruiter
        recruiter_email = "recruiter@example.com"
        recruiter_user = User.query.filter_by(email=recruiter_email).first()
        if not recruiter_user:
            recruiter_user = User(email=recruiter_email, role='recruiter')
            recruiter_user.set_password("Recruiter@123")
            db.session.add(recruiter_user)
            db.session.flush()

            recruiter = Recruiter(
                user_id=recruiter_user.id,
                full_name="Sarah Miller",
                company_name="Apex Cloud Technologies",
                company_description="Leading enterprise cloud & distributed systems infrastructure provider.",
                website="https://apexcloud.example.com",
                location="San Francisco, CA",
                contact_email=recruiter_email
            )
            db.session.add(recruiter)
            db.session.flush()
            print("✓ Demo recruiter created: recruiter@example.com / Recruiter@123")
        else:
            recruiter = recruiter_user.recruiter

        # 2. Create Demo Jobs
        jobs_data = [
            {
                "title": "Senior Python Backend Developer",
                "description": "We are seeking a senior Python software engineer to design and scale distributed microservices, develop robust RESTful APIs, and manage scalable database layers.",
                "responsibilities": "Architect high-throughput services using Flask and FastAPI.\nDesign relational database schemas and optimize PostgreSQL queries.\nImplement CI/CD automated test pipelines and containerize services with Docker.",
                "requirements": "Bachelor's degree in Computer Science or equivalent.\n3+ years experience with Python, SQL, and REST APIs.\nDemonstrated proficiency in Docker, Git, and automated testing.",
                "experience_level": "Senior Level",
                "min_years_exp": 3.0,
                "location": "Remote / San Francisco, CA",
                "job_type": "Full-Time",
                "salary_range": "$135,000 - $165,000 / yr",
                "required_skills": ["Python", "Flask", "SQL", "REST API", "Git", "Docker"],
                "preferred_skills": ["AWS", "Redis", "PostgreSQL", "FastAPI"]
            },
            {
                "title": "Full Stack Engineer (React & Node.js)",
                "description": "Join our product engineering squad building interactive data dashboards and responsive SaaS web applications.",
                "responsibilities": "Develop reusable React UI components with Tailwind CSS.\nIntegrate REST & GraphQL backend services.\nEnsure state performance and accessibility standards.",
                "requirements": "2+ years of full stack web engineering experience.\nProficiency with modern JavaScript/TypeScript, React, Node.js, and SQL.",
                "experience_level": "Mid Level",
                "min_years_exp": 2.0,
                "location": "New York, NY (Hybrid)",
                "job_type": "Full-Time",
                "salary_range": "$115,000 - $140,000 / yr",
                "required_skills": ["JavaScript", "TypeScript", "React", "Node.js", "HTML", "CSS"],
                "preferred_skills": ["GraphQL", "Docker", "PostgreSQL", "Tailwind CSS"]
            },
            {
                "title": "Machine Learning Engineer",
                "description": "Develop and deploy scalable machine learning models for natural language processing, semantic matching, and predictive recommendation systems.",
                "responsibilities": "Build data ingestion and feature engineering pipelines.\nTrain, evaluate, and tune machine learning classifiers using Scikit-learn and PyTorch.\nContainerize and deploy inference microservices.",
                "requirements": "Degree in Computer Science, Data Science, or related quantitative discipline.\nHands-on experience with Python, Pandas, NumPy, and Scikit-learn.",
                "experience_level": "Mid Level",
                "min_years_exp": 2.5,
                "location": "Remote",
                "job_type": "Full-Time",
                "salary_range": "$130,000 - $160,000 / yr",
                "required_skills": ["Python", "Machine Learning", "Scikit-learn", "Pandas", "NumPy", "SQL"],
                "preferred_skills": ["PyTorch", "TensorFlow", "Docker", "Natural Language Processing"]
            },
            {
                "title": "DevOps & Cloud Infrastructure Engineer",
                "description": "Drive cloud migration, Kubernetes container orchestration, and continuous integration pipelines for our core platform.",
                "responsibilities": "Manage AWS cloud infrastructure using Terraform.\nMaintain Kubernetes clusters and Helm deployments.\nAutomate CI/CD pipelines with GitHub Actions.",
                "requirements": "Strong foundation in Linux systems administration, Docker, and AWS.",
                "experience_level": "Senior Level",
                "min_years_exp": 3.0,
                "location": "Seattle, WA or Remote",
                "job_type": "Full-Time",
                "salary_range": "$140,000 - $175,000 / yr",
                "required_skills": ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD", "Linux"],
                "preferred_skills": ["Prometheus", "Grafana", "Python", "Go"]
            }
        ]

        for jd in jobs_data:
            existing_job = Job.query.filter_by(title=jd["title"], recruiter_id=recruiter.id).first()
            if not existing_job:
                job = Job(
                    recruiter_id=recruiter.id,
                    title=jd["title"],
                    company_name=recruiter.company_name,
                    description=jd["description"],
                    responsibilities=jd["responsibilities"],
                    requirements=jd["requirements"],
                    experience_level=jd["experience_level"],
                    min_years_exp=jd["min_years_exp"],
                    education_required="Bachelor's Degree in Computer Science or related field",
                    location=jd["location"],
                    job_type=jd["job_type"],
                    salary_range=jd["salary_range"],
                    is_published=True
                )
                db.session.add(job)
                db.session.flush()

                for req_s in jd["required_skills"]:
                    norm_s = normalizer.normalize(req_s)
                    db.session.add(JobSkill(job_id=job.id, skill_name=norm_s, is_required=True))

                for pref_s in jd["preferred_skills"]:
                    norm_s = normalizer.normalize(pref_s)
                    db.session.add(JobPreferredSkill(job_id=job.id, skill_name=norm_s))

        db.session.commit()
        print(f"✓ Seeded {len(jobs_data)} realistic job descriptions with normalized skill requirements.")

        # 3. Create Demo Candidate
        candidate_email = "candidate@example.com"
        cand_user = User.query.filter_by(email=candidate_email).first()
        if not cand_user:
            cand_user = User(email=candidate_email, role='candidate')
            cand_user.set_password("Candidate@123")
            db.session.add(cand_user)
            db.session.flush()

            candidate = Candidate(
                user_id=cand_user.id,
                full_name="Alex Chen",
                phone="+1 (415) 890-2341",
                location="San Francisco, CA",
                headline="Senior Full Stack & Python Engineer",
                bio="Software engineer specializing in distributed backend systems, Python, Flask, SQL, and modern React interfaces. Active open-source contributor."
            )
            db.session.add(candidate)
            db.session.flush()

            profile = CandidateProfile(
                candidate_id=candidate.id,
                summary="Full stack engineer with 3+ years of experience designing robust RESTful microservices in Python (Flask, FastAPI), relational database modeling in PostgreSQL/MySQL, and interactive React user interfaces.",
                career_objective="To contribute to high-impact cloud platforms as a senior software engineer while scaling distributed systems and machine learning workflows.",
                years_of_experience=3.5,
                highest_education="B.E. Computer Science"
            )
            db.session.add(profile)
            db.session.flush()

            # Education
            db.session.add(Education(
                candidate_id=candidate.id,
                institution="University of Washington",
                degree="B.E. Computer Science",
                field_of_study="Computer Science & Engineering",
                start_year=2018,
                end_year=2022,
                grade="3.85 / 4.0"
            ))

            # Experience
            db.session.add(Experience(
                candidate_id=candidate.id,
                company="Vector Analytics Lab",
                title="Software Engineer",
                location="San Francisco, CA",
                start_date="Jul 2022",
                end_date="Present",
                is_current=True,
                description="Built automated ETL data pipelines and RESTful microservices using Python and Flask. Designed database schemas in MySQL and PostgreSQL, improving query response latency by 40%."
            ))

            # Projects
            db.session.add(Project(
                candidate_id=candidate.id,
                title="Intelligent Recommendation & Matching System",
                description="An end-to-end recruitment matching engine utilizing TF-IDF cosine similarity, NLP tokenizers, and multi-source skill aggregation.",
                technologies="Python, Flask, SQL, Scikit-learn, REST API, Git",
                github_url="https://github.com/alexchen-dev/job-matcher",
                live_url="https://job-matcher-demo.dev"
            ))

            db.session.add(Project(
                candidate_id=candidate.id,
                title="Distributed Task Orchestrator",
                description="Microservices task queue with async workers and Redis backend caching.",
                technologies="Python, Redis, Docker, Git",
                github_url="https://github.com/alexchen-dev/task-queue"
            ))

            # Seed Candidate Skills & Multi-Source Evidence
            seed_evidence_items = [
                ("Python", "resume", "resume_extracted", "Found in Work Experience at Vector Analytics Lab"),
                ("Python", "github", "repo_language", "Primary language across 8 public repositories (job-matcher, task-queue)"),
                ("Python", "leetcode", "solved_language", "Used for solving 150+ DSA algorithmic problems"),
                ("Python", "portfolio", "project_tech", "Featured in portfolio capstone projects"),
                ("Flask", "resume", "resume_extracted", "Demonstrated in Vector Analytics Lab microservice stack"),
                ("Flask", "github", "repository_evidence", "Web framework used in job-matcher repository"),
                ("Flask", "portfolio", "project_tech", "Documented in live application demos"),
                ("SQL", "resume", "resume_extracted", "Relational schema design and query optimization"),
                ("SQL", "github", "repository_evidence", "Database migration files in job-matcher"),
                ("Git", "resume", "resume_extracted", "Daily version control in Agile development"),
                ("Git", "github", "git_activity", "Active commit history on GitHub"),
                ("REST API", "resume", "resume_extracted", "API design and client integration"),
                ("REST API", "github", "repository_evidence", "Endpoint routing in task-queue and job-matcher"),
                ("Scikit-learn", "resume", "resume_extracted", "TF-IDF matching model implementation"),
                ("Scikit-learn", "github", "repository_evidence", "Imported and tested in job-matcher ml module"),
                ("Data Structures & Algorithms", "leetcode", "verified_platform", "180 problems solved on LeetCode (95 Easy, 72 Medium, 13 Hard)"),
                ("Machine Learning", "resume", "resume_extracted", "Coursework and recommendation system project"),
                ("Machine Learning", "kaggle", "kaggle_notebooks", "Authored 3 public data analysis notebooks on Kaggle")
            ]

            for sname, src, ev_type, ev_text in seed_evidence_items:
                norm = normalizer.normalize(sname)
                cat = normalizer.get_category(norm)

                cs = CandidateSkill.query.filter_by(candidate_id=candidate.id, skill_name=norm).first()
                if not cs:
                    cs = CandidateSkill(
                        candidate_id=candidate.id,
                        skill_name=norm,
                        category=cat,
                        proficiency="Advanced" if norm in ["Python", "Flask", "SQL"] else "Intermediate",
                        verified=True,
                        evidence_count=1
                    )
                    db.session.add(cs)
                else:
                    cs.evidence_count = (cs.evidence_count or 1) + 1

                db.session.add(SkillEvidence(
                    candidate_id=candidate.id,
                    skill_name=norm,
                    source=src,
                    evidence_type=ev_type,
                    evidence_text=ev_text,
                    confidence=0.92 if src in ['github', 'resume'] else 0.85
                ))

            # External Profiles
            gh_prof = ExternalProfile(
                candidate_id=candidate.id,
                platform='github',
                profile_url='https://github.com/alexchen-dev',
                username='alexchen-dev',
                status='success',
                status_message='Successfully analyzed 8 public repositories (Python, Flask, SQL).'
            )
            db.session.add(gh_prof)
            db.session.flush()

            gh_data = ExternalProfileData(external_profile_id=gh_prof.id)
            gh_data.set_skills(["Python", "Flask", "SQL", "Git", "REST API", "Scikit-learn"])
            gh_data.set_stats({"repos": 8, "stars": 34, "forks": 12})
            gh_data.set_projects([
                {"name": "job-matcher", "language": "Python", "stars": 22, "technologies": ["Python", "Flask", "Scikit-learn"]},
                {"name": "task-queue", "language": "Python", "stars": 12, "technologies": ["Python", "Redis", "Docker"]}
            ])
            db.session.add(gh_data)

            # LeetCode Profile
            lc_prof = ExternalProfile(
                candidate_id=candidate.id,
                platform='leetcode',
                profile_url='https://leetcode.com/alexchen-dev',
                username='alexchen-dev',
                status='success',
                status_message='Verified LeetCode activity: 180 solved problems.'
            )
            db.session.add(lc_prof)
            db.session.flush()

            lc_data = ExternalProfileData(external_profile_id=lc_prof.id)
            lc_data.set_skills(["Data Structures & Algorithms", "Problem Solving", "Python"])
            lc_data.set_stats({"total_solved": 180, "easy": 95, "medium": 72, "hard": 13, "ranking": "Top 12%"})
            db.session.add(lc_data)

            # LinkedIn Profile (transparent status)
            li_prof = ExternalProfile(
                candidate_id=candidate.id,
                platform='linkedin',
                profile_url='https://linkedin.com/in/alexchen-dev',
                username='alexchen-dev',
                status='unavailable',
                status_message='LinkedIn profile linked. Automatic analysis unavailable for this source.'
            )
            db.session.add(li_prof)

            # Portfolio Profile
            port_prof = ExternalProfile(
                candidate_id=candidate.id,
                platform='portfolio',
                profile_url='https://alexchen.dev',
                username='alexchen',
                status='success',
                status_message='Parsed portfolio website (HTML & live project links).'
            )
            db.session.add(port_prof)
            db.session.flush()

            port_data = ExternalProfileData(external_profile_id=port_prof.id)
            port_data.set_skills(["Python", "Flask", "SQL", "REST API", "React"])
            db.session.add(port_data)

            # Professional links
            db.session.add(ProfessionalLink(candidate_id=candidate.id, platform='github', url='https://github.com/alexchen-dev'))
            db.session.add(ProfessionalLink(candidate_id=candidate.id, platform='linkedin', url='https://linkedin.com/in/alexchen-dev'))
            db.session.add(ProfessionalLink(candidate_id=candidate.id, platform='leetcode', url='https://leetcode.com/alexchen-dev'))
            db.session.add(ProfessionalLink(candidate_id=candidate.id, platform='portfolio', url='https://alexchen.dev'))

            profile.calculate_completeness()

            # Seed an Application to the Senior Python Backend job
            py_job = Job.query.filter_by(title="Senior Python Backend Developer").first()
            if py_job:
                app_record = Application(
                    job_id=py_job.id,
                    candidate_id=candidate.id,
                    status="Shortlisted",
                    ats_score=86.5,
                    job_match_score=88.0,
                    skill_match_score=92.0,
                    keyword_match_score=85.0,
                    experience_match_score=100.0,
                    education_match_score=100.0,
                    cover_letter="I am excited to apply for the Senior Python Backend Developer role at Apex Cloud Technologies. My strong background in Python, Flask, SQL, and REST microservices aligns closely with your core tech stack.",
                    recruiter_notes="Strong multi-source evidence across GitHub and LeetCode. Candidate shortlisted for initial technical screening."
                )
                db.session.add(app_record)

            db.session.commit()
            print("✓ Demo candidate created: candidate@example.com / Candidate@123 with full 360° profile evidence.")

        print("✨ Database seed completed successfully!")

if __name__ == '__main__':
    seed_database()
