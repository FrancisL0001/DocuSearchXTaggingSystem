#!/usr/bin/env python3
"""Generate sentence-transformer embeddings for all documents in the corpus zip.

Run from the server/ directory:
    python scripts/generate_embeddings.py

Outputs written to models/:
    metadata.json   — list of {id, title, topic, date, source, snippet}
                      ordered to match the FAISS index row positions
    texts.json      — list of full document texts (needed by cluster_documents.py)
    embeddings.npy  — (N, D) float32 array, row i matches metadata[i]
"""
import json
import sys
import zipfile
from pathlib import Path

import numpy as np

# Allow importing from app/ without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import get_settings
from app.search.embeddings import Embedder


def parse_header(raw_text: str) -> tuple[dict, str]:
    """Split a document into its key:value header block and plain-text body.

    The header is the first run of "Key: Value" lines before the first blank line.
    Everything after that blank line is the body.
    Returns (header_dict, body_text).
    """
    lines = raw_text.strip().splitlines()
    header: dict = {}
    body_start = 0

    for i, line in enumerate(lines):
        if ":" in line and i < 10:  # Header lines appear in the first 10 rows
            key, _, value = line.partition(":")
            header[key.strip().lower()] = value.strip()
        elif line.strip() == "" and header:
            body_start = i + 1
            break

    body = "\n".join(lines[body_start:]).strip()
    return header, body


def main() -> None:
    settings = get_settings()
    zip_path = settings.data_dir / "articles_corpus.zip"
    models_dir = settings.models_dir
    models_dir.mkdir(exist_ok=True)

    print(f"Reading corpus: {zip_path}")

    metadata_list: list[dict] = []
    texts: list[str] = []

    with zipfile.ZipFile(zip_path) as zf:
        # Sort so the output order is deterministic regardless of zip internal order
        txt_names = sorted(name for name in zf.namelist() if name.endswith(".txt"))

        for name in txt_names:
            content = zf.read(name).decode("utf-8")
            header, body = parse_header(content)

            doc_id = header.get("id", Path(name).stem)
            title = header.get("title", Path(name).stem)

            # Truncate to ~220 chars for the UI result-card snippet
            snippet = body[:220].replace("\n", " ").strip()

            metadata_list.append({
                "id": doc_id,
                "title": title,
                "topic": header.get("topic", ""),
                "date": header.get("date", ""),
                "source": header.get("source", ""),
                "snippet": snippet,
            })

            # Prepend the title so the embedding captures topic + content signal
            texts.append(f"{title}. {body}")

    print(f"Parsed {len(texts)} documents")
    print("Encoding embeddings — this may take ~30 s on first run (model download included)…")

    embedder = Embedder(settings.embedding_model)
    embeddings = embedder.encode(texts)  # Returns (N, D) float32

    # Save the three artifacts that downstream scripts depend on
    meta_path = models_dir / "metadata.json"
    texts_path = models_dir / "texts.json"
    emb_path = models_dir / "embeddings.npy"

    with meta_path.open("w") as f:
        json.dump(metadata_list, f, indent=2)

    with texts_path.open("w") as f:
        json.dump(texts, f)

    np.save(emb_path, embeddings)

    print(f"\nSaved to {models_dir}/")
    print(f"  {meta_path.name}  ({len(metadata_list)} docs)")
    print(f"  {texts_path.name}")
    print(f"  {emb_path.name}  shape={embeddings.shape}")


if __name__ == "__main__":
    main()
