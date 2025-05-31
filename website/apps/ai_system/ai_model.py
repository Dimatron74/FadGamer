# ai_model.py

from pathlib import Path
from llama_cpp import Llama
import re
from .rag.retriever import retrieve_relevant_documents
from ..support.models import Message, Ticket

# Путь к модели
MODEL_PATH = Path(__file__).parent.parent.parent / "models" / "Qwen3-1.7B-UD-Q8_K_XL.gguf"

# Загружаем модель с кастомным шаблоном
llm = Llama(
    model_path=str(MODEL_PATH),
    n_ctx=40000,
    n_threads=2,
    n_gpu_layers=-1,
    verbose=False
)



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
    "Вы — квалифицированный сотрудник технической поддержки игровой студии FadGamers. "
    "Вы получаете вопросы пользователей и обязаны отвечать только на основе информации из контекста выше или истории переписки. "
    "Пользователь уже находится в службе поддержки — НЕ призывайте его обращаться в поддержку повторно. "
    "Если в контексте или истории нет точного ответа — честно скажите, что не можете помочь с этим вопросом, и попросите пользователя отключить ИИ и отправить новое сообщение для связи с человеком. "
    "Никогда не опирайтесь на свои знания или догадки. "
    "Отвечайте вежливо, структурированно и на языке пользователя. "
    "Добавьте завершающий тег: </AI_END>"
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

    # Получаем историю сообщений
    history = []
    if ticket_id:
        history = get_ticket_history(ticket_id)[-6:]

    rag_prompt = (
        "ВНИМАНИЕ: Вы обязаны отвечать строго по информации из следующей базы знаний:\n\n"
        f"{rag_context}\n\n"
        
        "Правила поведения:\n"
        "1. Всегда проверяйте базу знаний перед ответом.\n"
        "2. Если в базе есть точный ответ — используйте его напрямую.\n"
        "3. Если точного ответа нет, но есть частично релевантный контекст — сделайте обобщение на основе него.\n"
        "4. Если контекста нет, но есть история сообщений — опирайтесь на неё, чтобы дать логичный ответ.\n"
        "5. НИКОГДА не добавляйте информацию, которой нет в контексте или истории.\n"
        "6. ВАЖНО, НИКОГДА не выдумывайте, не предполагайте, не угадывайте.\n"
        f"7. Ответ должен быть на языке {get_no_answer_response(user_message)[0]}, вежливым и структурированным.\n"
        "8. НЕ призывайте пользователя обращаться в службу поддержки — он уже находится в ней.\n"
        "9. Если ответа нет ни в контексте, ни в истории — честно скажите об этом и попросите пользователя отключить ИИ и отправить новое сообщение для связи с сотрудником."
        # f"9. Если вы совсем не знаете ответа — скажите: {get_no_answer_response(user_message)[1]}\n"
    )

    full_prompt = [
        {"role": "system", "content": rag_prompt},
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    # Добавляем историю
    full_prompt.extend(history)

    # Добавляем текущий запрос
    full_prompt.append({"role": "user", "content": user_message + ' /no_think'})

    print(full_prompt)
    return full_prompt

def generate_ai_response(prompt: str, ticket_id=None) -> str:
    chat_prompt = build_rag_prompt(prompt, ticket_id=ticket_id)

    output = llm.create_chat_completion(
        messages=chat_prompt,
        max_tokens=1024,
        temperature=0.3,
        top_p=0.8,
        top_k=20,
        min_p=0,
        presence_penalty=1.5,
        stop=["</AI_END>"]
    )

    response = output["choices"][0]["message"]["content"].strip()

    # Очистка от возможных артефактов
    response = re.sub(r"<[^>]+>", "", response)
    response = response.split("</AI_END>")[0].strip()

    return response or "Сейчас я не могу ответить на ваш запрос. Попробуйте позже."