import pytest
from src.rag_pipeline import RAGPipeline

@pytest.fixture
def toy_pipeline(tmp_path_factory, monkeypatch):
    idx_dir = tmp_path_factory.mktemp("idx")

    # ---- existing setup ----
    from langchain_community.embeddings.fake import FakeEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import ChatGoogleGenerativeAI

    em = FakeEmbeddings(size=768)
    docs = ["Paris is the capital of France.", "Berlin is the capital of Germany."]
    store = FAISS.from_texts(docs, em)
    store.save_local(str(idx_dir))

    # stub network call
    monkeypatch.setattr(
        ChatGoogleGenerativeAI,
        "invoke",
        lambda self, prompt: type("Resp", (), {"content": "Paris"})()
    )

    # ---- NEW: build pipeline, then re-attach dummy embeddings ----
    from src.rag_pipeline import RAGPipeline
    pipe = RAGPipeline(index_path=str(idx_dir), k=1)
    pipe.store.embedding_function = em.embed_query     # <- crucial line
    return pipe

def test_basic(toy_pipeline):
    assert "Paris" in toy_pipeline("What is the capital of France?")
