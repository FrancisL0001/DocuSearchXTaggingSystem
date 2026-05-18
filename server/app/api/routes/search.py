import logging

from fastapi import APIRouter, Depends

from api.dependencies import get_document_service, get_embedder, get_faiss_index
from schemas.query import SearchQuery
from schemas.response import SearchResponse
from search.embeddings import Embedder
from search.faiss_index import FaissIndex
from search.retrieval import retrieve
from services.document_service import DocumentService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(
    body: SearchQuery,
    embedder: Embedder = Depends(get_embedder),
    index: FaissIndex = Depends(get_faiss_index),
    document_service: DocumentService = Depends(get_document_service),
) -> SearchResponse:
    """Semantic search: embed the query, find nearest neighbors in FAISS, return ranked docs."""
    logger.debug("Search query=%r top_k=%d", body.query, body.top_k)

    # retrieve() returns [(faiss_position, cosine_similarity), ...]
    hits = retrieve(body.query, embedder, index, body.top_k)

    faiss_indices = [h[0] for h in hits]
    scores = [h[1] for h in hits]

    results = document_service.get_by_indices(faiss_indices, scores)
    return SearchResponse(results=results, total=len(results))
