from django.urls import path
from .views import SubmitContactRequest

urlpatterns = [
    path('submit/', SubmitContactRequest.as_view(), name='submit_contact'),
]