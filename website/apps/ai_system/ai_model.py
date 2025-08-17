# ai_model.py

from pathlib import Path
from llama_cpp import Llama
import re
from .rag.retriever import retrieve_relevant_documents
from ..support.models import Message, Ticket
from django.conf import settings

if settings.AI_SYSTEM_ENABLED:
    from llama_cpp import Llama
    from .rag.retriever import retrieve_relevant_documents
    MODEL_PATH = Path(__file__).parent.parent.parent / "models" / "Qwen3-1.7B-UD-Q8_K_XL.gguf"
    llm = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=40000,
        n_threads=2,
        n_gpu_layers=-1,
        verbose=False
    )
else:
    retrieve_relevant_documents = lambda *_args, **_kwargs: []



NO_ANSWER_RESPONSES = {
    "en": "I currently don't have information to answer this question.",
    "ru": "На данный момент у меня нет информации для ответа на этот вопрос.",
    "es": "Actualmente no tengo información para responder a esta pregunta.",
    "fr": "Je n’ai actuellement aucune information pour répondre à cette question.",
    "de": "Ich habe derzeit keine Informationen, um diese Frage zu beantworten.",
    "uk": "Наразі у мене немає інформації, щоб відповісти на це запитання.",
    "zh-cn": "目前我没有足够的信息来回答这个问题。",
    "ja": "現在、この質問に回答するための情報がありません。",
    "ko": "현재 이 질문에 답변할 수 있는 정보가 없습니다.",
    "pt": "Atualmente não tenho informações para responder a essa pergunta.",
    "it": "Al momento non ho informazioni per rispondere a questa domanda.",
    "ar": "في الوقت الحالي ليس لدي معلومات للإجابة على هذا السؤв.",
    "tr": "Şu anda bu soruya cevap vermek için bilgiye sahip değilim.",
    "hi": "वर्तमान में इस प्रश्न का उत्तर देने के लिए मेरे पास जानकारी नहीं है।",
}

from langdetect import detect

def get_no_answer_response(user_query):
    try:
        lang = detect(user_query)
    except:
        lang = "ru"  # fallback

    return lang, NO_ANSWER_RESPONSES.get(lang, NO_ANSWER_RESPONSES["ru"])



SYSTEM_PROMPT = (
    "Вы — сотрудник технической поддержки игровой студии FadGamers. "
    "Ваша задача — отвечать пользователю только на основе информации из базы знаний или истории переписки. "
    "Если точного ответа нет — честно скажите, что не можете помочь с этим вопросом, и попросите временно отключить ИИ и отправить новое сообщение для связи с человеком. "

    "Правила поведения:\n"
    "1. Всегда проверяйте базу знаний перед ответом.\n"
    "2. Если в контексте есть точный ответ — используйте его напрямую без изменений.\n"
    "3. Если точного ответа нет, но есть частично релевантная информация — сделайте краткое обобщение, опираясь только на неё.\n"
    "4. Если информации недостаточно — не пытайтесь угадывать, не добавляйте ничего лишнего.\n"
    "5. Никогда не используйте свои знания или предположения — только то, что в контексте.\n"
    "6. Ответ должен быть структурированным, понятным и на языке пользователя.\n"
    "7. Не призывайте пользователя обращаться повторно в службу поддержки — он уже здесь.\n"
    "8. При отсутствии информации: «На данный момент я не могу вам помочь по этому вопросу. Пожалуйста, временно отключите ИИ и отправьте новое сообщение для связи с сотрудником.»\n"
    "9. Добавьте завершающий тег: </AI_END>"
)

def get_ticket_history(ticket_id):

    try:
        ticket = Ticket.objects.get(id=ticket_id)
        messages = ticket.messages.all().order_by('created_at')

        history = []
        for msg in messages:
            role = 'user' if msg.sender_type == 'user' else 'assistant'
            history.append({
                "role": role,
                "content": msg.text
            })
        return history[:-1]
    except Ticket.DoesNotExist:
        return []

def build_rag_prompt(user_message: str, ticket_id=None):
    relevant_docs = retrieve_relevant_documents(user_message)

    rag_context = ""
    for doc in relevant_docs:
        rag_context += f"Вопрос: {doc['question']}\nОтвет: {doc['answer']}\n\n"

    history = []
    if ticket_id:
        history = get_ticket_history(ticket_id)[-6:]

    # Язык запроса для правильного ответа
    lang, no_answer_text = get_no_answer_response(user_message)

    # Формируем финальный prompt
    full_prompt = [
        {
            "role": "system",
            "content": (
                "ВНИМАНИЕ: Вы обязаны отвечать ТОЛЬКО на основе следующей информации:\n\n"
                f"{rag_context}\n"
                
                "Правила поведения:\n"
                "1. НИКОГДА не добавляйте информацию, которой нет в предоставленной базе знаний или истории диалога.\n"
                "2. Если в базе знаний нет ответа — не выдумывайте, не угадывайте, не дополняйте.\n"
                "3. Если в истории есть дополнительный контекст — используйте его, но не выходите за рамки.\n"
                "4. Отвечайте структурированно, вежливо и на языке пользователя.\n"
                "5. Если ответа нет — ответьте честно, как указано ниже, и добавьте тег </AI_END>.\n"
                f"6. Пример ответа, если информации нет: \"{no_answer_text}\"\n"
                "7. Никогда не просите пользователя связаться с поддержкой снова — он уже здесь.\n"
                "8. Все ответы должны быть основаны исключительно на предоставляемом контексте."
            )
        },
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    # Добавляем историю диалога (до 6 последних сообщений)
    full_prompt.extend(history)

    # Добавляем текущий запрос пользователя
    full_prompt.append({"role": "user", "content": user_message + ' /no_think'})

    return full_prompt

def generate_ai_response(prompt: str, ticket_id=None) -> str:
    if not settings.AI_SYSTEM_ENABLED:
        return "ИИ отключён в настройках администратором. Ответ сформирован не будет."
    
    chat_prompt = build_rag_prompt(prompt, ticket_id=ticket_id)

    output = llm.create_chat_completion(
        messages=chat_prompt,
        max_tokens=1024,
        temperature=0.1,
        top_p=0.8,
        top_k=20,
        min_p=0.05,
        presence_penalty=1.5,
        frequency_penalty=1.2,
        stop=["</AI_END>"]
    )

    response = output["choices"][0]["message"]["content"].strip()

    # Очистка от возможных артефактов
    response = re.sub(r"<[^>]+>", "", response)
    response = response.split("</AI_END>")[0].strip()

    return response or "Сейчас я не могу ответить на ваш запрос. Попробуйте позже."