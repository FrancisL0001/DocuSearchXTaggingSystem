# PLAN.md — Document Search & Tagging System

## Goal

Build a semantic document search and auto-tagging system over a corpus of 50–100 policy and research documents. Users submit natural-language queries and get back ranked, relevant documents. Documents are automatically tagged by topic using unsupervised clustering — no labeled data required.

---

## Stack

| Layer | Technology |
|---|---|
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector index | FAISS (flat L2 or inner-product index) |
| Clustering / tagging | scikit-learn k-means over document embeddings |
| Backend | FastAPI + Pydantic |
| Frontend | React |
| Scripts | Python (one-off: ingest, embed, index, cluster) |

---

## Architecture

```
corpus (raw docs)
      │
      ▼
[generate_embeddings.py]  →  embeddings (.npy)
      │
      ├──▶ [build_index.py]        →  FAISS index file
      └──▶ [cluster_documents.py]  →  tag assignments per document
                                       (stored alongside doc metadata)

FastAPI server (runtime)
  ├── POST /search   — embed query → FAISS kNN → return ranked docs
  └── GET  /tags     — return documents grouped by cluster tag

React client
  └── search bar + results list with tag chips
```

The embedding, indexing, and clustering steps are **offline scripts** run once (or re-run when the corpus changes). The server loads the pre-built index and metadata at startup; it does not re-embed at request time.

---

## Implementation Phases

### Phase 1 — Data & Offline Pipeline

**Goal:** produce the artifacts the server needs before writing any API code.

- [ ] Collect 50–100 documents (plain text or PDF → text). Store in `server/data/`.
- [ ] `server/app/search/embeddings.py` — `Embedder` class wrapping `SentenceTransformer("all-MiniLM-L6-v2")`. Exposes `encode(texts) -> np.ndarray`.
- [ ] `server/scripts/generate_embeddings.py` — load docs from `server/data/`, encode, save embeddings to `server/models/embeddings.npy` and a matching `server/models/metadata.json` (id, filename, title/snippet).
- [ ] `server/app/search/faiss_index.py` — `FaissIndex` class: `build(embeddings)`, `save(path)`, `load(path)`, `search(query_vec, k) -> [(id, score)]`.
- [ ] `server/scripts/build_index.py` — load embeddings, build FAISS index, save to `server/models/index.faiss`.
- [ ] `server/app/search/clustering.py` — `cluster(embeddings, n_clusters) -> label_array`. Uses scikit-learn `MiniBatchKMeans`. Also produces human-readable tag names (top TF-IDF terms per cluster or ordinal fallback: `Topic 1 … Topic N`).
- [ ] `server/scripts/cluster_documents.py` — load embeddings, run clustering, write `server/models/tags.json` mapping doc id → tag label.

**Done when:** running the three scripts in order produces `embeddings.npy`, `index.faiss`, `metadata.json`, and `tags.json` with no errors.

---

### Phase 2 — FastAPI Backend

**Goal:** a working, tested API over the pre-built artifacts.

- [ ] `server/app/core/config.py` — `Settings` (pydantic-settings): paths to model artifacts, FAISS index, top-k default, number of clusters.
- [ ] `server/app/core/logging.py` — structured logging setup (stdlib `logging`, JSON formatter).
- [ ] `server/app/schemas/query.py` — `SearchQuery(query: str, top_k: int = 5)`.
- [ ] `server/app/schemas/response.py` — `DocumentResult(id, title, snippet, score, tags: list[str])`, `SearchResponse(results: list[DocumentResult])`, `TagsResponse(tags: dict[str, list[DocumentResult]])`.
- [ ] `server/app/services/document_services.py` — `DocumentService`: loads metadata + tags at init, exposes `get_by_ids(ids)`, `get_by_tag(tag)`, `all_tags()`.
- [ ] `server/app/search/retrieval.py` — `retrieve(query: str, k: int) -> list[(id, score)]`: embed query with `Embedder`, call `FaissIndex.search`.
- [ ] `server/app/api/dependencies.py` — FastAPI dependency providers for `DocumentService`, `FaissIndex`, `Embedder` (singletons, loaded once at startup).
- [ ] `server/app/api/routes/search.py` — `POST /search`: validate `SearchQuery`, call retrieval, hydrate results, return `SearchResponse`.
- [ ] `server/app/api/routes/tags.py` — `GET /tags`: return all tag groups via `DocumentService`. `GET /tags/{tag}`: documents for a specific tag.
- [ ] `server/app/api/router.py` — mount both route modules under `/api/v1`.
- [ ] `server/app/main.py` — FastAPI app init, lifespan (load artifacts on startup), mount router, CORS for React dev server.

**Done when:** `uvicorn app.main:app` starts cleanly, `/search` and `/tags` return correct shaped responses.

---

### Phase 3 — React Frontend

**Goal:** interactive UI for search and tag browsing.

- [ ] Initialize React app under `client/` (Vite + React).
- [ ] Search bar component — sends `POST /search`, displays ranked results with title, snippet, score, and tag chips.
- [ ] Tags panel — fetches `GET /tags`, lists topics; clicking a tag filters the result list.
- [ ] Loading and error states for all async calls.
- [ ] Proxy `/api` to `localhost:8000` in Vite config (avoids CORS friction in dev).

**Done when:** typing a query returns results and tag chips match the clustering output.

---

### Phase 4 — Testing

See `docs/TESTING_PLAN.md` for the full test plan. Summary:

- Unit tests: `Embedder`, `FaissIndex`, `clustering`, `DocumentService`.
- Integration tests: `/search` and `/tags` endpoints via FastAPI `TestClient`.
- Pipeline smoke test: run the three scripts end-to-end on a 10-doc fixture corpus and assert artifacts are produced with correct shapes.

**Done when:** `pytest` passes with no failures and key behaviors are covered (see TESTING_PLAN.md).

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| Offline embedding pipeline | Keeps request latency low; avoids recomputing embeddings per query. |
| `all-MiniLM-L6-v2` | Small (80 MB), fast, strong on semantic similarity benchmarks; no GPU required. |
| FAISS flat index | Corpus is small (≤100 docs); exact search is fast enough and avoids approximate-index complexity. |
| k-means on embeddings | No labels needed; clusters reflect semantic proximity already captured by the embeddings. |
| Tag names from TF-IDF | Gives interpretable topic labels without a separate LLM call; degrades gracefully to `Topic N`. |
| Artifacts loaded at startup | Avoids per-request disk I/O; safe because artifacts are read-only during server lifetime. |

---

## Open Questions

- How many clusters (`k`)? Start with `k = 8` for 50–100 docs; expose as a config value so it can be tuned without code changes.
- Tag name quality: TF-IDF top terms are the default. If labels are poor, we can fall back to manual overrides in a `tag_labels.json` config file.
- Document format: plain `.txt` assumed for Phase 1. PDF support can be added via `pdfminer.six` if needed — isolated to the ingestion script.

---

## File Checklist (implementation order)

```
server/app/search/embeddings.py
server/app/search/faiss_index.py
server/app/search/clustering.py
server/scripts/generate_embeddings.py
server/scripts/build_index.py
server/scripts/cluster_documents.py
server/app/core/config.py
server/app/core/logging.py
server/app/schemas/query.py
server/app/schemas/response.py
server/app/services/document_services.py
server/app/search/retrieval.py
server/app/api/dependencies.py
server/app/api/routes/search.py
server/app/api/routes/tags.py
server/app/api/router.py
server/app/main.py
client/  (React app)
server/tests/
docs/TESTING_PLAN.md  (fill in)
```
