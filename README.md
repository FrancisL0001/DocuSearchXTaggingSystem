# DocuSearch

Semantic document search and auto-tagging over a corpus of policy and research documents.

Type a natural-language query and get back ranked, relevant documents in real time. Documents are automatically grouped into topics using unsupervised clustering — no labeled data required.

---

## What it does

- **Semantic search** — embeds queries with `all-MiniLM-L6-v2` and retrieves the most relevant documents using FAISS vector similarity
- **Auto-tagging** — applies k-means clustering over document embeddings to assign topic tags without any labeled training data
- **Topic browsing** — a sidebar lets you explore documents grouped by their automatically generated topic cluster

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
server/   FastAPI backend, ML pipeline scripts, corpus data
client/   React + Vite frontend
docs/     PLAN.md, TESTING_PLAN.md
```

For setup and usage instructions see the component READMEs:

- [server/README.md](server/README.md) — backend setup, pipeline scripts, API reference
- [client/README.md](client/README.md) — frontend setup and dev workflow

For the full project vision and design decisions see [docs/PLAN.md](docs/PLAN.md).
