from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.support_request, name='support_request'),
]