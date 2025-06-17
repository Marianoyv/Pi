from django.shortcuts import render

def index(request):
    """Render the home page."""
    return render(request, 'web/index.html')

def about(request):
    """Render the About page."""
    return render(request, 'web/about.html')

def contact(request):
    """Render the Contact page."""
    return render(request, 'web/contact.html')

def policies(request):
    """Render the policies page."""
    return render(request, 'web/policies.html')

def portfolio(request):
    return render(request, 'web/portfolio.html')


# The project/portfolio section is currently unused. Enable it once a template is available.
# def projects(request):
#     return render(request, 'web/projects.html')
