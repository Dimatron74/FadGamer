from django.contrib import admin
from .models import BonusType, PromoCode, PromoCodeBonus, UserPromoCodeActivation

admin.site.register(BonusType)
admin.site.register(PromoCode)
admin.site.register(PromoCodeBonus)
admin.site.register(UserPromoCodeActivation)