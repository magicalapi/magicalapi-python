import json
from collections.abc import AsyncGenerator
from typing import Any

import httpx
import pytest
import pytest_asyncio

from magicalapi.services.resume_score_service import ResumeScoreService
from magicalapi.types.resume_score import ResumeScoreResponse
from magicalapi.types.schemas import HttpResponse


def _make_resume_score_response() -> HttpResponse:
    response_body = {
        "data": {
            "score": 87,
            "summary": "Strong match for the role",
            "strengths": [{"text": "Python experience", "category": "skills"}],
            "improvements": [
                {"text": "Add more leadership examples", "category": "other"}
            ],
            "job_match": {
                "score": 90,
                "summary": "Job match is strong",
                "pros": [{"type": "title", "message": "Title aligns"}],
                "cons": [{"type": "gap", "message": "Missing one requirement"}],
                "warns": [
                    {
                        "type": "note",
                        "message": "Consider tailoring summary",
                    }
                ],
            },
            "skill_match": {
                "score": 85,
                "summary": "Skills align",
                "skills": {"all_skills": ["Python", "AWS"]},
                "match_result": {
                    "miss_match": ["Kubernetes"],
                    "partial_match": ["Docker"],
                    "strong_match": ["Python"],
                },
            },
            "education_match": {
                "score": 80,
                "summary": "Education is a fit",
                "pros": [{"type": "degree", "message": "Relevant degree"}],
                "cons": [
                    {
                        "type": "specialization",
                        "message": "Could be more specific",
                    }
                ],
                "warns": [{"type": "note", "message": "No issues"}],
            },
            "more_information": {
                "region": "Europe",
                "overqualification_status": False,
                "qualification_reason": "Meets the role requirements",
            },
            "jd_text": "job description text",
        },
        "usage": {"credits": 10},
    }

    return HttpResponse(
        text=json.dumps(response_body),
        status_code=200,
    )


@pytest_asyncio.fixture(scope="function")
async def httpxclient() -> AsyncGenerator[httpx.AsyncClient]:
    client = httpx.AsyncClient(headers={"content-type": "application/json"})

    yield client

    await client.aclose()
    del client


@pytest.mark.asyncio
@pytest.mark.parametrize("job_description", ["a" * 99, "a" * 5001])
async def test_get_resume_score_rejects_invalid_job_description_length(
    httpxclient: httpx.AsyncClient, job_description: str
):
    service = ResumeScoreService(httpxclient)

    with pytest.raises(ValueError, match="between 100 and 5000 characters long"):
        await service.get_resume_score(
            url="https://example.com/resume.pdf", job_description=job_description
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("job_description", ["a" * 100, "a" * 5000])
async def test_get_resume_score_accepts_boundary_lengths(
    httpxclient: httpx.AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
    job_description: str,
):
    service = ResumeScoreService(httpxclient)
    captured_request: dict[str, str] = {}

    async def fake_send_post_request(
        path: str, data: dict[str, Any], headers: dict[str, str] | None = None
    ):
        captured_request["path"] = path
        captured_request.update(data)
        return _make_resume_score_response()

    monkeypatch.setattr(service, "_send_post_request", fake_send_post_request)

    response = await service.get_resume_score(
        url="https://example.com/resume.pdf",
        job_description=job_description,
    )

    assert isinstance(response, ResumeScoreResponse)
    assert response.data.score == 87
    assert response.usage.credits == 10
    assert captured_request["path"] == "resume-score"
    assert captured_request["url"] == "https://example.com/resume.pdf"
    assert captured_request["job_description"] == job_description
