import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router
from core.config import get_settings
from core.logging import setup_logging
from search.embeddings import Embedder
from search.faiss_index import FaissIndex
from services.document_service import DocumentService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load all ML artifacts once at startup so every request reuses them in memory."""
    setup_logging()
    settings = get_settings()

    logger.info("Loading embedder: %s", settings.embedding_model)
    app.state.embedder = Embedder(settings.embedding_model)

    index_path = settings.models_dir / "index.faiss"
    logger.info("Loading FAISS index from %s", index_path)
    app.state.faiss_index = FaissIndex.load(index_path)

    logger.info("Loading document metadata and tag assignments")
    app.state.document_service = DocumentService(
        metadata_path=settings.models_dir / "metadata.json",
        tags_path=settings.models_dir / "tags.json",
    )

    logger.info("Server ready")
    yield  # The server runs here; code after yield runs on shutdown

    logger.info("Shutting down")


app = FastAPI(
    title="DocuSearch API",
    description="Semantic search and auto-tagging over policy and research documents",
    version="0.1.0",
    lifespan=lifespan,
)

# Allow the React dev server (Vite default: 5173, CRA default: 3000) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
