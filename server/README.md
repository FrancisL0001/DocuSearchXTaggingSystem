# DocuSearch — Backend

FastAPI backend for semantic document search and auto-tagging.

## Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

## Setup

```bash
cd server
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Build the ML pipeline (run once)

These three scripts must be run in order before starting the server. Each one produces the artifacts the next step depends on.

```bash
# 1. Embed all documents — outputs models/metadata.json, models/texts.json, models/embeddings.npy
python scripts/generate_embeddings.py

# 2. Build the FAISS vector index — outputs models/index.faiss
python scripts/build_index.py

# 3. Cluster documents into topics — outputs models/tags.json
python scripts/cluster_documents.py
```

All scripts read settings from `.env`. Re-run from step 1 if the corpus changes.

## Start the server

Run from the `server/` directory so relative paths (`data/`, `models/`) resolve correctly.
`PYTHONPATH=app` puts `server/app/` on the Python path so the bare-module imports in `main.py` are found.

```bash
# macOS / Linux
PYTHONPATH=app uvicorn main:app --reload

# Windows (PowerShell)
$env:PYTHONPATH="app"; uvicorn main:app --reload
```

Server runs at `http://localhost:8000`. Auto-docs at `http://localhost:8000/docs`.

## Configuration

Edit `.env` to override defaults:

| Variable | Default | Description |
|---|---|---|
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformer model name |
| `DATA_DIR` | `data` | Directory containing the corpus zip |
| `MODELS_DIR` | `models` | Where pipeline artifacts are saved/loaded |
| `DEFAULT_TOP_K` | `5` | Default number of search results |
| `N_CLUSTERS` | `8` | Number of k-means topic clusters |

## API endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/search` | Semantic search — returns ranked documents |
| `GET` | `/api/v1/tags` | All topic clusters with their documents |
| `GET` | `/api/v1/documents/{id}/tags` | Tags assigned to a specific document |

### Search request body

```json
{ "query": "carbon emissions policy", "top_k": 8 }
```

## Docker

```bash
# Build and run (requires models/ artifacts to already exist)
docker build -t docusearch-server .
docker run -p 8000:8000 docusearch-server
```

## Project structure

```
server/
├── app/
│   ├── api/          HTTP routes and dependency injection
│   ├── core/         Settings and logging
│   ├── schemas/      Pydantic request/response models
│   ├── search/       Embedder, FAISS index, clustering, retrieval
│   ├── services/     DocumentService — metadata and tag lookups
│   └── main.py       FastAPI entry point
├── data/             Corpus zip (not committed)
├── models/           Pipeline artifacts (not committed)
├── scripts/          One-off pipeline scripts
└── tests/            pytest test suite
```
