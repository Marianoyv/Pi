from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

from .models import Servicio

def home(request):
    servicios = Servicio.objects.all()
    return render(request, 'index.html', {'servicios': servicios})
