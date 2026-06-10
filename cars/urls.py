from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='cars/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.accueil, name='accueil'),                # Page d'accueil à la racine
    path('mon-espace-prive/', views.accueil, name='accueil_alt'),  # Alias si vous voulez garder cette URL
    path('catalogue/', views.catalogue, name='catalogue'),
    path('location/', views.location, name='location'),
    path('vente/', views.vente, name='vente'),
    path('voiture/<int:car_id>/', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('dashboard/voiture/ajouter/', views.admin_car_create, name='admin_car_create'),
    path('dashboard/voiture/<int:car_id>/modifier/', views.admin_car_update, name='admin_car_update'),
    path('dashboard/voiture/<int:car_id>/supprimer/', views.admin_car_delete, name='admin_car_delete'),
    path('dashboard/messages/', views.admin_messages, name='admin_messages'),
    
    # Gestion des médias
    path('dashboard/medias/', views.admin_media_list, name='admin_media_list'),
    path('dashboard/medias/ajouter/', views.admin_media_create, name='admin_media_create'),
    path('dashboard/medias/<int:media_id>/supprimer/', views.admin_media_delete, name='admin_media_delete'),
    
    # Gestion des utilisateurs
    path('dashboard/utilisateurs/', views.admin_user_list, name='admin_user_list'),
    path('dashboard/utilisateurs/ajouter/', views.admin_user_create, name='admin_user_create'),
    path('dashboard/utilisateurs/<int:user_id>/modifier/', views.admin_user_update, name='admin_user_update'),
    path('dashboard/utilisateurs/<int:user_id>/supprimer/', views.admin_user_delete, name='admin_user_delete'),
]