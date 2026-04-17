from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),                # Page d'accueil à la racine
    path('mon-espace-prive/', views.accueil, name='accueil_alt'),  # Alias si vous voulez garder cette URL
    path('catalogue/', views.catalogue, name='catalogue'),
    path('location/', views.location, name='location'),
    path('vente/', views.vente, name='vente'),
    path('voiture/<int:car_id>/', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
]