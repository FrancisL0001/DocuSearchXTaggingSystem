# DocuSearch

__Live__ : https://docu-search-x-tagging-system.vercel.app/

Semantic document search and auto-tagging over a corpus of policy and research documents.

Type a natural-language query and get back ranked, relevant documents in real time. Documents are automatically grouped into topics using unsupervised clustering — no labeled data required.

---

## What it does

- **Semantic search** — embeds queries with `all-MiniLM-L6-v2` and retrieves the most relevant documents using FAISS vector similarity
- **Auto-tagging** — applies k-means clustering over document embeddings to assign topic tags without any labeled training data
- **Topic browsing** — a sidebar lets you explore documents grouped by their automatically generated topic cluster

## Quickstart

**Prerequisites:** Python 3.11+, Node.js 18+

```bash
# 1. Clone and install backend dependencies
cd server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Build the ML pipeline (run once — takes ~30 s on first run while the model downloads)
python scripts/generate_embeddings.py
python scripts/build_index.py
python scripts/cluster_documents.py

# 3. Start the backend
PYTHONPATH=app uvicorn main:app --reload
# → http://localhost:8000  |  docs at http://localhost:8000/docs

# 4. In a separate terminal, start the frontend
cd ../client
npm install
npm run dev
# → http://localhost:5173
```

Copy `server/.env.example` → `server/.env` and `client/.env.example` → `client/.env` before running if you need to override any defaults.

---

## Stack

| Layer | Technology |
|---|---|
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector search | FAISS (flat inner-product index) |
| Clustering | scikit-learn k-means |
| Backend | FastAPI + Pydantic |
| Frontend | React + TypeScript + Tailwind CSS |

## Project layout

```
server/    FastAPI backend, ML pipeline scripts, corpus data
client/    React + Vite frontend
docs/      PLAN.md, TESTING_PLAN.md
.github/   GitHub Actions CI workflow
```

For setup and usage instructions see the component READMEs:

- [server/README.md](server/README.md) — backend setup, pipeline scripts, API reference
- [client/README.md](client/README.md) — frontend setup and dev workflow

CI runs backend pytest, frontend Vitest tests, and the frontend production build on pushes and pull requests to `main`.

For the full project vision and design decisions see [docs/PLAN.md](docs/PLAN.md).
