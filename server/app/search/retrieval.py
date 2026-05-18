from search.embeddings import Embedder
from search.faiss_index import FaissIndex


def retrieve(
    query: str,
    embedder: Embedder,
    index: FaissIndex,
    k: int,
) -> list[tuple[int, float]]:
    """Embed a natural-language query and return the k nearest document positions.

    Returns a list of (faiss_position, cosine_similarity) pairs ordered
    from highest similarity to lowest. faiss_position is the integer row
    in the FAISS index, which matches the row order in metadata.json.
    """
    # Encode the query into the same vector space as the document embeddings
    query_vec = embedder.encode([query])[0]  # Shape: (D,)

    scores, indices = index.search(query_vec, k)

    # Filter out FAISS sentinel values (-1 appears when k > corpus size)
    return [
        (int(idx), float(score))
        for idx, score in zip(indices, scores)
        if idx >= 0
    ]
