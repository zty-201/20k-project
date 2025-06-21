"""Simple evaluation harness.

Computes exact match & BLEU between answers and references.
Extend as needed.
"""
from __future__ import annotations
import json, pathlib
from typing import Sequence
from rag_pipeline import RAGPipeline
from nltk.translate.bleu_score import corpus_bleu

def evaluate(pipeline: RAGPipeline, dataset_path: str | pathlib.Path) -> dict[str, float]:
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    predictions, references = [], []
    for row in data:
        pred = pipeline(row["question"])
        predictions.append(pred.split())
        references.append([row["answer"].split()])

    bleu = corpus_bleu(references, predictions)
    exact = sum(" ".join(p) == " ".join(r[0]) for p, r in zip(predictions, references)) / len(data)
    return {"BLEU": bleu, "Exact": exact}
