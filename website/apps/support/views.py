from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import PermissionDenied
from .models import Service, Category, Ticket, Message
from .serializers import (
    ServiceSerializer,
    CategorySerializer,
    TicketSerializer,
    MessageSerializer
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


# ==== User Ticket ViewSet (только свои тикеты) ====
class UserTicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def set_status(self, request, pk=None):
        ticket = self.get_object()
        status_value = request.data.get('status')

        if status_value not in dict(Ticket.STATUS_CHOICES):
            return Response({'error': 'Неверный статус'}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = status_value
        ticket.save()

        return Response({'status': ticket.status}, status=status.HTTP_200_OK)


# ==== Admin Ticket ViewSet (все тикеты, только для is_staff) ====
class AdminTicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAdminUser]  # Только для is_staff

    def get_queryset(self):
        return Ticket.objects.all()

    @action(detail=True, methods=['patch'])
    def set_status(self, request, pk=None):
        ticket = self.get_object()
        status_value = request.data.get('status')

        if status_value not in dict(Ticket.STATUS_CHOICES):
            return Response({'error': 'Неверный статус'}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = status_value
        ticket.save()

        return Response({'status': ticket.status}, status=status.HTTP_200_OK)


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

    def perform_update(self, serializer):
        allowed_fields = {'is_deleted'}
        data = self.request.data

        for field in data:
            if field not in allowed_fields:
                raise PermissionDenied(f"Поле '{field}' нельзя редактировать")

        serializer.save()

    lookup_url_kwarg = 'message_id'