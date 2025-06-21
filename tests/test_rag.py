import pytest
from src.rag_pipeline import RAGPipeline

@pytest.fixture(scope="session")
def toy_pipeline(tmp_path_factory):
    # Create a minimal FAISS index in a temp dir
    idx_dir = tmp_path_factory.mktemp("idx")
    from langchain_community.embeddings import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    em = OpenAIEmbeddings()
    docs = ["Paris is the capital of France.", "Berlin is the capital of Germany."]
    store = FAISS.from_texts(docs, em)
    store.save_local(str(idx_dir))
    return RAGPipeline(index_path=str(idx_dir), k=1, model="gpt-3.5-turbo")

def test_basic(toy_pipeline, monkeypatch):
    monkeypatch.setattr("src.rag_pipeline.ChatOpenAI.invoke", lambda self, prompt: type("Resp",(object,),{"content":"Paris"})())
    assert "Paris" in toy_pipeline("What is the capital of France?")
