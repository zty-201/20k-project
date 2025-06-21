# demo_rag.py
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.rag_pipeline import RAGPipeline
from src.config import settings

# 1) Build a tiny index in ./scratch_index
docs = [
    "Paris is the capital of France.",
    "Berlin is the capital of Germany.",
]
emb = GoogleGenerativeAIEmbeddings(api_key=settings.gemini_api_key,
                                   model="models/embedding-001")
index_dir = "scratch_index"
store = FAISS.from_texts(docs, emb)
store.save_local(index_dir)

# 2) Make the pipeline
pipe = RAGPipeline(index_path=index_dir, k=1)

pipe.store.embedding_function = emb 

# 3) Fire a few questions
for q in [
    "What is the capital of France?",
    "And what about Germany?",
]:
    print(f"Q: {q}")
    print("A:", pipe(q))
    print("-" * 40)
