# /rag/__init__.py

from .loader import build_index

index, questions, answers = build_index()