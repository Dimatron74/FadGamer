# support/admin.py
from django.contrib import admin
from .models import Products, Category, Ticket, Message, MessageAttachment

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Message)
admin.site.register(MessageAttachment)