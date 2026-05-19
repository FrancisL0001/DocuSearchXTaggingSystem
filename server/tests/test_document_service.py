from __future__ import annotations

import json
from pathlib import Path

from services.document_service import DocumentService


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def make_service(tmp_path: Path) -> DocumentService:
    metadata = [
        {"id": "doc-1", "title": "Climate Policy", "snippet": "Carbon targets"},
        {"id": "doc-2", "title": "Housing Study", "snippet": "Urban density"},
        {"id": "doc-3", "title": "Untitled Notes", "snippet": "No tag assigned"},
    ]
    tags = {
        "doc-1": "climate",
        "doc-2": "housing",
    }

    metadata_path = tmp_path / "metadata.json"
    tags_path = tmp_path / "tags.json"
    write_json(metadata_path, metadata)
    write_json(tags_path, tags)

    return DocumentService(metadata_path=metadata_path, tags_path=tags_path)


def test_get_by_indices_preserves_faiss_order_and_skips_invalid_positions(tmp_path: Path) -> None:
    service = make_service(tmp_path)

    results = service.get_by_indices([1, -1, 99, 0], [0.87654, 0.5, 0.4, 0.12345])

    assert [doc.id for doc in results] == ["doc-2", "doc-1"]
    assert results[0].title == "Housing Study"
    assert results[0].score == 0.8765
    assert results[0].tags == ["housing"]
    assert results[1].score == 0.1235


def test_get_all_tags_groups_documents_and_marks_missing_tags_uncategorized(tmp_path: Path) -> None:
    service = make_service(tmp_path)

    groups = service.get_all_tags()

    assert list(groups) == ["Uncategorized", "climate", "housing"]
    assert [doc.id for doc in groups["climate"]] == ["doc-1"]
    assert [doc.id for doc in groups["housing"]] == ["doc-2"]
    assert [doc.id for doc in groups["Uncategorized"]] == ["doc-3"]
    assert groups["Uncategorized"][0].tags == ["Uncategorized"]


def test_get_doc_tags_returns_none_for_unknown_documents(tmp_path: Path) -> None:
    service = make_service(tmp_path)

    assert service.get_doc_tags("doc-1") == ["climate"]
    assert service.get_doc_tags("doc-3") == ["Uncategorized"]
    assert service.get_doc_tags("missing") is None


def test_get_by_tag_returns_empty_list_for_unknown_tag(tmp_path: Path) -> None:
    service = make_service(tmp_path)

    assert [doc.id for doc in service.get_by_tag("housing")] == ["doc-2"]
    assert service.get_by_tag("does-not-exist") == []
