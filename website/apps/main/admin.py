from django.contrib import admin
from .models import Service, AcquisitionMethod

admin.site.register(Service)
admin.site.register(AcquisitionMethod)