# contact/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ContactRequestSerializer

class SubmitContactRequest(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()

        # Если пользователь авторизован — добавляем его как user
        if request.user.is_authenticated:
            data['user'] = request.user.uid
            data['name'] = request.user.nickname  # Сохраняем имя из профиля

        serializer = ContactRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)