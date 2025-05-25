from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .models import Service, Category, Ticket, Message
from .serializers import (
    ServiceSerializer, CategorySerializer,
    TicketSerializer, MessageSerializer
)

# ==== Read-only views ====
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        service_slug = self.request.query_params.get('service')
        if service_slug:
            return Category.objects.filter(service__slug=service_slug)
        return Category.objects.all()

# ==== Ticket views ====
class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ==== Message views ====
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs['ticket_id']
        return Message.objects.filter(ticket_id=ticket_id)

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        sender_type = self.request.data.get('sender_type', 'user')
        author = self.request.user if sender_type != 'ai' else None
        serializer.save(
            ticket_id=ticket_id,
            author=author,
            sender_type=sender_type
        )