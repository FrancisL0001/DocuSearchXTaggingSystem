#!/usr/bin/env python3
"""Run k-means clustering over document embeddings and save per-document topic tags.

Run from the server/ directory (after generate_embeddings.py):
    python scripts/cluster_documents.py

Reads:   models/embeddings.npy  models/metadata.json  models/texts.json
Writes:  models/tags.json  →  {doc_id: tag_name}
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import get_settings
from app.search.clustering import cluster, generate_tag_names


def main() -> None:
    settings = get_settings()
    models_dir = settings.models_dir

    embeddings = np.load(models_dir / "embeddings.npy")

    with (models_dir / "metadata.json").open() as f:
        metadata: list[dict] = json.load(f)

    with (models_dir / "texts.json").open() as f:
        texts: list[str] = json.load(f)

    n_clusters = settings.n_clusters
    print(f"Clustering {len(texts)} documents into {n_clusters} topics…")

    # Integer cluster label for each document (row order matches metadata/embeddings)
    labels = cluster(embeddings, n_clusters=n_clusters)

    # Derive human-readable names from top TF-IDF terms per cluster
    tag_names = generate_tag_names(texts, labels, n_clusters=n_clusters)

    print("\nCluster tag names:")
    for cluster_id, name in sorted(tag_names.items()):
        count = int((labels == cluster_id).sum())
        print(f"  [{cluster_id}]  {name!r}  ({count} docs)")

    # Build the final mapping: string doc ID → tag name
    tags: dict[str, str] = {
        meta["id"]: tag_names[int(label)]
        for meta, label in zip(metadata, labels)
    }

    out_path = models_dir / "tags.json"
    with out_path.open("w") as f:
        json.dump(tags, f, indent=2)

    print(f"\nSaved tag assignments → {out_path}")


if __name__ == "__main__":
    main()
