# app/features/jobs/router.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.features.jobs.schemas import JobCreate, JobListOut, JobOut, JobUpdate
from app.features.jobs.service import JobService
from app.models.job import JobStatus
from app.models.user import User

router = APIRouter()


# ── Helpers ──────────────────────────────────────────────────────────

async def _get_job_or_404(job_id: uuid.UUID, db: AsyncSession):
    job = await JobService(db).get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

def _assert_owner(job, current_user: User):
    if job.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")


# ── Endpoints privés (recruteur authentifié) ─────────────────────────

@router.post("/", response_model=JobOut, status_code=201,
             summary="Create a job posting (draft)")
async def create_job(
    body: JobCreate,
    db:           AsyncSession = Depends(get_db),
    current_user: User         = Depends(get_current_user),
):
    return await JobService(db).create(body, current_user.id)


@router.get("/", response_model=list[JobListOut],
            summary="List my job postings")
async def list_jobs(
    db:           AsyncSession = Depends(get_db),
    current_user: User         = Depends(get_current_user),
):
    return await JobService(db).list_for_user(current_user.id)


@router.get("/{job_id}", response_model=JobOut,
            summary="Get a job posting by ID")
async def get_job(
    job_id: uuid.UUID,
    db:           AsyncSession = Depends(get_db),
    current_user: User         = Depends(get_current_user),
):
    job = await _get_job_or_404(job_id, db)
    _assert_owner(job, current_user)
    return job


@router.patch("/{job_id}", response_model=JobOut,
              summary="Update a job posting")
async def update_job(
    job_id: uuid.UUID,
    body:   JobUpdate,
    db:           AsyncSession = Depends(get_db),
    current_user: User         = Depends(get_current_user),
):
    job = await _get_job_or_404(job_id, db)
    _assert_owner(job, current_user)
    if job.status != JobStatus.draft:
        raise HTTPException(
            status_code=400,
            detail="Only draft jobs can be edited. Close and recreate if needed."
        )
    try:
        return await JobService(db).update(job, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{job_id}/publish", response_model=JobOut,
              summary="Publish a job (draft → active)")
async def publish_job(
    job_id: uuid.UUID,
    db:           AsyncSession = Depends(get_db),
    current_user: User         = Depends(get_current_user),
):
    job = await _get_job_or_404(job_id, db)
    _assert_owner(job, current_user)
    try:
        return await JobService(db).transition(job, JobStatus.active)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{job_id}/close", response_model=JobOut,
              summary="Close a job (active → closed)")
async def close_job(
    job_id: uuid.UUID,
    db:           AsyncSession = Depends(get_db),
    current_user: User         = Depends(get_current_user),
):
    job = await _get_job_or_404(job_id, db)
    _assert_owner(job, current_user)
    try:
        return await JobService(db).transition(job, JobStatus.closed)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{job_id}", status_code=204,
               summary="Delete a job (draft only)")
async def delete_job(
    job_id: uuid.UUID,
    db:           AsyncSession = Depends(get_db),
    current_user: User         = Depends(get_current_user),
):
    job = await _get_job_or_404(job_id, db)
    _assert_owner(job, current_user)
    try:
        await JobService(db).delete(job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Endpoint public (candidat, sans auth) ────────────────────────────

@router.get("/public/{slug}", response_model=JobOut,
            summary="Public job page for candidates")
async def get_public_job(slug: str, db: AsyncSession = Depends(get_db)):
    job = await JobService(db).get_by_slug(slug)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not active")
    return job