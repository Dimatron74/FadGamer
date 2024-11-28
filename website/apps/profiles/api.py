from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .forms import SignupForm


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'username': data['username'],
        'email': data['email'],
        'password1': data['password'],
        'password2': data['password']
    })

    if form.is_valid():
        form.save()
    else:
        message = 'error'

    return JsonResponse({'message': message})