# profiles/views.py

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
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = MyTokenObtainPairSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=False):
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    