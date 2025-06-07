import json
import time
import difflib
from django.core.management.base import BaseCommand
from ...ai_model import generate_ai_response
from pathlib import Path

KB_PATH = Path(__file__).parent.parent.parent.parent.parent / "data" / "test_cases.json"

def is_relevant_response(expected, generated, threshold=0.85):
    expected_clean = expected.strip().lower()
    generated_clean = generated.strip().lower()

    # Полное совпадение
    if expected_clean == generated_clean:
        return True

    # Сравнение через SequenceMatcher
    ratio = difflib.SequenceMatcher(None, expected_clean, generated_clean).ratio()
    return ratio >= threshold


class Command(BaseCommand):
    help = 'Тестирование качества генерации ответа моделью Qwen3-1.7B'

    def handle(self, *args, **kwargs):

        try:
            with open(KB_PATH, 'r', encoding='utf-8') as f:
                test_cases = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('❌ Файл test_cases.json не найден'))
            return

        correct_count = 0
        total_time = 0
        total_count = len(test_cases)

        self.stdout.write("=== ТЕСТИРОВАНИЕ ГЕНЕРАЦИИ ОТВЕТОВ ===\n")

        for idx, case in enumerate(test_cases):
            question = case["question"]
            expected = case["expected_answer"]

            self.stdout.write(f"ТЕСТ #{idx + 1}")
            self.stdout.write(f"Вопрос: {question}")

            start_time = time.time()
            generated_answer = generate_ai_response(question)
            end_time = time.time()

            elapsed_time = end_time - start_time
            total_time += elapsed_time

            self.stdout.write(f"Ответ модели: {generated_answer[:200]}...")  # показываем начало
            self.stdout.write(f"⏳ Время генерации: {elapsed_time:.2f} сек.")

            if is_relevant_response(expected, generated_answer, threshold=0.85):
                correct_count += 1
                self.stdout.write("✅ Ответ релевантен")
            else:
                self.stdout.write("❌ Ответ не совпадает с эталоном")

            self.stdout.write("")  # пустая строка

        accuracy = correct_count / total_count * 100 if total_count else 0
        avg_time = total_time / total_count if total_count else 0

        self.stdout.write("=== ИТОГОВЫЕ РЕЗУЛЬТАТЫ ===")
        self.stdout.write(f"Количество тестов: {total_count}")
        self.stdout.write(f"Релевантных ответов: {correct_count} из {total_count}")
        self.stdout.write(f"Точность: {accuracy:.2f}%")
        self.stdout.write(f"Среднее время генерации: {avg_time:.2f} секунд")
        self.stdout.write(self.style.SUCCESS("✅ Тестирование завершено"))