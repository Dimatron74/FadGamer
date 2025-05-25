from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, TicketViewSet, MessageViewSet, CategoryList

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('tickets/<int:ticket_id>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('tickets/<int:pk>/set_status/', TicketViewSet.as_view({'patch': 'set_status'})),
    path('tickets/<int:ticket_id>/messages/<int:message_id>/', 
         MessageViewSet.as_view({'patch': 'update', 'delete': 'destroy'})),
    path('', include(router.urls)),
]