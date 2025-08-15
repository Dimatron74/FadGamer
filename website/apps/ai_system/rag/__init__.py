# /rag/__init__.py

from django.conf import settings

def run_ai_model(*args, **kwargs):
    if not getattr(settings, "AI_SYSTEM_ENABLED", True):
        # Возвращаем заглушку или None, если ИИ отключён
        return None
    from .loader import build_index

    index, questions, answers = build_index()

