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
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import User, UserEmail, Email, UserProducts
from .serializers import ProductUserSerializer
import io
from PIL import Image
from ..main.email_service import send_company_email
from django.utils import timezone
import random 


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
            'is_staff': user.is_staff,
            'birth_date': user.birth_date.isoformat() if user.birth_date else None,
            'phone_number': str(user.phone_number) if user.phone_number else None,
            'notification_type': user.notification_type,
            'avatar': request.build_absolute_uri(user.avatar.url) if user.avatar else None,
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

    # Обновление типа уведомлений
    if 'notification_type' in data:
        notification_type = data['notification_type']

        valid_choices = dict(User.NOTIFICATION_CHOICES).keys()
        if notification_type not in valid_choices:
            return Response({
                'error': 'Некорректный тип уведомления'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.notification_type = notification_type

    # Обновление телефона
    if 'phone_number' in data:
        raw_phone = data['phone_number']

        try:
            # Просто присваиваем строковое значение
            user.phone_number = raw_phone  # PhoneNumberField сам валидирует и нормализует
        except Exception as e:
            return Response({'error': 'Неверный формат телефона'}, status=status.HTTP_400_BAD_REQUEST)

    # Смена пароля
    if 'old_password' in data and 'new_password' in data:
        old_password = data['old_password']
        new_password = data['new_password']
        if not user.check_password(old_password):
            return Response({'error': 'Неверный текущий пароль'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)

    # Обновление email
    if 'email' in data:
        new_email_str = data['email'].strip()

        if not new_email_str:
            return Response({'error': 'Email обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        # Валидация формата email (простая)
        if '@' not in new_email_str or '.' not in new_email_str:
            return Response({'error': 'Некорректный email'}, status=status.HTTP_400_BAD_REQUEST)

        current_email = user.get_active_email()
        if new_email_str == current_email:
            return Response({'error': 'Этот email уже используется'}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем или получаем Email объект
        email_obj, _ = Email.objects.get_or_create(email=new_email_str)

        # Проверяем, используется ли этот email другим пользователем активно
        if UserEmail.objects.filter(email=email_obj, is_active=True).exclude(user=user).exists():
            return Response({'error': 'Этот email уже используется другим аккаунтом'}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем новый UserEmail (не активный)
        user_email, created = UserEmail.objects.get_or_create(user=user, email=email_obj, defaults={
            'is_active': False,
            'is_confirmed': False
        })

        if not created and user_email.is_confirmed:
            return Response({'error': 'Этот email уже подтвержден'}, status=status.HTTP_400_BAD_REQUEST)

        # Генерируем и отправляем код (используем метод из модели)
        user_email.generate_confirmation_code()
        context = {'code': user_email.confirmation_code}
        send_company_email(new_email_str, 'email_confirmation', context)

        # Не сохраняем user здесь, так как изменения в user_email
        return Response({'message': 'Код подтверждения отправлен на email'}, status=status.HTTP_200_OK)

    user.save()
    return Response({'message': 'Профиль успешно обновлен'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def upload_avatar(request):
    user = request.user
    avatar = request.FILES.get('avatar')

    if not avatar:
        return Response({'error': 'Файл не загружен'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверяем, что это изображение
    try:
        original_image = Image.open(avatar).convert("RGBA")
    except Exception:
        return Response({'error': 'Загруженный файл не является изображением'}, status=status.HTTP_400_BAD_REQUEST)

    # Масштабируем до максимального размера 512x512
    max_size = (512, 512)
    original_image.thumbnail(max_size, Image.LANCZOS)

    # Создаём буфер в памяти для сжатого изображения
    img_io = io.BytesIO()

    # Сохраняем как WebP с компрессией
    original_image.save(img_io, format='WEBP', quality=80, optimize=True, method=6)

    # Закрываем исходное изображение, чтобы освободить ресурсы
    original_image.close()

    # Формируем новое имя файла
    file_name = f'avatars/{user.uid}.webp'

    # Создаём InMemoryUploadedFile из буфера
    compressed_image = InMemoryUploadedFile(
        img_io,
        None,
        f'{user.uid}.webp',
        'image/webp',
        img_io.tell(),
        None
    )

    # Сохраняем в storage
    path = default_storage.save(file_name, compressed_image)

    # Обновляем аватар пользователя
    user.avatar = path
    user.save()

    return Response({
        'message': 'Аватар успешно загружен',
        'avatar_url': request.build_absolute_uri(user.avatar.url)
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_products(request):
    user = request.user
    products = UserProducts.objects.filter(user=user).select_related('product', 'distribution_model')
    serializer = ProductUserSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def confirm_email(request):
    user = request.user
    data = request.data
    code = data.get('code')
    email_str = data.get('email')  # Frontend отправит email, для которого код

    if not code or not email_str:
        return Response({'error': 'Код и email обязательны'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        email_obj = Email.objects.get(email=email_str)
        user_email = UserEmail.objects.get(user=user, email=email_obj)
    except (Email.DoesNotExist, UserEmail.DoesNotExist):
        return Response({'error': 'Email не найден'}, status=status.HTTP_404_NOT_FOUND)

    if user_email.verify_code(code):
        return Response({'message': 'Email подтвержден'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Неверный или просроченный код'}, status=status.HTTP_400_BAD_REQUEST)