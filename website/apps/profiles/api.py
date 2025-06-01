# profiles/api.py

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .forms import SignupForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.middleware.csrf import get_token


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def me(request):
    authentication = JWTAuthentication()
    try:
        user_auth_tuple = authentication.authenticate(request)

        if user_auth_tuple is None:
            return Response({'error': 'Токен отсутствует или недействителен'}, status=401)

        user, auth = user_auth_tuple

        if not user.is_authenticated:
            return Response({'error': 'Пользователь не аутентифицирован'}, status=401)

        user_email = user.useremail_set.filter(is_active=True).first()
        email = user_email.email.email if user_email else None

        return Response({
            'uid': user.uid,
            'email': email,
            'name': user.nickname,
            'is_staff': user.is_staff
        })

    except AuthenticationFailed as e:
        return Response({'error': str(e)}, status=401)

    except Exception as e:
        print("Unexpected error:", e)
        return Response({'error': 'Ошибка сервера при обработке запроса'}, status=500)

@api_view(['POST', 'OPTIONS'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    print(data)
    message = 'success'

    form = SignupForm({
        'nickname': data.get('name'),
        'email': data.get('email'),
        'password1': data.get('password'),
        'password2': data.get('password_confirm'),
    })

    if form.is_valid():
        form.save()
    else:
        print("Ошибка формы:", form.errors)
        message = 'error form'

    return JsonResponse({'message': message})

def get_csrf_token(request):
    print(request)
    return JsonResponse({'csrf_token': get_token(request)})