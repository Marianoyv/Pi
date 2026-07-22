"""pi_development URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from pi_development.health import health_check


urlpatterns = [
    path("health", health_check, name="health"),
    path("healthz/", health_check, name="healthz"),
    path('', include('pi_development.web.urls')),
]

if settings.ENABLE_ADMIN:
    urlpatterns.insert(0, path('admin/', admin.site.urls))
