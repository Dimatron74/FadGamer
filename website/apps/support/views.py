from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import PermissionDenied
from .models import Service, Category, Ticket, Message
from django.db.models import Case, When, Value, IntegerField, DateTimeField, F, Q
from .ai_model import generate_ai_response
from django.db import transaction
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .serializers import (
    ServiceSerializer,
    CategorySerializer,
    TicketSerializer,
    MessageSerializer
)

# Создаем пул потоков
executor = ThreadPoolExecutor(max_workers=1)

# Функция для запуска async-функций в sync-контексте
def run_async_in_thread(func, *args):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(func(*args))


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

    @transaction.atomic
    def perform_create(self, serializer):
        # Сохраняем тикет
        ticket = serializer.save(user=self.request.user)

        # # Создаем первое сообщение от пользователя — из description
        # user_message = Message.objects.create(
        #     ticket=ticket,
        #     text=ticket.description,
        #     author=ticket.user,
        #     sender_type='user'
        # )

        # Отправляем задачу в пул потоков
        executor.submit(run_async_in_thread, self.generate_and_save_ai_reply, ticket.description, ticket.id)

    def generate_and_save_ai_reply(self, prompt, ticket_id):
        ai_response = generate_ai_response(prompt)
        ticket = Ticket.objects.get(id=ticket_id)
        Message.objects.create(
            ticket=ticket,
            text=ai_response,
            sender_type='ai'
        )


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
        return Ticket.objects.order_by(
            Case(
                When(status='open', then=Value(0)),
                When(status='in_progress', then=Value(1)),
                When(status='closed', then=Value(2)),
                output_field=IntegerField()
            ),
            # Для open — сортировка по возрастанию (FIFO)
            Case(
                When(status='open', then=F('last_message_time')),
                default=None,
                output_field=DateTimeField()
            ).asc(nulls_last=True),
            # Для in_progress — по убыванию (LIFO)
            Case(
                When(status='in_progress', then=F('last_message_time')),
                default=None,
                output_field=DateTimeField()
            ).desc(nulls_last=True),
            # Для closed — по убыванию (LIFO)
            Case(
                When(status='closed', then=F('last_message_time')),
                default=None,
                output_field=DateTimeField()
            ).desc(nulls_last=True),
        )

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
    lookup_url_kwarg = 'message_id'

    def get_queryset(self):
        ticket_id = self.kwargs['ticket_id']
        user = self.request.user

        if '/admin/' in self.request.path and user.is_staff:
            return Message.objects.filter(ticket_id=ticket_id)

        return Message.objects.filter(ticket_id=ticket_id, is_deleted=False)

    @transaction.atomic
    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        sender_type = self.request.data.get('sender_type', 'user')
        author = self.request.user if sender_type != 'ai' else None

        message = serializer.save(
            ticket_id=ticket_id,
            author=author,
            sender_type=sender_type
        )

        ticket = message.ticket

        if sender_type == 'user':
            ticket.status = 'open'
            ticket.save(update_fields=['status'])

            # Запускаем ИИ в фоне
            executor.submit(run_async_in_thread, self.generate_and_save_ai_reply, message.text, ticket.id)

        elif sender_type == 'staff':
            ticket.status = 'in_progress'
            ticket.save(update_fields=['status'])

    def generate_and_save_ai_reply(self, prompt, ticket_id):
        ai_response = generate_ai_response(prompt)
        ticket = Ticket.objects.get(id=ticket_id)
        Message.objects.create(
            ticket=ticket,
            text=ai_response,
            sender_type='ai'
        )

        ticket.status = 'in_progress'
        ticket.save(update_fields=['status'])

    def perform_update(self, serializer):
        allowed_fields = {'is_deleted'}
        data = self.request.data

        for field in data:
            if field not in allowed_fields:
                raise PermissionDenied(f"Поле '{field}' нельзя редактировать")

        serializer.save()