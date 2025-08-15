# rag/loader.py
import json
import numpy as np
import faiss
from pathlib import Path
from django.conf import settings

KB_PATH = Path(__file__).parent.parent.parent.parent / "data" / "faq.json"
MODEL_PATH = Path(__file__).parent.parent.parent.parent / "models" / "MiniLM_qint8_avx512_vnni.onnx"
INDEX_PATH = Path(__file__).parent.parent.parent.parent / "models" / "kb_index.faiss"

ort_session = None
tokenizer = None

def init_ai_components():
    """Инициализируем модель и токенизатор только при первом вызове."""
    global ort_session, tokenizer
    if not settings.AI_SYSTEM_ENABLED:
        return False
    if ort_session is None or tokenizer is None:
        import onnxruntime as ort
        from transformers import AutoTokenizer
        ort_session = ort.InferenceSession(MODEL_PATH)
        tokenizer = AutoTokenizer.from_pretrained(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
    return True

def normalize_embeddings(embeddings):
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / norms

def text_to_embedding(text):
    if not init_ai_components():
        return None
    encoded_input = tokenizer(text, padding='max_length', truncation=True, max_length=128, return_tensors="np")
    inputs = {
        "input_ids": encoded_input["input_ids"],
        "attention_mask": encoded_input["attention_mask"],
        "token_type_ids": encoded_input["token_type_ids"]
    }
    outputs = ort_session.run(None, inputs)
    embedding = np.mean(outputs[0], axis=1)
    return normalize_embeddings(embedding)

def load_knowledge_base():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    questions, answers = [], []
    for pair in data:
        if len(pair) >= 2:
            questions.append(pair[0]["value"])
            answers.append(pair[1]["value"])
    return questions, answers

def build_index():
    if not settings.AI_SYSTEM_ENABLED:
        return None, [], []
    questions, answers = load_knowledge_base()
    if INDEX_PATH.exists():
        index = faiss.read_index(str(INDEX_PATH))
    else:
        embeddings = np.vstack([text_to_embedding(q) for q in questions])
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)
        faiss.write_index(index, str(INDEX_PATH))
    return index, questions, answers
