from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta de la página principal
    path('about/', views.about, name='about'),  # Página "Acerca de"
    path('contact/', views.contact, name='contact'),  # Página "Contacto"
]