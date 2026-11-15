from django.urls import include, path


urlpatterns = [path("", include("pi_development.web.urls"))]
