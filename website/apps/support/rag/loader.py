# /rag/loader.py

import json
import numpy as np
import faiss
import onnxruntime as ort
from pathlib import Path
from transformers import AutoTokenizer

# Пути
KB_PATH = Path(__file__).parent.parent.parent.parent / "data" / "faq.json"
MODEL_PATH = Path(__file__).parent.parent.parent.parent / "models" / "MiniLM_qint8_avx512_vnni.onnx"
INDEX_PATH = Path(__file__).parent.parent.parent.parent / "models" / "kb_index.faiss"

# ONNX Session
ort_session = ort.InferenceSession(MODEL_PATH)

# Загрузка токенизатора
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def normalize_embeddings(embeddings):
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / norms

def text_to_embedding(text):
    encoded_input = tokenizer(text, padding='max_length', truncation=True, max_length=128, return_tensors="np")

    inputs = {
        "input_ids": encoded_input["input_ids"],
        "attention_mask": encoded_input["attention_mask"],
        "token_type_ids": encoded_input["token_type_ids"]
    }

    outputs = ort_session.run(None, inputs)

    # Убедимся, что мы берём [CLS] токен или делаем mean pooling
    embedding = outputs[0]  # shape: [batch_size, seq_len, hidden_dim]
    
    # Mean pooling — усредняем по seq_len
    embedding = np.mean(embedding, axis=1)  # shape: [batch_size, hidden_dim]

    return normalize_embeddings(embedding)

def load_knowledge_base():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = []
    answers = []

    for pair in data:
        if len(pair) >= 2:
            human = pair[0]["value"]
            gpt = pair[1]["value"]
            questions.append(human)
            answers.append(gpt)

    return questions, answers

def build_index():
    questions, answers = load_knowledge_base()

    print("Генерируем эмбеддинги...")
    embeddings = np.vstack([text_to_embedding(q) for q in questions])

    print("Создаем FAISS индекс...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner Product вместо L2
    index.add(embeddings)

    # Сохраняем индекс
    faiss.write_index(index, str(INDEX_PATH))

    print("Индекс создан и сохранён.")
    return index, questions, answers