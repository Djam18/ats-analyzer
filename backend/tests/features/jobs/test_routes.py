import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_list_jobs_empty(client: AsyncClient):
    response = await client.get("/api/v1/jobs/")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


async def test_create_job_draft(client: AsyncClient):
    payload = {
        "title": "Développeur Python",
        "description": "Nous recherchons un développeur Python expérimenté...",
        "location": "Paris",
        "contract_type": "CDI",
        "alert_threshold": 80,
        "scoring_criteria": [
            {"criterion_name": "skills", "weight": 40},
            {"criterion_name": "experience", "weight": 30},
            {"criterion_name": "education", "weight": 20},
            {"criterion_name": "languages", "weight": 10},
        ],
        "required_skills": [{"skill_name": "Python"}, {"skill_name": "FastAPI"}],
        "required_languages": [{"language_name": "English"}],
    }
    response = await client.post("/api/v1/jobs/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["status"] == "draft"
    assert data["slug"] is None or data["slug"] == ""
    assert len(data["scoring_criteria"]) == 4
    assert data["alert_threshold"] == 80

    # Retrieve by ID
    job_id = data["id"]
    response = await client.get(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["id"] == job_id


async def test_get_job_not_found(client: AsyncClient):
    fake_id = uuid.uuid4()
    response = await client.get(f"/api/v1/jobs/{fake_id}")
    assert response.status_code == 404


async def test_update_job_draft(client: AsyncClient):
    # Create a draft
    payload = {
        "title": "Titre initial",
        "description": "Description initiale",
        "location": "Lyon",
        "contract_type": "CDD",
        "alert_threshold": 70,
        "scoring_criteria": [
            {"criterion_name": "skills", "weight": 50},
            {"criterion_name": "experience", "weight": 50},
        ],
        "required_skills": [],
        "required_languages": [],
    }
    create_resp = await client.post("/api/v1/jobs/", json=payload)
    assert create_resp.status_code == 201
    job_id = create_resp.json()["id"]

    # Update
    update_payload = {
        "title": "Titre modifié",
        "description": "Nouvelle description",
    }
    response = await client.patch(f"/api/v1/jobs/{job_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Titre modifié"
    assert data["description"] == "Nouvelle description"
    assert data["location"] == "Lyon"  # unchanged


async def test_cannot_update_published_job(client: AsyncClient):
    # Create and publish
    payload = {
        "title": "Job à publier",
        "description": "Description",
        "scoring_criteria": [
            {"criterion_name": "skills", "weight": 100},
        ],
    }
    create_resp = await client.post("/api/v1/jobs/", json=payload)
    job_id = create_resp.json()["id"]
    await client.patch(f"/api/v1/jobs/{job_id}/publish")

    # Try to update
    update = {"title": "Nouveau titre"}
    response = await client.patch(f"/api/v1/jobs/{job_id}", json=update)
    assert response.status_code == 400
    assert "Only draft jobs can be edited" in response.text


async def test_publish_job(client: AsyncClient):
    # Create a draft
    payload = {
        "title": "DevOps Engineer",
        "description": "Description",
        "scoring_criteria": [],
    }
    create_resp = await client.post("/api/v1/jobs/", json=payload)
    job_id = create_resp.json()["id"]

    # Publish
    response = await client.patch(f"/api/v1/jobs/{job_id}/publish")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert data["slug"] is not None
    assert data["slug"] != ""

    # Verify that the public URL works
    slug = data["slug"]
    pub_response = await client.get(f"/api/v1/jobs/public/{slug}")
    assert pub_response.status_code == 200
    assert pub_response.json()["id"] == job_id


async def test_close_job(client: AsyncClient):
    # Create and publish
    payload = {"title": "Job à fermer", "description": "description"}
    create_resp = await client.post("/api/v1/jobs/", json=payload)
    job_id = create_resp.json()["id"]
    await client.patch(f"/api/v1/jobs/{job_id}/publish")

    # Close
    response = await client.patch(f"/api/v1/jobs/{job_id}/close")
    assert response.status_code == 200
    assert response.json()["status"] == "closed"


async def test_archive_job(client: AsyncClient):
    # Create a draft
    payload = {"title": "Job à archiver", "description": "description"}
    create_resp = await client.post("/api/v1/jobs/", json=payload)
    job_id = create_resp.json()["id"]

    # Archive
    response = await client.patch(f"/api/v1/jobs/{job_id}/archive")
    assert response.status_code == 200
    data = response.json()
    assert data["archived_at"] is not None
    assert "T" in data["archived_at"]  # ISO format

    # Verify it no longer appears in the default list
    list_resp = await client.get("/api/v1/jobs/")
    items = list_resp.json()["items"]
    assert all(item["id"] != job_id for item in items)


async def test_delete_draft_job(client: AsyncClient):
    payload = {"title": "Job à supprimer", "description": "Description du job à supprimer"}

    create_resp = await client.post("/api/v1/jobs/", json=payload)
    job_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 204

    # Verify it no longer exists
    get_resp = await client.get(f"/api/v1/jobs/{job_id}")
    assert get_resp.status_code == 404


async def test_filter_jobs_by_status(client: AsyncClient):
    # Create a draft
    draft = {"title": "Draft Job", "description": "Description du brouillon"}

    await client.post("/api/v1/jobs/", json=draft)

    # Create a published job
    pub = {"title": "Published Job", "description": "Description du job publié"}

    pub_resp = await client.post("/api/v1/jobs/", json=pub)
    pub_id = pub_resp.json()["id"]
    await client.patch(f"/api/v1/jobs/{pub_id}/publish")

    # Filter by draft
    resp = await client.get("/api/v1/jobs/", params={"status": "draft"})
    items = resp.json()["items"]
    assert all(item["status"] == "draft" for item in items)

    # Filter by active
    resp = await client.get("/api/v1/jobs/", params={"status": "active"})
    items = resp.json()["items"]
    assert all(item["status"] == "active" for item in items)
