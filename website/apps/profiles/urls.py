# profiles/urls.py

from django.urls import path
from . import views, api, serializers
from rest_framework_simplejwt.views import TokenRefreshView




urlpatterns = [
    path("signup/", api.signup, name="signup"),
    path("me/", api.me, name="me"),
    path("profile/", api.update_profile, name="update_profile"),
    path("avatar/upload/", api.upload_avatar, name="upload_avatar"),
    path('products/', api.get_user_products, name='user-products'),

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/csrf-token/', api.get_csrf_token, name='csrf-token'),
]