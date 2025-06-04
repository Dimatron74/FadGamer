from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.main.email_service import send_company_email

class SendCompanyEmail(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        recipient = request.data.get("recipient")
        template_name = request.data.get("template_name")
        context = request.data.get("context", {})

        success = send_company_email(recipient, template_name, context)
        return Response({"success": success})