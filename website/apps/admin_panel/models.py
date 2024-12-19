from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import RichTextField
from apps.support.models import SupportRequest

# class SupportPage(Page):
#     body = RichTextField(blank=True)

#     content_panels = Page.content_panels + [
#         FieldPanel('body', classname="full"),
#     ]

#     def get_context(self, request):
#         context = super().get_context(request)
#         context['support_requests'] = SupportRequest.objects.all()
#         return context