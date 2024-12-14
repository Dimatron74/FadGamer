from django.urls import path
from . import views, api, serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView




urlpatterns = [
    path("signup/", api.signup, name="signup"),
    path("me/", api.me, name="me"),

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/csrf-token/', api.get_csrf_token, name='csrf-token'),
]