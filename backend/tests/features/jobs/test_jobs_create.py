import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_job_draft(client: AsyncClient, db_session):
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


@pytest.mark.asyncio
async def test_create_job_missing_title(client: AsyncClient):
    payload = {"description": "Test", "scoring_criteria": []}
    response = await client.post("/api/v1/jobs/", json=payload)
    assert response.status_code == 422
