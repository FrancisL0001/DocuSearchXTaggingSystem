from fastapi import Request

from app.search.embeddings import Embedder
from app.search.faiss_index import FaissIndex
from app.services.document_service import DocumentService


# These functions are used as FastAPI dependency injectors (Depends(...)).
# They pull the singleton objects that were loaded into app.state at server startup,
# so every request reuses the same in-memory model and index rather than reloading them.

def get_embedder(request: Request) -> Embedder:
    return request.app.state.embedder


def get_faiss_index(request: Request) -> FaissIndex:
    return request.app.state.faiss_index


def get_document_service(request: Request) -> DocumentService:
    return request.app.state.document_service
