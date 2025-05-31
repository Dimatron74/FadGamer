# /rag/retriever.py

from . import index, questions, answers
from .loader import text_to_embedding

def retrieve_relevant_documents(query: str, top_k=2):
    query_emb = text_to_embedding(query)

    D, I = index.search(query_emb, top_k)

    results = []
    for idx in I[0]:
        if idx != -1:
            results.append({
                "question": questions[idx],
                "answer": answers[idx]
            })
    return results