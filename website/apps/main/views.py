from django.shortcuts import render
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("главная страница")

from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')