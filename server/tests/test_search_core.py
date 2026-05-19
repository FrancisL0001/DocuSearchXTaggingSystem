from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from search.faiss_index import FaissIndex
from search.retrieval import retrieve


def test_faiss_index_search_returns_nearest_documents_in_score_order(tmp_path: Path) -> None:
    embeddings = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.7, 0.7, 0.0],
        ],
        dtype="float32",
    )
    query = np.array([1.0, 0.0, 0.0], dtype="float32")

    index = FaissIndex(dimension=3)
    index.add(embeddings)

    scores, indices = index.search(query, k=2)

    assert indices.tolist() == [0, 2]
    assert scores.tolist() == pytest.approx([1.0, 0.7])


def test_faiss_index_can_be_saved_and_loaded_without_losing_vectors(tmp_path: Path) -> None:
    embeddings = np.eye(3, dtype="float32")
    index_path = tmp_path / "index.faiss"

    index = FaissIndex(dimension=3)
    index.add(embeddings)
    index.save(index_path)

    loaded = FaissIndex.load(index_path)
    scores, indices = loaded.search(np.array([0.0, 1.0, 0.0], dtype="float32"), k=2)

    assert loaded.dimension == 3
    assert loaded.index.ntotal == 3
    assert indices[0] == 1
    assert scores[0] == pytest.approx(1.0)


def test_retrieve_embeds_query_and_filters_faiss_sentinel_indices() -> None:
    class FakeEmbedder:
        def encode(self, texts: list[str]) -> np.ndarray:
            assert texts == ["carbon policy"]
            return np.array([[0.2, 0.8]], dtype="float32")

    class FakeIndex:
        def search(self, query_vec: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
            np.testing.assert_array_equal(query_vec, np.array([0.2, 0.8], dtype="float32"))
            assert k == 4
            return (
                np.array([0.95, 0.70, -3.4, -3.4], dtype="float32"),
                np.array([7, 2, -1, -1], dtype="int64"),
            )

    results = retrieve("carbon policy", FakeEmbedder(), FakeIndex(), k=4)

    assert [idx for idx, _score in results] == [7, 2]
    assert [score for _idx, score in results] == pytest.approx([0.95, 0.70])
