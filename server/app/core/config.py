from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Sentence-transformer model name — must match what was used to build the FAISS index
    embedding_model: str = "all-MiniLM-L6-v2"

    # Paths are relative to wherever the server is started from (i.e. server/)
    data_dir: Path = Path("data")
    models_dir: Path = Path("models")

    # How many results /search returns when top_k is not specified by the caller
    default_top_k: int = 5

    # Number of k-means topic clusters — tune this to your corpus size
    n_clusters: int = 8

    # Per-client API rate limits. Search is more expensive because it embeds the query.
    search_rate_limit_per_minute: int = 30
    tags_rate_limit_per_minute: int = 120

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    # lru_cache means the .env file is read exactly once per process lifetime
    return Settings()
