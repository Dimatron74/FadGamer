# website/apps/support/admin.py
from django.contrib import admin
from apps.support.models import SupportRequest

# class SupportRequestAdmin(admin.ModelAdmin):
#     list_display = ('question', 'text', 'created_at', 'answered')
#     search_fields = ('question',)

# admin.site.register(SupportRequest, SupportRequestAdmin)