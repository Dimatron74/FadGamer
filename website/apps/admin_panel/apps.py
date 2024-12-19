from django.apps import AppConfig
from wagtail import hooks

class Admin_panelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin_panel'
    verbose_name = 'Админ Панель'

    # def ready(self):
    #     from .models import SupportPage

    #     hooks.register('register_page_models', lambda: [SupportPage])

