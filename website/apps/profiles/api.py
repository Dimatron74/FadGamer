from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .forms import SignupForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def me(request):
    authentication = JWTAuthentication()
    user, auth = authentication.authenticate(request)
    if user:
        user_email = user.useremail_set.filter(is_active=True).first()
        if user_email:
            email = user_email.email.email
        else:
            email = None
        return Response({
            'id': user.id,
            'email': email,
            'name': user.nickname,
            })
    else:
        return Response({'error': 'Токен авторизации не найден'})

@api_view(['POST'])
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
        message = 'error'

    return JsonResponse({'message': message})