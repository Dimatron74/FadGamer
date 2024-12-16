from django.shortcuts import render
from django.http import HttpResponse
from .serializers import MyTokenObtainPairSerializer
from . import permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserEmail
from rest_framework_simplejwt.authentication import JWTAuthentication

class MyTokenObtainPairView(APIView):
    permission_classes = []
    authentication_classes = [JWTAuthentication]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Обработка валидных данных
            email = serializer.validated_data['email']
            user_email = UserEmail.objects.get(email__email=email)
            user = user_email.user
            token = MyTokenObtainPairSerializer.get_token(user)
            # return Response({'refresh': str(token), 'access': str(token.access_token)}, status=status.HTTP_200_OK)
            return Response(token, status=status.HTTP_200_OK)
        else:
            # Обработка невалидных данных
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


from django.utils.translation import gettext as _

def my_view(request):
    message = _("Hello, world!")
    message2 = _("You are next")
    message3 = _("Hello, world!")
    print(message)
    return HttpResponse(message)

    