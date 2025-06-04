# apps/admin_panel/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from .models import PromoCode, Products, BonusType, UserPromoCodeActivation
from .serializers import PromoCodeSerializer, ServiceSerializer, BonusTypeSerializer, NewsSerializer
from apps.news.models import News
from apps.contact.models import ContactRequest
from apps.contact.serializers import ContactRequestSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from apps.news.models import News, NewsBlock
from django.utils.text import slugify
from cyrtranslit import to_latin



def generate_slug(title):
    # Сначала пробуем транслировать кириллицу в латиницу
    try:
        title_translit = to_latin(title, 'ru')
    except:
        title_translit = title

    # Генерируем slug
    slug = slugify(title_translit)
    
    if not slug:
        slug = 'news'

    # Проверяем уникальность
    original_slug = slug
    counter = 1
    while News.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1

    return slug



class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer

    @action(detail=False, methods=['get'])
    def services(self, request):
        """Получить список всех сервисов (игр)"""
        services = Products.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bonus_types(self, request):
        bonus_types = BonusType.objects.all()
        serializer = BonusTypeSerializer(bonus_types, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def activate(self, request):
        code = request.data.get('code')
        user = request.user

        if not code:
            return Response({'error': 'Не указан промокод'}, status=status.HTTP_400_BAD_REQUEST)

        # Ищем промокод
        promo_code = PromoCode.objects.filter(code=code).first()

        # Промокод не найден
        if not promo_code:
            return Response({'error': 'Промокод не найден'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем статус промокода
        if not promo_code.status == 'active':
            return Response({'error': 'Этот промокод нельзя активировать'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что пользователь ещё не активировал этот промокод
        if UserPromoCodeActivation.objects.filter(user=user, promocode=promo_code).exists():
            return Response({'error': 'Вы уже активировали этот промокод'}, status=status.HTTP_400_BAD_REQUEST)

        # Увеличиваем счётчик активаций
        promo_code.activations_promo = promo_code.activations_promo + 1 if promo_code.activations_promo else 1
        promo_code.save()

        # Создаём запись об активации
        UserPromoCodeActivation.objects.create(user=user, promocode=promo_code)

        return Response({
            'success': f'Промокод "{promo_code.code}" успешно активирован!',
            'promocode_id': promo_code.id,
        }, status=status.HTTP_200_OK)
    


@method_decorator(csrf_exempt, name='dispatch')
class NewsCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        title = request.data.get('title', '').strip()
        short_description = request.data.get('short_description', '')
        cover_image = request.FILES.get('cover_image')

        # Генерируем slug из заголовка, если его нет
        slug = generate_slug(title)

        # Создаем новость
        news = News.objects.create(
            title=title,
            short_description=short_description,
            cover_image=cover_image,
            is_published=True,
            slug=slug  # <-- здесь мы явно указываем slug
        )

        # Парсим блоки и связываем с новостью
        blocks = self.parse_blocks(request.data)
        for block_data in blocks:
            block_data['news'] = news
            NewsBlock.objects.create(**block_data)

        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def parse_blocks(self, data):
        """Разбираем блоки из запроса"""
        blocks = []
        i = 0
        while f'blocks[{i}][block_type]' in data:
            block_type = data[f'blocks[{i}][block_type]']
            item = {'block_type': block_type, 'order': int(data[f'blocks[{i}][order]'])}

            if block_type == 'text' or block_type == 'quote':
                item['content'] = data.get(f'blocks[{i}][content]', '')
            elif block_type == 'video':
                item['video_url'] = data.get(f'blocks[{i}][video_url]', '')
            elif block_type == 'image' and f'blocks[{i}][image]' in self.request.FILES:
                item['image'] = self.request.FILES[f'blocks[{i}][image]']

            blocks.append(item)
            i += 1
        return blocks
    
class NewsEditView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, slug=None):
        try:
            news = News.objects.get(slug=slug)
            serializer = NewsSerializer(news, context={'request': request})
            return Response(serializer.data)
        except News.DoesNotExist:
            return Response({'error': 'Новость не найдена'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, slug=None):
        try:
            news = News.objects.get(slug=slug)
        except News.DoesNotExist:
            return Response({'error': 'Новость не найдена'}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем основные поля
        news.title = request.data.get('title', news.title)
        news.short_description = request.data.get('short_description', news.short_description)

        if 'cover_image' in request.FILES:
            news.cover_image = request.FILES['cover_image']

        # Генерируем slug, если его нет
        title_for_slug = request.data.get('title', news.title)
        news.slug = generate_slug(title_for_slug)

        news.save()

        # Обновляем блоки
        blocks_data = self.parse_blocks(request.data)
        news.blocks.all().delete()  # или обновляем существующие

        for block_data in blocks_data:
            NewsBlock.objects.create(news=news, **block_data)

        return Response({'success': True}, status=status.HTTP_200_OK)

    def update_news(self, request, slug=None):
        try:
            news = News.objects.get(slug=slug)
        except News.DoesNotExist:
            return Response({'error': 'Новость не найдена'}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем основные поля
        news.title = request.data.get('title', news.title)
        news.short_description = request.data.get('short_description', news.short_description)

        if 'cover_image' in request.FILES:
            news.cover_image = request.FILES['cover_image']

        news.save()

        # Обновляем блоки
        blocks_data = self.parse_blocks(request.data)
        news.blocks.all().delete()  # или можно обновлять по ID

        for block_data in blocks_data:
            block_data['news'] = news
            NewsBlock.objects.create(**block_data)

        return Response({'success': True}, status=status.HTTP_200_OK)


    def parse_blocks(self, data):
        blocks = []
        i = 0
        while f'blocks[{i}][block_type]' in data:
            block_type = data[f'blocks[{i}][block_type]']
            item = {
                'block_type': block_type,
                'order': int(data.get(f'blocks[{i}][order]', i))
            }

            if block_type == 'text' or block_type == 'quote':
                item['content'] = data.get(f'blocks[{i}][content]', '')

            elif block_type == 'video':
                item['video_url'] = data.get(f'blocks[{i}][video_url]', '')

            elif block_type == 'image':
                # Проверяем, загружено ли новое изображение
                if f'blocks[{i}][image]' in self.request.FILES:
                    item['image'] = self.request.FILES[f'blocks[{i}][image]']
                else:
                    # Используем существующее изображение
                    existing_image_path = data.get(f'blocks[{i}][existing_image]', None)
                    if existing_image_path and '/media/' in existing_image_path:
                        # Убираем http://.../media/
                        existing_image_path = existing_image_path.split('/media/')[-1]

                    item['image'] = existing_image_path

            blocks.append(item)
            i += 1
        return blocks
    
class ContactRequestDetail(RetrieveUpdateAPIView):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer

class ContactRequestList(ListAPIView):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer