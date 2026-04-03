# app/features/jobs/service.py
import re
import uuid
from typing import Optional

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.features.jobs.schemas import JobCreate, JobUpdate
from app.models.job import JobPosting, JobStatus, RequiredLanguage, RequiredSkill, ScoringCriterion

# ─── Transitions d'états autorisées ─────────────────────────────────
ALLOWED_TRANSITIONS: dict[JobStatus, set[JobStatus]] = {
    JobStatus.draft:  {JobStatus.active},
    JobStatus.active: {JobStatus.closed},
    JobStatus.closed: set(),   # terminal
}


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Utilitaire : eager loading ───────────────────────────────────
    def _with_relations(self):
        return (
            selectinload(JobPosting.scoring_criteria),
            selectinload(JobPosting.required_skills),
            selectinload(JobPosting.required_languages),
        )

    # ── Génération de slug unique ────────────────────────────────────
    async def _generate_unique_slug(self, title: str) -> str:
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while True:
            result = await self.db.execute(
                select(JobPosting).where(JobPosting.slug == slug)
            )
            if result.scalar_one_or_none() is None:
                return slug
            slug = f"{base_slug}-{counter}"
            counter += 1

    # ── Remplacement des relations enfants ───────────────────────────
    def _build_children(self, job: JobPosting, data: JobCreate | JobUpdate):
        if data.scoring_criteria is not None:
            job.scoring_criteria = [
                ScoringCriterion(criterion_name=c.criterion_name, weight=c.weight)
                for c in data.scoring_criteria
            ]
        if data.required_skills is not None:
            job.required_skills = [
                RequiredSkill(skill_name=s.skill_name)
                for s in data.required_skills
            ]
        if data.required_languages is not None:
            job.required_languages = [
                RequiredLanguage(language_name=l.language_name)
                for l in data.required_languages
            ]

    # ── CREATE ───────────────────────────────────────────────────────
    async def create(self, data: JobCreate, user_id: uuid.UUID) -> JobPosting:
        slug = await self._generate_unique_slug(data.title)
        job = JobPosting(
            title           = data.title,
            description     = data.description,
            location        = data.location,
            contract_type   = data.contract_type,
            alert_threshold = data.alert_threshold,
            slug            = slug,
            created_by_id   = user_id,
            status          = JobStatus.draft,
        )
        self._build_children(job, data)
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return await self.get_by_id(job.id)  # reload avec relations

    # ── LIST (recruteur) ─────────────────────────────────────────────
    async def list_for_user(self, user_id: uuid.UUID) -> list[JobPosting]:
        result = await self.db.execute(
            select(JobPosting)
            .where(JobPosting.created_by_id == user_id)
            .order_by(JobPosting.created_at.desc())
        )
        return result.scalars().all()

    # ── GET by ID ────────────────────────────────────────────────────
    async def get_by_id(self, job_id: uuid.UUID) -> Optional[JobPosting]:
        result = await self.db.execute(
            select(JobPosting)
            .where(JobPosting.id == job_id)
            .options(*self._with_relations())
        )
        return result.scalar_one_or_none()

    # ── GET by slug (public) ─────────────────────────────────────────
    async def get_by_slug(self, slug: str) -> Optional[JobPosting]:
        result = await self.db.execute(
            select(JobPosting)
            .where(JobPosting.slug == slug, JobPosting.status == JobStatus.active)
            .options(*self._with_relations())
        )
        return result.scalar_one_or_none()

    # ── UPDATE (PATCH) ───────────────────────────────────────────────
    async def update(self, job: JobPosting, data: JobUpdate) -> JobPosting:
        if data.title is not None and data.title != job.title:
            job.title = data.title
            job.slug  = await self._generate_unique_slug(data.title)
        if data.description  is not None: job.description     = data.description
        if data.location     is not None: job.location        = data.location
        if data.contract_type is not None: job.contract_type  = data.contract_type
        if data.alert_threshold is not None: job.alert_threshold = data.alert_threshold

        self._build_children(job, data)
        await self.db.commit()
        return await self.get_by_id(job.id)

    # ── TRANSITION D'ÉTAT ────────────────────────────────────────────
    async def transition(self, job: JobPosting, new_status: JobStatus) -> JobPosting:
        allowed = ALLOWED_TRANSITIONS.get(job.status, set())
        if new_status not in allowed:
            raise ValueError(
                f"Cannot transition from '{job.status}' to '{new_status}'. "
                f"Allowed: {[s.value for s in allowed] or 'none'}"
            )
        job.status = new_status
        await self.db.commit()
        return await self.get_by_id(job.id)

    # ── DELETE (brouillon seulement) ─────────────────────────────────
    async def delete(self, job: JobPosting) -> None:
        if job.status != JobStatus.draft:
            raise ValueError("Only draft jobs can be deleted.")
        await self.db.delete(job)
        await self.db.commit()