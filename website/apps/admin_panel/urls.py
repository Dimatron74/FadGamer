from django.urls import path
from apps.support.models import SupportRequest
from wagtail.api.v2.views import PagesAPIViewSet, BaseAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from apps.support.views import SupportRequestListView

class SupportRequestViewSet(BaseAPIViewSet):
    model = SupportRequest

# Роутинг для API
api_router = WagtailAPIRouter("wagtailapi")
api_router.register_endpoint("support_requests", SupportRequestViewSet)

urlpatterns = [
    path("cms/api/support_requests/", SupportRequestListView.as_view(), name='support-request-list'),
]