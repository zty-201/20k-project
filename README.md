# OpenAI RAG Agent with Evaluations

This repository contains an example notebook and scaffolding for building a Retrieval‑Augmented Generation (RAG) pipeline powered by OpenAI models, along with an evaluation harness.

## Contents
* **notebooks/openai_rag_agent_w_evals.ipynb** – Interactive Jupyter Notebook that walks through:
  * Setting up environment variables securely
  * Creating an index over your documents
  * Implementing a simple RAG pipeline
  * Running automatic and manual evaluation
* **src/** – Place for production‑grade Python modules (empty for now).
* **tests/** – Placeholder for unit and integration tests.
* **requirements.txt** – Minimal Python dependencies.
* **.gitignore** – Standard Python ignores.
* **LICENSE** – MIT License.

## Quick start
```bash
# Clone the repo and create a virtual environment
git clone <your‑fork‑url>
cd openai_rag_agent_repo
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install deps
pip install -r requirements.txt

# Launch Jupyter
jupyter lab
```

## Deployment
Feel free to refactor the notebook into production‑ready scripts inside **src/** and add tests in **tests/**. CI/CD is left to you – GitHub Actions works great with Python and Jupyter.

## Contributing
Pull requests are welcome! Please open an issue first to discuss major changes.

---
© 2025 Zhang TongYan – released under the MIT License.
