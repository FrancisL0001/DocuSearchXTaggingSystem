#!/usr/bin/env python3
"""Build a FAISS flat inner-product index from pre-computed document embeddings.

Run from the server/ directory (after generate_embeddings.py):
    python scripts/build_index.py

Reads:   models/embeddings.npy
Writes:  models/index.faiss
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import get_settings
from app.search.faiss_index import FaissIndex


def main() -> None:
    settings = get_settings()
    emb_path = settings.models_dir / "embeddings.npy"
    index_path = settings.models_dir / "index.faiss"

    print(f"Loading embeddings from {emb_path}")
    embeddings = np.load(emb_path)  # Shape: (N, D)

    print(f"Building FAISS index  N={embeddings.shape[0]}  D={embeddings.shape[1]}")
    faiss_index = FaissIndex(dimension=embeddings.shape[1])
    faiss_index.add(embeddings)

    faiss_index.save(index_path)
    print(f"Saved index → {index_path}  ({faiss_index.index.ntotal} vectors indexed)")


if __name__ == "__main__":
    main()
