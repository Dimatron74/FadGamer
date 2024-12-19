from wagtail.admin.panels import FieldPanel
from django.contrib import admin
from .models import SupportRequest

@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    model = SupportRequest
    menu_label = "Поддержка"
    menu_icon = "help"  # Используйте иконку Wagtail
    add_to_settings_menu = False
    list_display = ('question', 'answered', 'created_at', 'updated_at')
    list_filter = ('answered', 'created_at')
    search_fields = ('question', 'text')
    fields = ('question', 'text', 'answer', 'answered', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')  # Эти поля нельзя редактировать
