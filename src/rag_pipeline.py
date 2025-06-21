"""RAG pipeline core.

retrieve(query) → prompt(question, context) → openai_chat → answer
"""
from __future__ import annotations
from typing import List
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from config import settings

_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful assistant. Use the following context to answer the question.
Context:
{context}

Question:
{question}

Answer briefly yet completely:""",
)

class RAGPipeline:
    def __init__(self, index_path: str, k: int = 4, model: str = "gpt-4o-mini"):
        self.store = FAISS.load_local(index_path, embeddings=None, allow_dangerous_deserialization=True)
        self.embed = self.store.embedding_function
        self.chat = ChatOpenAI(api_key=settings.openai_api_key, model=model)
        self.k = k

    def _retrieve(self, query: str) -> List[str]:
        docs = self.store.similarity_search(query, k=self.k)
        return [d.page_content for d in docs]

    def __call__(self, question: str) -> str:
        context = "\n---\n".join(self._retrieve(question))
        prompt = _PROMPT.format(context=context, question=question)
        resp = self.chat.invoke(prompt)
        return resp.content.strip()
