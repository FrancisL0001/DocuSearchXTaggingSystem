import logging

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_document_service
from schemas.response import TagGroup, TagsResponse
from services.document_service import DocumentService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/tags", response_model=TagsResponse)
def get_all_tags(
    document_service: DocumentService = Depends(get_document_service),
) -> TagsResponse:
    """Return every topic cluster with its member documents (for the tag-browse panel)."""
    groups = document_service.get_all_tags()
    tags = [TagGroup(tag=tag, documents=docs) for tag, docs in groups.items()]
    return TagsResponse(tags=tags)


@router.get("/documents/{doc_id}/tags", response_model=list[str])
def get_document_tags(
    doc_id: str,
    document_service: DocumentService = Depends(get_document_service),
) -> list[str]:
    """Return the topic tag(s) assigned to a single document by its ID."""
    tags = document_service.get_doc_tags(doc_id)
    if tags is None:
        raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")
    return tags
