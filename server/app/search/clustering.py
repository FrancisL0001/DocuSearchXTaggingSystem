import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def cluster(embeddings: np.ndarray, n_clusters: int) -> np.ndarray:
    """Partition document embeddings into n_clusters groups using k-means.

    Returns an integer label array of length N (one cluster id per document).
    random_state=42 keeps results reproducible across runs.
    """
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    return kmeans.fit_predict(embeddings)


def generate_tag_names(
    texts: list[str],
    labels: np.ndarray,
    n_clusters: int,
    top_n: int = 3,
) -> dict[int, str]:
    """Derive a short, human-readable name for each cluster.

    For every cluster, we sum the TF-IDF weights of its member documents and
    pick the top_n terms with the highest aggregate score. Those terms become
    the tag name (e.g. "climate / emissions / carbon").
    Falls back to "Topic N" if a cluster has no documents.
    """
    vectorizer = TfidfVectorizer(max_features=2000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()

    tag_names: dict[int, str] = {}
    for cluster_id in range(n_clusters):
        # Indices of documents that belong to this cluster
        doc_indices = np.where(labels == cluster_id)[0]

        if len(doc_indices) == 0:
            tag_names[cluster_id] = f"Topic {cluster_id + 1}"
            continue

        # Sum TF-IDF weights column-wise across all cluster members
        cluster_tfidf = np.asarray(tfidf_matrix[doc_indices].sum(axis=0)).flatten()

        # The top_n columns with the highest summed weight are the representative terms
        top_indices = cluster_tfidf.argsort()[-top_n:][::-1]
        top_terms = [feature_names[i] for i in top_indices]
        tag_names[cluster_id] = " / ".join(top_terms)

    return tag_names
