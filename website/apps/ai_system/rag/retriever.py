# rag/retriever.py
from django.conf import settings
from .loader import build_index, text_to_embedding

index, questions, answers = (None, [], [])
if settings.AI_SYSTEM_ENABLED:
    index, questions, answers = build_index()

def retrieve_relevant_documents(query: str, top_k=2):
    if not settings.AI_SYSTEM_ENABLED:
        return []
    query_emb = text_to_embedding(query)
    if query_emb is None or index is None:
        return []
    D, I = index.search(query_emb, top_k)
    results = []
    for idx in I[0]:
        if idx != -1:
            results.append({"question": questions[idx], "answer": answers[idx]})
    return results
