from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from apps.profiles.models import User

@register_snippet
class SupportRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answered = models.BooleanField(default=False)
    answer = models.TextField(blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [   
                FieldPanel("user", heading="Никнейм пользователя", read_only=True),
                FieldPanel("question", heading="Вопрос", read_only=True),  # Поле для отображения вопроса
                FieldPanel("text", heading="Текст вопроса", read_only=True),      # Поле для отображения текста
            ],
            heading="Контекст запроса",
        ),
        MultiFieldPanel(
            [
                FieldPanel("answer", heading="Ответ"),    # Редактируемое поле для ответа
            ],
            heading="Ответы и статус",
        ),
    ]

    api_fields = [
        APIField("question"),
        APIField("text"),
        APIField("answer"),
        APIField("answered"),
        APIField("created_at"),
        APIField("updated_at"),
    ]
    
    class Meta:
        verbose_name = "Запрос"  # Единственное число
        verbose_name_plural = "Запросы в поддержку"

    def __str__(self):
        return self.question