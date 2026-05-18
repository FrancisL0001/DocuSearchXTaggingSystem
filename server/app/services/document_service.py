import json
import logging
from pathlib import Path

from schemas.response import DocumentResult

logger = logging.getLogger(__name__)


class DocumentService:
    """Loads pre-built metadata and tag assignments at startup; answers document lookups at request time.

    metadata.json is a list ordered to match the FAISS index row positions,
    so FAISS integer position i maps directly to metadata_list[i].
    tags.json is a dict {doc_id: tag_name} produced by cluster_documents.py.
    """

    def __init__(self, metadata_path: Path, tags_path: Path) -> None:
        with metadata_path.open() as f:
            docs: list[dict] = json.load(f)

        # Keep the list for O(1) lookup by FAISS integer position
        self._metadata_list: list[dict] = docs

        # Keep the dict for O(1) lookup by string document ID
        self._metadata_by_id: dict[str, dict] = {d["id"]: d for d in docs}

        with tags_path.open() as f:
            self._tags: dict[str, str] = json.load(f)  # {doc_id: tag_name}

        logger.info("DocumentService loaded %d documents", len(docs))

    # ------------------------------------------------------------------
    # Search path: called with FAISS integer positions + similarity scores
    # ------------------------------------------------------------------

    def get_by_indices(
        self,
        faiss_indices: list[int],
        scores: list[float],
    ) -> list[DocumentResult]:
        """Map FAISS row positions back to DocumentResult objects with their similarity scores."""
        results = []
        for idx, score in zip(faiss_indices, scores):
            # FAISS pads with -1 when top_k > corpus size; skip those
            if idx < 0 or idx >= len(self._metadata_list):
                continue

            doc = self._metadata_list[idx]
            tag = self._tags.get(doc["id"], "Uncategorized")
            results.append(
                DocumentResult(
                    id=doc["id"],
                    title=doc["title"],
                    snippet=doc["snippet"],
                    score=round(float(score), 4),
                    tags=[tag],
                )
            )
        return results

    # ------------------------------------------------------------------
    # Tag-browse path: no search query, just cluster groupings
    # ------------------------------------------------------------------

    def get_all_tags(self) -> dict[str, list[DocumentResult]]:
        """Return every document grouped by its cluster tag, sorted by tag name."""
        groups: dict[str, list[DocumentResult]] = {}
        for doc in self._metadata_list:
            tag = self._tags.get(doc["id"], "Uncategorized")
            result = DocumentResult(
                id=doc["id"],
                title=doc["title"],
                snippet=doc["snippet"],
                score=0.0,
                tags=[tag],
            )
            groups.setdefault(tag, []).append(result)
        return dict(sorted(groups.items()))

    def get_by_tag(self, tag: str) -> list[DocumentResult]:
        """Return all documents belonging to a specific tag cluster."""
        return self.get_all_tags().get(tag, [])

    def get_doc_tags(self, doc_id: str) -> list[str] | None:
        """Return the tag(s) for a document by its string ID, or None if not found."""
        if doc_id not in self._metadata_by_id:
            return None
        tag = self._tags.get(doc_id, "Uncategorized")
        return [tag]

    def all_tag_names(self) -> list[str]:
        return sorted(set(self._tags.values()))
