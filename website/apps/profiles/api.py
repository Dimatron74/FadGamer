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
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import User, UserEmail, Email


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    try:
        user = request.user

        if not user.is_authenticated:
            return Response({'error': 'Пользователь не аутентифицирован'}, status=401)

        # Проверяем, есть ли у пользователя активный email
        active_email_entry = user.useremail_set.filter(is_active=True).first()
        if not active_email_entry:
            return Response({
                'error': 'У пользователя нет активного email',
                'code': 'no_active_email'
            }, status=403)

        # Возвращаем данные
        return Response({
            'uid': user.uid,
            'email': active_email_entry.email.email,
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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_profile(request):
    user = request.user
    data = request.data

    # Обновление никнейма
    if 'nickname' in data:
        nickname = data['nickname'].strip()
        if User.objects.filter(nickname=nickname).exclude(uid=user.uid).exists():
            return Response({'error': 'Этот никнейм уже занят'}, status=status.HTTP_400_BAD_REQUEST)
        user.nickname = nickname

    # Обновление даты рождения
    if 'birth_date' in data:
        user.birth_date = data['birth_date']

    # Обновление телефона
    if 'phone_number' in data:
        user.phone_number = data['phone_number']

    # Смена пароля
    if 'old_password' in data and 'new_password' in data:
        old_password = data['old_password']
        new_password = data['new_password']
        if not user.check_password(old_password):
            return Response({'error': 'Неверный текущий пароль'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)

    # Обновление email
    if 'email' in data:
        new_email = data['email'].strip()

        current_email = user.get_active_email()

        if new_email != current_email:

            # Проверяем, используется ли этот email другим пользователем (активно)
            existing_email = Email.objects.filter(email=new_email).first()
            if existing_email:
                if UserEmail.objects.filter(
                    email=existing_email,
                    is_active=True
                ).exclude(user=user).exists():
                    return Response({
                        'error': 'Этот email уже используется другим аккаунтом'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Получаем или создаём объект Email
            email_obj, created = Email.objects.get_or_create(email=new_email)

            # Деактивируем текущий email пользователя
            if current_email:
                try:
                    current_email_entry = user.useremail_set.get(email__email=current_email, is_active=True)
                    current_email_entry.is_active = False
                    current_email_entry.save()
                except UserEmail.DoesNotExist:
                    pass 

            # Проверяем, есть ли уже такая связь (пользователь + email)
            existing_user_email = UserEmail.objects.filter(user=user, email=email_obj).first()

            if existing_user_email:
                # Обновляем существующую запись вместо создания новой
                existing_user_email.is_active = True
                existing_user_email.is_confirmed = False  # можно оставить без подтверждения или отправить ссылку
                existing_user_email.save()
            else:
                # Создаём новую связь только если такой ещё нет
                UserEmail.objects.create(
                    user=user,
                    email=email_obj,
                    is_active=True,
                    is_confirmed=False  # можно отправить ссылку подтверждения
                )

    user.save()
    return Response({'message': 'Профиль успешно обновлен'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    user = request.user
    avatar = request.FILES.get('avatar')

    if not avatar:
        return Response({'error': 'Файл не загружен'}, status=status.HTTP_400_BAD_REQUEST)

    # Сохраняем файл
    file_name = f'avatars/{user.uid}_{avatar.name}'
    path = default_storage.save(file_name, ContentFile(avatar.read()))
    user.avatar = path
    user.save()

    return Response({'message': 'Аватар успешно загружен', 'avatar_url': user.avatar.url})