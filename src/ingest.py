"""Document ingestion utilities.

Example:
    from ingest import ingest_directory
    ingest_directory("data/", "index.faiss")
"""
from __future__ import annotations
import pathlib, logging
from typing import Iterable
import langchain_community.vectorstores as vs
from langchain_community.embeddings import OpenAIEmbeddings
from config import settings

log = logging.getLogger(__name__)

def all_files(root: str | pathlib.Path, suffixes: tuple[str, ...] = (".txt", ".md")) -> Iterable[pathlib.Path]:
    root = pathlib.Path(root)
    for p in root.rglob("*"):
        if p.suffix.lower() in suffixes:
            yield p

def ingest_directory(directory: str | pathlib.Path, index_path: str | pathlib.Path) -> None:
    """Ingests every text-like file under *directory* and writes a FAISS index."""
    directory = pathlib.Path(directory)
    index_path = pathlib.Path(index_path)

    log.info("Scanning %s ...", directory.resolve())
    docs = []
    for file in all_files(directory):
        docs.append(file.read_text(encoding="utf-8"))
    if not docs:
        raise ValueError("No text files found.")

    embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key, model="text-embedding-3-small")
    store = vs.FAISS.from_texts(docs, embeddings)
    store.save_local(str(index_path.with_suffix("")))
    log.info("Saved index to %s", index_path)
