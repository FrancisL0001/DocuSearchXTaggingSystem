from __future__ import annotations

import numpy as np
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.dependencies import get_document_service, get_embedder, get_faiss_index
from api.rate_limit import reset_rate_limiters, search_rate_limiter
from api.router import api_router
from schemas.response import DocumentResult


class FakeEmbedder:
    def encode(self, texts: list[str]) -> np.ndarray:
        assert texts == ["carbon policy"]
        return np.array([[1.0, 0.0]], dtype="float32")


class FakeIndex:
    def search(self, query_vec: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
        np.testing.assert_array_equal(query_vec, np.array([1.0, 0.0], dtype="float32"))
        assert k == 2
        return (
            np.array([0.91, 0.72], dtype="float32"),
            np.array([0, 1], dtype="int64"),
        )


class FakeDocumentService:
    def get_by_indices(self, faiss_indices: list[int], scores: list[float]) -> list[DocumentResult]:
        assert faiss_indices == [0, 1]
        return [
            DocumentResult(
                id="doc-1",
                title="Carbon Targets",
                snippet="Policy text",
                score=scores[0],
                tags=["climate"],
            ),
            DocumentResult(
                id="doc-2",
                title="Emissions Report",
                snippet="Research text",
                score=scores[1],
                tags=["climate"],
            ),
        ]

    def get_all_tags(self) -> dict[str, list[DocumentResult]]:
        return {
            "climate": [
                DocumentResult(
                    id="doc-1",
                    title="Carbon Targets",
                    snippet="Policy text",
                    score=0.0,
                    tags=["climate"],
                )
            ],
            "housing": [
                DocumentResult(
                    id="doc-3",
                    title="Housing Study",
                    snippet="Rent text",
                    score=0.0,
                    tags=["housing"],
                )
            ],
        }

    def get_doc_tags(self, doc_id: str) -> list[str] | None:
        if doc_id == "doc-1":
            return ["climate"]
        return None


def make_client() -> TestClient:
    reset_rate_limiters()
    app = FastAPI()
    app.include_router(api_router, prefix="/api/v1")
    app.dependency_overrides[get_embedder] = lambda: FakeEmbedder()
    app.dependency_overrides[get_faiss_index] = lambda: FakeIndex()
    app.dependency_overrides[get_document_service] = lambda: FakeDocumentService()
    return TestClient(app)


def test_search_endpoint_validates_request_and_returns_ranked_document_shape() -> None:
    client = make_client()

    response = client.post("/api/v1/search", json={"query": "carbon policy", "top_k": 2})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert [doc["id"] for doc in body["results"]] == ["doc-1", "doc-2"]
    assert set(body["results"][0]) == {"id", "title", "snippet", "score", "tags"}
    assert body["results"][0]["tags"] == ["climate"]


def test_search_endpoint_rejects_empty_queries_and_invalid_top_k() -> None:
    client = make_client()

    assert client.post("/api/v1/search", json={"query": "", "top_k": 2}).status_code == 422
    assert client.post("/api/v1/search", json={"query": "carbon", "top_k": 0}).status_code == 422
    assert client.post("/api/v1/search", json={"query": "carbon", "top_k": 21}).status_code == 422


def test_tags_endpoint_returns_topic_groups_with_documents() -> None:
    client = make_client()

    response = client.get("/api/v1/tags")

    assert response.status_code == 200
    assert response.json() == {
        "tags": [
            {
                "tag": "climate",
                "documents": [
                    {
                        "id": "doc-1",
                        "title": "Carbon Targets",
                        "snippet": "Policy text",
                        "score": 0.0,
                        "tags": ["climate"],
                    }
                ],
            },
            {
                "tag": "housing",
                "documents": [
                    {
                        "id": "doc-3",
                        "title": "Housing Study",
                        "snippet": "Rent text",
                        "score": 0.0,
                        "tags": ["housing"],
                    }
                ],
            },
        ]
    }


def test_document_tags_endpoint_returns_tags_or_404() -> None:
    client = make_client()

    known = client.get("/api/v1/documents/doc-1/tags")
    missing = client.get("/api/v1/documents/missing/tags")

    assert known.status_code == 200
    assert known.json() == ["climate"]
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Document 'missing' not found"


def test_search_endpoint_returns_429_after_rate_limit_is_exceeded() -> None:
    client = make_client()

    for _ in range(search_rate_limiter.limit):
        response = client.post("/api/v1/search", json={"query": "carbon policy", "top_k": 2})
        assert response.status_code == 200

    limited = client.post("/api/v1/search", json={"query": "carbon policy", "top_k": 2})

    assert limited.status_code == 429
    assert limited.json()["detail"] == "Rate limit exceeded. Please retry later."
    assert limited.headers["Retry-After"].isdigit()
    assert limited.headers["X-RateLimit-Limit"] == str(search_rate_limiter.limit)
    assert limited.headers["X-RateLimit-Remaining"] == "0"
