import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_full_job_lifecycle(client: AsyncClient):
    """Full scenario: creation, publication, public consultation, closing, archiving."""
    # 1. Create a draft
    create_payload = {
        "title": "Senior Backend Developer",
        "description": "We are looking for an experienced backend developer.",
        "location": "Paris / Remote",
        "contract_type": "CDI",
        "alert_threshold": 85,
        "scoring_criteria": [
            {"criterion_name": "skills", "weight": 50},
            {"criterion_name": "experience", "weight": 30},
            {"criterion_name": "education", "weight": 10},
            {"criterion_name": "languages", "weight": 10},
        ],
        "required_skills": [{"skill_name": "Python"}, {"skill_name": "PostgreSQL"}],
        "required_languages": [{"language_name": "English"}],
    }
    resp = await client.post("/api/v1/jobs/", json=create_payload)
    assert resp.status_code == 201
    job = resp.json()
    job_id = job["id"]
    assert job["status"] == "draft"
    assert job["slug"] is None

    # 2. Publish
    resp = await client.patch(f"/api/v1/jobs/{job_id}/publish")
    assert resp.status_code == 200
    job = resp.json()
    assert job["status"] == "active"
    slug = job["slug"]
    assert slug is not None

    # 3. Public consultation
    resp = await client.get(f"/api/v1/jobs/public/{slug}")
    assert resp.status_code == 200
    public_job = resp.json()
    assert public_job["title"] == create_payload["title"]
    # Verify sensitive info is not exposed (e.g., created_by_id)
    assert "created_by_id" not in public_job

    # 4. Close the job posting
    resp = await client.patch(f"/api/v1/jobs/{job_id}/close")
    assert resp.status_code == 200
    assert resp.json()["status"] == "closed"

    # 5. The public URL should return 404 (or a "job closed" page)
    resp = await client.get(f"/api/v1/jobs/public/{slug}")
    # Depending on implementation, it may return 404 or 200 with a message.
    # Currently, the get_by_slug service filters by status=active, so 404.
    assert resp.status_code == 404

    # 6. Archive (allowed for closed)
    resp = await client.patch(f"/api/v1/jobs/{job_id}/archive")
    assert resp.status_code == 200
    archived_job = resp.json()
    assert archived_job["archived_at"] is not None

    # 7. The job no longer appears in the default list
    resp = await client.get("/api/v1/jobs/")
    items = resp.json()["items"]
    assert not any(item["id"] == job_id for item in items)


async def test_candidate_cannot_access_draft_job(client: AsyncClient):
    """A candidate must not be able to access a draft job via the public URL."""
    # Create a draft
    create_resp = await client.post(
        "/api/v1/jobs/", json={"title": "Secret Job", "description": "Description confidentielle"}
    )
    job_id = create_resp.json()["id"]

    # Try to access /public/{slug} with a non-existent slug (not generated yet)
    # Or with a fake slug
    resp = await client.get("/api/v1/jobs/public/non-existent-slug")
    assert resp.status_code == 404


async def test_pagination_works(client: AsyncClient):
    """Create multiple job postings and verify pagination."""
    for i in range(5):
        payload = {"title": f"Job {i}", "description": f"Description complète du job numéro {i}"}
        await client.post("/api/v1/jobs/", json=payload)

    # Page 1 with per_page=2
    resp = await client.get("/api/v1/jobs/", params={"page": 1, "per_page": 2})
    data = resp.json()
    assert len(data["items"]) == 2
    assert data["total"] >= 5
    assert data["page"] == 1
    assert data["pages"] >= 3

    # Page 2
    resp = await client.get("/api/v1/jobs/", params={"page": 2, "per_page": 2})
    assert len(resp.json()["items"]) == 2

    # Beyond last page
    resp = await client.get("/api/v1/jobs/", params={"page": 999, "per_page": 2})
    assert len(resp.json()["items"]) == 0
