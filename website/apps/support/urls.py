from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceViewSet,
    UserTicketViewSet,
    AdminTicketViewSet,
    MessageViewSet,
    CategoryList
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'tickets', UserTicketViewSet, basename='user-ticket')  # для обычных пользователей

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    
    # Админские тикеты
    path('admin/tickets/', AdminTicketViewSet.as_view({'get': 'list'})),
    path('admin/tickets/<int:pk>/', AdminTicketViewSet.as_view({'get': 'retrieve'})),
    path('admin/tickets/<int:pk>/set_status/', AdminTicketViewSet.as_view({'patch': 'set_status'})),

    # Сообщения
    path('tickets/<int:ticket_id>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('tickets/<int:ticket_id>/set_status/', UserTicketViewSet.as_view({'patch': 'set_status'})),
    path('tickets/<int:ticket_id>/messages/<int:message_id>/', 
         MessageViewSet.as_view({'patch': 'update', 'delete': 'destroy'})),

    path('', include(router.urls)),
]