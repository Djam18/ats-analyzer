# app/features/jobs/service.py
import uuid
from datetime import datetime, timezone
from typing import Optional

from slugify import slugify
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.features.jobs.schemas import JobCreate, JobListOut, JobUpdate, PaginatedResponse
from app.models.job import JobPosting, JobStatus, RequiredLanguage, RequiredSkill, ScoringCriterion

ALLOWED_TRANSITIONS: dict[JobStatus, set[JobStatus]] = {
    JobStatus.draft: {JobStatus.active},
    JobStatus.active: {JobStatus.closed},
    JobStatus.closed: set(),
}


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _with_relations(self):
        return (
            selectinload(JobPosting.scoring_criteria),
            selectinload(JobPosting.required_skills),
            selectinload(JobPosting.required_languages),
        )

    async def _generate_unique_slug(self, title: str) -> str:
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while True:
            result = await self.db.execute(select(JobPosting).where(JobPosting.slug == slug))
            if result.scalar_one_or_none() is None:
                return slug
            slug = f"{base_slug}-{counter}"
            counter += 1

    def _build_children(self, job: JobPosting, data: JobCreate | JobUpdate):
        if data.scoring_criteria is not None:
            job.scoring_criteria = [
                ScoringCriterion(criterion_name=c.criterion_name, weight=c.weight)
                for c in data.scoring_criteria
            ]
        if data.required_skills is not None:
            job.required_skills = [
                RequiredSkill(skill_name=s.skill_name) for s in data.required_skills
            ]
        if data.required_languages is not None:
            job.required_languages = [
                RequiredLanguage(language_name=lang.language_name)
                for lang in data.required_languages
            ]

    async def create(self, data: JobCreate, user_id: uuid.UUID) -> JobPosting:
        # Slug will be generated upon first publication (draft → active)
        job = JobPosting(
            title=data.title,
            description=data.description,
            location=data.location,
            contract_type=data.contract_type,
            alert_threshold=data.alert_threshold,
            slug=None,  # Empty for drafts
            created_by_id=user_id,
            status=JobStatus.draft,
        )
        self._build_children(job, data)
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)

        result = await self.get_by_id(job.id)
        if not result:
            raise RuntimeError(f"Job {job.id} not found after creation")
        return result

    async def archive(self, job: JobPosting) -> JobPosting:
        if job.status not in (JobStatus.draft, JobStatus.closed):
            raise ValueError("Only draft or closed jobs can be archived.")
        if job.archived_at is not None:
            raise ValueError("Job already archived.")
        job.archived_at = datetime.now(timezone.utc)
        await self.db.commit()
        return job

    # ── Paginated LIST ──────────────────────────────────────────────────
    async def list_for_user(
        self,
        user_id: uuid.UUID,
        page: int = 1,
        per_page: int = 20,
        status: JobStatus | None = None,
        include_archived: bool = False,
    ) -> PaginatedResponse[JobListOut]:

        base_query = select(JobPosting).where(JobPosting.created_by_id == user_id)

        if not include_archived:
            base_query = base_query.where(JobPosting.archived_at.is_(None))

        if status is not None:
            base_query = base_query.where(JobPosting.status == status)

        # Total count
        count_result = await self.db.execute(
            select(func.count()).select_from(base_query.subquery())
        )
        total = count_result.scalar_one()

        # Paginated data
        offset = (page - 1) * per_page
        result = await self.db.execute(
            base_query.order_by(JobPosting.created_at.desc()).offset(offset).limit(per_page)
        )
        items = result.scalars().all()

        pages = max(1, -(-total // per_page))

        return PaginatedResponse[JobListOut](
            items=[JobListOut.model_validate(j) for j in items],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        )

    async def get_by_id(self, job_id: uuid.UUID) -> Optional[JobPosting]:
        result = await self.db.execute(
            select(JobPosting).where(JobPosting.id == job_id).options(*self._with_relations())
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[JobPosting]:
        result = await self.db.execute(
            select(JobPosting)
            .where(JobPosting.slug == slug, JobPosting.status == JobStatus.active)
            .options(*self._with_relations())
        )
        return result.scalar_one_or_none()

    async def update(self, job: JobPosting, data: JobUpdate) -> JobPosting:
        # Slug NEVER changes after creation (immutability)
        if data.title is not None:
            job.title = data.title

        if data.description is not None:
            job.description = data.description

        if data.location is not None:
            job.location = data.location

        if data.contract_type is not None:
            job.contract_type = data.contract_type

        if data.alert_threshold is not None:
            job.alert_threshold = data.alert_threshold

        self._build_children(job, data)
        await self.db.commit()

        result = await self.get_by_id(job.id)
        if not result:
            raise RuntimeError(f"Job {job.id} not found after update")
        return result

    async def transition(self, job: JobPosting, new_status: JobStatus) -> JobPosting:
        allowed = ALLOWED_TRANSITIONS.get(job.status, set())
        if new_status not in allowed:
            raise ValueError(
                f"Cannot transition from '{job.status}' to '{new_status}'. "
                f"Allowed: {[s.value for s in allowed] or 'none'}"
            )

        if job.status == JobStatus.draft and new_status == JobStatus.active:
            if job.slug is None:  # instead of if not job.slug
                job.slug = await self._generate_unique_slug(job.title)

        if not job.scoring_criteria:
            # Create the 4 default criteria with weight 25 each
            default_criteria = [
                ScoringCriterion(criterion_name="skills", weight=25),
                ScoringCriterion(criterion_name="experience", weight=25),
                ScoringCriterion(criterion_name="education", weight=25),
                ScoringCriterion(criterion_name="languages", weight=25),
            ]
            job.scoring_criteria = default_criteria
            await self.db.flush()

        job.status = new_status
        await self.db.commit()

        result = await self.get_by_id(job.id)
        if not result:
            raise RuntimeError(f"Job {job.id} not found after transition")
        return result

    async def delete(self, job: JobPosting) -> None:
        if job.status != JobStatus.draft:
            raise ValueError("Only draft jobs can be deleted.")
        await self.db.delete(job)
        await self.db.commit()
