# convert_to_onnx.py

from sentence_transformers import SentenceTransformer
import torch
import torch.nn as nn
import numpy as np
from pathlib import Path

class TextEncoder(torch.nn.Module):
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        super().__init__()
        self.model = SentenceTransformer(model_name)

    def forward(self, texts):
        # Предполагаем, что texts — это list[str]
        embeddings = self.model.encode(texts, convert_to_tensor=True)
        return embeddings.detach().cpu().numpy()

# Пример входного значения
dummy_input = ["Пример текста"]

# Загружаем модель
encoder = TextEncoder()

# Упаковываем как TorchScript
script_model = torch.jit.trace(encoder, dummy_input)
script_model.save("text_encoder.pt")

print("✅ TorchScript модель сохранена как text_encoder.pt")

# Конвертируем в ONNX
onnx_output_path = Path(__file__).parent.parent.parent.parent / "models" / "MiniLM.onnx"

# Делаем export
torch.onnx.export(
    encoder,
    dummy_input,
    onnx_output_path,
    export_params=True,
    opset_version=13,
    do_constant_folding=True,
    input_names=["input_text"],
    output_names=["output"],
    dynamic_axes={
        "input_text": {0: "batch_size"},
        "output": {0: "batch_size"}
    },
    verbose=False,
    input_dtype=torch.long  # Тип данных для токенайзера
)

print(f"✅ ONNX модель успешно сохранена как {onnx_output_path}")