# scripts/download_models.py

from pathlib import Path
import boto3
import os

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("R2_ENDPOINT"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
)

FILES = [
    "index.faiss",
    "embeddings.npy",
    "metadata.json",
    "tags.json",
    "texts.json",
]

for file_name in FILES:

    file_path = MODEL_DIR / file_name

    if not file_path.exists():

        print(f"Downloading {file_name}...")

        s3.download_file(
            os.getenv("R2_BUCKET"),
            file_name,
            str(file_path),
        )

print("All model artifacts downloaded.")