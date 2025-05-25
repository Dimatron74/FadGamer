
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),
    path('games/', include('apps.games.urls')),
    path('news/', include('apps.news.urls')),
    path('support/', include('apps.support.urls')),
    path('admin_panel/', include('apps.admin_panel.urls')),
    path('contact/', include('apps.contact.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
