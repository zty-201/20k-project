"""Document ingestion utilities using Gemini embeddings."""
from __future__ import annotations
import pathlib, logging
from typing import Iterable
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from .config import settings

log = logging.getLogger(__name__)

def all_files(root: str | pathlib.Path, suffixes: tuple[str, ...] = (".txt", ".md")) -> Iterable[pathlib.Path]:
    root = pathlib.Path(root)
    for p in root.rglob("*"):
        if p.suffix.lower() in suffixes:
            yield p

def ingest_directory(directory: str | pathlib.Path, index_path: str | pathlib.Path) -> None:
    """Ingests text files under *directory* and writes a FAISS index."""
    directory = pathlib.Path(directory)
    index_path = pathlib.Path(index_path)

    log.info("Scanning %s ...", directory.resolve())
    docs = [file.read_text(encoding="utf-8") for file in all_files(directory)]
    if not docs:
        raise ValueError("No text files found.")

    embeddings = GoogleGenerativeAIEmbeddings(
        api_key=settings.gemini_api_key,
        model="models/embedding-001"
    )
    store = FAISS.from_texts(docs, embeddings)
    store.save_local(str(index_path.with_suffix("")))
    log.info("Saved index to %s", index_path)
