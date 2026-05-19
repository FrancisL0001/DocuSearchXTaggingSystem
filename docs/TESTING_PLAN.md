# Testing Plan

This plan lists the core behaviors worth testing to keep DocuSearch reliable as the app evolves. Tests should focus on user-visible behavior, data correctness, and pipeline robustness.

## General Behaviors

- The project can be installed and run from documented setup steps.
- Required configuration is validated clearly when missing or invalid.
- Missing model artifacts fail with useful errors instead of silent crashes.
- Search and tag responses keep a stable shape across backend and frontend.
- Empty states are handled gracefully: no documents, no results, no tags.
- Errors are surfaced clearly without exposing internal stack traces to users.
- Common development commands are covered by CI or a repeatable local checklist.

## Server Behaviors

### Offline Pipeline

- `generate_embeddings.py` reads the document corpus and creates matching `embeddings.npy`, `metadata.json`, and `texts.json` artifacts.
- Generated embeddings have the expected shape: one vector per document.
- Metadata preserves stable document ids, titles, filenames, and snippets.
- `build_index.py` creates a loadable FAISS index with the same document count as the embeddings file.
- `cluster_documents.py` creates a tag entry for every document id.
- Pipeline scripts fail clearly when input files or directories are missing.
- A small fixture corpus can run through the full pipeline end to end.

### Search Core

- The embedder returns numeric vectors with consistent dimensions.
- The FAISS wrapper can build, save, load, and search an index.
- Search results are ranked and limited by `top_k`.
- Invalid `top_k` values are rejected or normalized consistently.
- Retrieval handles empty queries and queries with no strong matches predictably.

### Document and Tag Services

- Documents can be loaded by id from metadata.
- Unknown document ids return a controlled error or empty result.
- Tags are grouped correctly and include the expected documents.
- Document/tag joins remain correct when a document has no tag or an unknown tag.

### API

- `POST /api/v1/search` validates request bodies.
- Search responses include id, title, snippet, score, and tags for each result.
- `GET /api/v1/tags` returns all tag groups in the documented response shape.
- `GET /api/v1/documents/{id}/tags` returns tags for a known document.
- API errors use consistent status codes and response bodies.
- App startup loads artifacts once and reports startup failures clearly.

## Client Behaviors

### Search UI

- The user can type a query and submit it.
- Search requests are sent to the correct API route.
- Results render title, snippet, score, and tag chips.
- Loading, empty, and error states are visible and understandable.
- Repeated searches replace old results without stale state leaking through.

### Tag Browsing

- Tags load from the backend on page load.
- Tag groups render with readable labels and document counts.
- Selecting a tag filters or displays the matching documents.
- Clearing or changing the selected tag restores the expected result view.
- Tag loading failures do not break the whole page.

### API Contract

- Frontend TypeScript types match backend response schemas.
- Client code handles missing optional fields defensively.
- Network failures and non-2xx responses show user-facing error states.

### Build and Accessibility

- The production build completes successfully.
- Main workflows are keyboard usable.
- Form controls have accessible labels or names.
- Important text has sufficient contrast and does not overlap on mobile layouts.

## Test Levels

- **Unit tests:** small behavior tests for embedder, FAISS wrapper, clustering, document services, API clients, and React components.
- **Integration tests:** FastAPI endpoints with test artifacts; React flows with mocked API responses.
- **Smoke tests:** full offline pipeline on a small fixture corpus; frontend build; backend startup with prepared artifacts.
