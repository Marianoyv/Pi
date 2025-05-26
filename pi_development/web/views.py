from django.shortcuts import render

def index(request):
    return render(request, 'pi_development/web/index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def policies(request):
    return render(request, 'policies.html')

def projects(request):
    return render(request, 'projects.html')



from django.shortcuts import render

def index(request):
    # Asegúrate de usar 'web/index.html' si tu archivo está en 'web/templates/web/index.html'
    return render(request, 'web/index.html')