import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    """Thin wrapper around a SentenceTransformer model."""

    def __init__(self, model_name: str) -> None:
        # Downloads the model on first use and caches it locally (~80 MB for MiniLM)
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        """Return a (N, D) float32 embedding matrix for a list of texts.

        normalize_embeddings=True ensures each vector has unit length,
        which lets us use inner product as a direct cosine similarity measure.
        """
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
