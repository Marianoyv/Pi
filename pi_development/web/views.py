from django.shortcuts import render

from .models import Servicio

def home(request):
    servicios = Servicio.objects.all()
    return render(request, 'index.html', {'servicios': servicios})
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def policies(request):
    return render(request, 'policies.html')
def projects(request):
    return render(request, 'projects.html')
