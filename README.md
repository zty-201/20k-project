# Gemini RAG Agent with Evaluations

**Now powered by Google Gemini—set `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) in your environment.**

This repository contains scaffolding for a Retrieval‑Augmented Generation (RAG) pipeline powered by **Google Gemini**, plus a notebook and evaluation harness.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # add your GEMINI_API_KEY
pytest -q                   # run unit tests
jupyter lab
```

## Directory layout
* **notebooks/** – walkthrough notebook  
* **src/** – production modules (`config`, `ingest`, `rag_pipeline`, `eval`)  
* **tests/** – pytest suite (network calls monkey‑patched)  
* **.github/workflows/ci.yml** – GitHub Actions CI  
* **requirements.txt**, **pyproject.toml**, **LICENSE**

---

© 2025 Zhang TongYan – MIT License
