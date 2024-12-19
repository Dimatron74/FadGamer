from django.shortcuts import render
from django.http import HttpResponse
from .models import SupportRequest
from .serializers import SupportRequestSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def support_request(request):
    print('СЮДА', request.data, 'user:', request.user)
    if request.method == 'POST':
        question = request.data.get('question')
        text = request.data.get('text')
        support_request = SupportRequest(question=question, text=text, user=request.user)
        support_request.save()
        return HttpResponse('Запрос отправлен успешно!')
    return HttpResponse('Ошибка отправки запроса!')



class SupportRequestListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SupportRequest.objects.all()
    serializer_class = SupportRequestSerializer

    def get_queryset(self):
        """
        Возвращает вопросы пользователя, если параметр user передан.
        """
        queryset = SupportRequest.objects.all()

        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        
        return queryset