"""RAG pipeline core powered by Gemini."""
from __future__ import annotations
from typing import List
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from .config import settings

_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful assistant. Use the following context to answer the question.
Context:
{context}

Question:
{question}

Answer briefly yet completely:""",
)

genai.configure(api_key=settings.gemini_api_key)

class RAGPipeline:
    def __init__(self, index_path: str, k: int = 4, model: str = "gemini-2.5-flash"):
        self.store = FAISS.load_local(index_path, embeddings=None, allow_dangerous_deserialization=True)
        self.embed = self.store.embedding_function
        self.chat = ChatGoogleGenerativeAI(model=model, temperature=0.2)
        self.k = k

    def _retrieve(self, query: str) -> List[str]:
        docs = self.store.similarity_search(query, k=self.k)
        return [d.page_content for d in docs]

    def __call__(self, question: str) -> str:
        context = "\n---\n".join(self._retrieve(question))
        prompt = _PROMPT.format(context=context, question=question)
        resp = self.chat.invoke(prompt)
        return resp.content.strip()
