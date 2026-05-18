from pathlib import Path

import faiss
import numpy as np


class FaissIndex:
    """Wraps a FAISS flat inner-product index for exact nearest-neighbor search.

    Because all embeddings are L2-normalized, inner product == cosine similarity,
    so the returned scores are directly interpretable as similarity values in [-1, 1].
    """

    def __init__(self, dimension: int) -> None:
        # IndexFlatIP: brute-force exact search using inner product
        self.index = faiss.IndexFlatIP(dimension)
        self.dimension = dimension

    def add(self, embeddings: np.ndarray) -> None:
        """Add all document vectors to the index (called once during the build script)."""
        self.index.add(embeddings.astype("float32"))

    def search(self, query_vec: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
        """Find the k nearest neighbors of query_vec.

        Returns (scores, indices) as 1-D arrays of length k.
        FAISS uses -1 as a sentinel index when k > number of indexed vectors.
        """
        query_vec = query_vec.astype("float32").reshape(1, -1)
        scores, indices = self.index.search(query_vec, k)
        return scores[0], indices[0]

    def save(self, path: Path) -> None:
        faiss.write_index(self.index, str(path))

    @classmethod
    def load(cls, path: Path) -> "FaissIndex":
        """Deserialize a previously saved FAISS index from disk."""
        raw_index = faiss.read_index(str(path))
        instance = cls.__new__(cls)
        instance.index = raw_index
        instance.dimension = raw_index.d
        return instance
