import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.jobs.schemas import JobCreate, JobUpdate
from app.features.jobs.service import JobService
from app.models.job import JobPosting, JobStatus


@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def job_service(mock_db):
    return JobService(mock_db)


@pytest.mark.asyncio
async def test_create_job_draft(job_service, mock_db):
    data = JobCreate(
        title="Test Job",
        description="Description",
        location="Remote",
        contract_type="CDI",
        alert_threshold=75,
        scoring_criteria=[
            {"criterion_name": "skills", "weight": 40},
            {"criterion_name": "experience", "weight": 60},
        ],
        required_skills=[{"skill_name": "Python"}],
        required_languages=[{"language_name": "English"}],
    )
    user_id = uuid.uuid4()

    # Mock slug generation (not called for draft)
    job_service.get_by_id = AsyncMock(return_value=MagicMock(spec=JobPosting))

    result = await job_service.create(data, user_id)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    assert result is not None


@pytest.mark.asyncio
async def test_transition_draft_to_active_generates_slug(job_service, mock_db):
    job = MagicMock(spec=JobPosting)
    job.id = uuid.uuid4()
    job.status = JobStatus.draft
    job.title = "My Job Title"
    job.slug = None
    job.scoring_criteria = []  # empty

    job_service._generate_unique_slug = AsyncMock(return_value="my-job-title")
    job_service.get_by_id = AsyncMock(return_value=job)

    result = await job_service.transition(job, JobStatus.active)

    job_service._generate_unique_slug.assert_called_once_with("My Job Title")
    assert job.slug == "my-job-title"
    assert job.status == JobStatus.active
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_transition_active_to_closed_allowed(job_service, mock_db):
    job = MagicMock(spec=JobPosting)
    job.status = JobStatus.active
    job_service.get_by_id = AsyncMock(return_value=job)

    result = await job_service.transition(job, JobStatus.closed)

    assert job.status == JobStatus.closed
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_transition_invalid_raises_error(job_service):
    job = MagicMock(spec=JobPosting)
    job.status = JobStatus.closed

    with pytest.raises(ValueError, match="Cannot transition"):
        await job_service.transition(job, JobStatus.active)


@pytest.mark.asyncio
async def test_archive_job(job_service, mock_db):
    from datetime import datetime, timezone

    job = MagicMock(spec=JobPosting)
    job.status = JobStatus.draft
    job.archived_at = None

    await job_service.archive(job)

    assert job.archived_at is not None
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_archive_already_archived_raises(job_service):
    from datetime import datetime

    job = MagicMock(spec=JobPosting)
    job.status = JobStatus.draft
    job.archived_at = datetime.now()

    with pytest.raises(ValueError, match="already archived"):
        await job_service.archive(job)


@pytest.mark.asyncio
async def test_list_for_user_with_status_filter(job_service, mock_db):
    user_id = uuid.uuid4()
    mock_result = MagicMock()
    mock_result.scalar_one.return_value = 3  # total count
    mock_result.scalars.return_value.all.return_value = []  # items

    mock_db.execute = AsyncMock(return_value=mock_result)

    result = await job_service.list_for_user(
        user_id=user_id, page=1, per_page=20, status=JobStatus.draft, include_archived=False
    )

    # Verify that the query includes the status filter
    called_query = mock_db.execute.call_args_list[0][0][0]
    # Cannot easily inspect SQL, but the test validates that it doesn't crash
    assert result.total == 3
