from django.shortcuts import render

def index(request):
    """Render the home page."""
    return render(request, 'web/index.html')

def about(request):
    """Render the About page (nosotros)."""
    return render(request, 'web/about_page.html')

def contact(request):
    """Render the Contact page (contacto)."""
    return render(request, 'web/contact_page.html')

def policies(request):
    """Render the policies page."""
    return render(request, 'web/policies.html')

def portfolio(request):
    return render(request, 'web/portfolio_page.html')

# The project/portfolio section is currently unused. Enable it once a template is available.
# def projects(request):
#     return render(request, 'web/projects.html')

from django.http import HttpResponse

def robots_txt(request):
    content = [
        "User-Agent: *",
        "Allow: /",
        "Sitemap: https://pidevelopment.web.app/sitemap.xml"
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")
