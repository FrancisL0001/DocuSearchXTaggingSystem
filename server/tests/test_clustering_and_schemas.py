from __future__ import annotations

import numpy as np
import pytest
from pydantic import ValidationError

from schemas.query import SearchQuery
from search.clustering import cluster, generate_tag_names


def test_search_query_validates_non_empty_query_and_top_k_bounds() -> None:
    assert SearchQuery(query="climate", top_k=3).top_k == 3
    assert SearchQuery(query="climate").top_k == 5

    with pytest.raises(ValidationError):
        SearchQuery(query="", top_k=3)

    with pytest.raises(ValidationError):
        SearchQuery(query="climate", top_k=0)

    with pytest.raises(ValidationError):
        SearchQuery(query="climate", top_k=21)


def test_cluster_returns_one_reproducible_label_per_embedding() -> None:
    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.9, 0.1],
            [0.0, 1.0],
            [0.1, 0.9],
        ],
        dtype="float32",
    )

    first = cluster(embeddings, n_clusters=2)
    second = cluster(embeddings, n_clusters=2)

    assert first.shape == (4,)
    assert set(first.tolist()) == {0, 1}
    np.testing.assert_array_equal(first, second)


def test_generate_tag_names_uses_cluster_terms_and_falls_back_for_empty_clusters() -> None:
    texts = [
        "carbon climate emissions",
        "carbon emissions policy",
        "housing rent affordability",
    ]
    labels = np.array([0, 0, 1])

    tag_names = generate_tag_names(texts, labels, n_clusters=3, top_n=2)

    assert set(tag_names) == {0, 1, 2}
    assert "carbon" in tag_names[0]
    assert any(term in tag_names[1] for term in ["housing", "rent", "affordability"])
    assert tag_names[2] == "Topic 3"
