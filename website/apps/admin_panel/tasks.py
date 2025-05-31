# apps/admin_panel/tasks.py
from django.utils import timezone
from .models import PromoCode

def update_promocode_statuses():
    """
    Автоматически обновляет статусы промокодов:
    - inactive -> active (если прошло created_at)
    - active -> expired (если прошло expires_at)
    """
    now = timezone.now()

    # Из inactive -> active
    PromoCode.objects.filter(
        status='inactive',
        created_at__lte=now
    ).update(status='active')

    # Из active -> expired
    PromoCode.objects.filter(
        status='active',
        expires_at__isnull=False,
        expires_at__lte=now
    ).update(status='expired')