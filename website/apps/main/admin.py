from django.contrib import admin
from .models import Service, AcquisitionMethod, SentEmail, EmailTemplate

admin.site.register(Service)
admin.site.register(AcquisitionMethod)
admin.site.register(SentEmail)
admin.site.register(EmailTemplate)

