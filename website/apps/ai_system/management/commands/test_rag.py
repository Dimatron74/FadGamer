from pathlib import Path

KB_PATH = Path(__file__).parent.parent.parent.parent.parent / "data" / "test_cases.json"

import json
from django.core.management.base import BaseCommand
from ...rag.retriever import retrieve_relevant_documents

class Command(BaseCommand):
    help = 'Тестирование точности поиска в RAG'

    def handle(self, *args, **kwargs):

        try:
            with open(KB_PATH, 'r', encoding='utf-8') as f:
                test_cases = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('❌ Файл test_cases.json не найден'))
            return

        correct_count = 0
        total_count = len(test_cases)

        self.stdout.write("=== ТЕСТИРОВАНИЕ RAG ===\n")

        for idx, case in enumerate(test_cases):
            question = case["question"]
            expected = case["expected_answer"]

            self.stdout.write(f"ТЕСТ #{idx+1}")
            self.stdout.write(f"Вопрос: {question}")

            results = retrieve_relevant_documents(question)
            found = False

            for i, res in enumerate(results):
                answer = res["answer"]
                if expected in answer:
                    correct_count += 1
                    found = True
                    self.stdout.write(f"✅ Найдено в результате #{i+1}")
                    break

            if not found:
                self.stdout.write("❌ Не найдено")
            self.stdout.write("")

        precision = correct_count / total_count * 100 if total_count else 0
        self.stdout.write("=== РЕЗУЛЬТАТЫ ===")
        self.stdout.write(f"Количество тестов: {total_count}")
        self.stdout.write(f"Найдено точно: {correct_count} из {total_count}")
        self.stdout.write(f"Точность: {precision:.2f}%")
        self.stdout.write(self.style.SUCCESS("✅ Тестирование завершено"))