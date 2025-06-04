from django.urls import path
from . import views

urlpatterns = [
    path('send-email/', views.SendCompanyEmail.as_view(), name='send_company_email'),
]