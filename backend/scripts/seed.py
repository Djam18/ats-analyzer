"""
Seed script — ATS Platform
Populates the database with initial data for development.

Usage (inside Docker):
    docker compose exec backend python scripts/seed.py

Usage (local):
    DATABASE_URL=postgresql+asyncpg://ats:devpass@localhost:5432/ats_dev python scripts/seed.py
"""

import asyncio
import os
import sys
import uuid

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Allow importing from app/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.models import (
    Application,
    ApplicationStage,
    EducationLevel,
    EmailTemplate,
    InternalNote,
    JobPosting,
    JobStatus,
    ParsingStatus,
    RequiredLanguage,
    RequiredSkill,
    ResumeExtraction,
    ResumeFile,
    ScoringCriterion,
    User,
    UserRole,
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://ats:devpass@localhost:5432/ats_dev")
pwd_context  = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─────────────────────────────────────────
# Seed data
# ─────────────────────────────────────────
async def reset_database(session):
    from app.models import Base
    from app.database import engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def seed(session: AsyncSession) -> None:

    print("🌱 Starting seed...")

    # ── 1. Admin user ───────────────────────────────────────────────────────
    admin = User(
        id            = uuid.uuid4(),
        email         = "admin@ats.dev",
        full_name     = "Admin ATS",
        password_hash = pwd_context.hash("admin1234"),
        role          = UserRole.admin,
    )
    recruiter = User(
        id            = uuid.uuid4(),
        email         = "recruiter@ats.dev",
        full_name     = "Alice Recruiter",
        password_hash = pwd_context.hash("recruiter1234"),
        role          = UserRole.recruiter,
    )
    session.add_all([admin, recruiter])
    await session.flush()
    print(f"  ✅ Users created — admin: admin@ats.dev / admin1234")

    # ── 2. Job postings ─────────────────────────────────────────────────────
    job_python = JobPosting(
        id              = uuid.uuid4(),
        title           = "Senior Python Developer",
        description     = (
            "We are looking for a senior Python developer to join our backend team. "
            "You will work on our ATS platform, building scalable APIs and async workers."
        ),
        location        = "Paris, France (Hybrid)",
        contract_type   = "Full-time",
        status          = JobStatus.active,
        alert_threshold = 75,
        slug            = "senior-python-developer",
        created_by_id   = recruiter.id,
    )
    job_frontend = JobPosting(
        id              = uuid.uuid4(),
        title           = "Frontend Engineer — Vue.js",
        description     = (
            "Join our product team as a Frontend Engineer. "
            "You will build modern, responsive UIs using Vue.js and Nuxt."
        ),
        location        = "Remote",
        contract_type   = "Full-time",
        status          = JobStatus.active,
        alert_threshold = 70,
        slug            = "frontend-engineer-vuejs",
        created_by_id   = recruiter.id,
    )
    job_draft = JobPosting(
        id              = uuid.uuid4(),
        title           = "DevOps Engineer",
        description     = "Draft — not published yet.",
        location        = "Lyon, France",
        contract_type   = "Full-time",
        status          = JobStatus.draft,
        alert_threshold = 80,
        slug            = "devops-engineer",
        created_by_id   = recruiter.id,
    )
    session.add_all([job_python, job_frontend, job_draft])
    await session.flush()
    print(f"  ✅ Job postings created (2 active, 1 draft)")

    # ── 3. Scoring criteria ─────────────────────────────────────────────────
    for job, weights in [
        (job_python,   {"skills": 40, "experience": 35, "education": 15, "languages": 10}),
        (job_frontend, {"skills": 45, "experience": 30, "education": 15, "languages": 10}),
    ]:
        for name, weight in weights.items():
            session.add(ScoringCriterion(
                id             = uuid.uuid4(),
                job_posting_id = job.id,
                criterion_name = name,
                weight         = weight,
            ))
    print(f"  ✅ Scoring criteria created")

    # ── 4. Required skills & languages ──────────────────────────────────────
    python_skills = ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "SQLAlchemy"]
    for skill in python_skills:
        session.add(RequiredSkill(id=uuid.uuid4(), job_posting_id=job_python.id, skill_name=skill))

    frontend_skills = ["Vue.js", "Nuxt", "TypeScript", "TailwindCSS", "REST APIs"]
    for skill in frontend_skills:
        session.add(RequiredSkill(id=uuid.uuid4(), job_posting_id=job_frontend.id, skill_name=skill))

    for lang in ["English", "French"]:
        session.add(RequiredLanguage(id=uuid.uuid4(), job_posting_id=job_python.id,   language_name=lang))
        session.add(RequiredLanguage(id=uuid.uuid4(), job_posting_id=job_frontend.id, language_name=lang))

    await session.flush()
    print(f"  ✅ Required skills and languages created")

    # ── 5. Applications ─────────────────────────────────────────────────────
    app1 = Application(
        id             = uuid.uuid4(),
        job_posting_id = job_python.id,
        candidate_name = "Bob Martin",
        email          = "bob.martin@example.com",
        stage          = ApplicationStage.hr_interview,
        gdpr_consent   = True,
        global_score   = 82,
        scores_detail  = {"skills": 88, "experience": 80, "education": 75, "languages": 90},
        alert_sent     = True,
    )
    app2 = Application(
        id             = uuid.uuid4(),
        job_posting_id = job_python.id,
        candidate_name = "Clara Dupont",
        email          = "clara.dupont@example.com",
        stage          = ApplicationStage.received,
        gdpr_consent   = True,
        global_score   = None,  # parsing not done yet
    )
    app3 = Application(
        id             = uuid.uuid4(),
        job_posting_id = job_frontend.id,
        candidate_name = "David Lee",
        email          = "david.lee@example.com",
        stage          = ApplicationStage.shortlisted,
        gdpr_consent   = True,
        global_score   = 68,
        scores_detail  = {"skills": 72, "experience": 60, "education": 65, "languages": 80},
    )
    session.add_all([app1, app2, app3])
    await session.flush()
    print(f"  ✅ Applications created (3)")

    # ── 6. Resume files ─────────────────────────────────────────────────────
    session.add(ResumeFile(
        id             = uuid.uuid4(),
        application_id = app1.id,
        file_path      = "resumes/bob-martin-cv.pdf",
        original_name  = "CV_Bob_Martin.pdf",
        file_size      = 204800,
        mime_type      = "application/pdf",
    ))
    session.add(ResumeFile(
        id             = uuid.uuid4(),
        application_id = app3.id,
        file_path      = "resumes/david-lee-cv.pdf",
        original_name  = "David_Lee_Resume.pdf",
        file_size      = 153600,
        mime_type      = "application/pdf",
    ))
    print(f"  ✅ Resume files created")

    # ── 7. Resume extractions ────────────────────────────────────────────────
    session.add(ResumeExtraction(
        id                  = uuid.uuid4(),
        application_id      = app1.id,
        extracted_name      = "Bob Martin",
        extracted_email     = "bob.martin@example.com",
        skills              = ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"],
        years_of_experience = 7,
        education_level     = EducationLevel.bac5,
        parsing_status      = ParsingStatus.success,
    ))
    session.add(ResumeExtraction(
        id                  = uuid.uuid4(),
        application_id      = app2.id,
        parsing_status      = ParsingStatus.pending,  # not yet processed
        attempt_count       = 0,
    ))
    session.add(ResumeExtraction(
        id                  = uuid.uuid4(),
        application_id      = app3.id,
        extracted_name      = "David Lee",
        extracted_email     = "david.lee@example.com",
        skills              = ["Vue.js", "TypeScript", "Nuxt", "TailwindCSS"],
        years_of_experience = 3,
        education_level     = EducationLevel.bac3,
        parsing_status      = ParsingStatus.success,
    ))
    print(f"  ✅ Resume extractions created")

    # ── 8. Internal notes ───────────────────────────────────────────────────
    session.add(InternalNote(
        id             = uuid.uuid4(),
        application_id = app1.id,
        user_id        = recruiter.id,
        content        = "Strong Python background. Schedule HR interview for next week.",
    ))
    session.add(InternalNote(
        id             = uuid.uuid4(),
        application_id = app3.id,
        user_id        = recruiter.id,
        content        = "Good portfolio. Lacks some experience but shows potential.",
    ))
    print(f"  ✅ Internal notes created")

    # ── 9. Email templates ──────────────────────────────────────────────────
    session.add(EmailTemplate(
        id         = uuid.uuid4(),
        name       = "application_received",
        subject    = "We received your application for: {{job_title}}",
        body_text  = (
            "Hi {{candidate_name}},\n\n"
            "Thank you for applying to \"{{job_title}}\".\n"
            "We will review your profile and get back to you shortly.\n\n"
            "Best regards,\nThe Recruitment Team"
        ),
        body_html  = (
            "<p>Hi <strong>{{candidate_name}}</strong>,</p>"
            "<p>Thank you for applying to <em>{{job_title}}</em>.</p>"
            "<p>We will review your profile and get back to you shortly.</p>"
            "<p>Best regards,<br/>The Recruitment Team</p>"
        ),
        is_default = True,
    ))
    session.add(EmailTemplate(
        id        = uuid.uuid4(),
        name      = "high_score_alert",
        subject   = "⚡ Strong candidate — {{job_title}}",
        body_text = (
            "Hi,\n\n"
            "{{candidate_name}} just scored {{score}}% on \"{{job_title}}\".\n"
            "Check their application now.\n\n"
            "The ATS Platform"
        ),
        is_default = False,
    ))
    session.add(EmailTemplate(
        id        = uuid.uuid4(),
        name      = "stage_update",
        subject   = "Update on your application — {{job_title}}",
        body_text = (
            "Hi {{candidate_name}},\n\n"
            "Your application for \"{{job_title}}\" has been updated: {{new_stage}}.\n\n"
            "Best regards,\nThe Recruitment Team"
        ),
        is_default = False,
    ))
    print(f"  ✅ Email templates created (3)")

    await session.commit()
    print("\n🎉 Seed completed successfully!")
    print("\n📋 Credentials:")
    print("   Admin     → admin@ats.dev      / admin1234")
    print("   Recruiter → recruiter@ats.dev  / recruiter1234")


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────

async def main():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        await reset_database(session)
        await seed(session)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())