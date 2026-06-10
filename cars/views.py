"""Vues (Views) du module Cars - Gestion de l'affichage des voitures

Ce module contient toutes les vues (contrôleurs) pour l'affichage des voitures.
Les vues récupèrent les données de la base de données et les affichent dans les templates.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Car, Media, ContactMessage, TestDriveRequest
from .forms import CarForm, ContactForm, TestDriveForm, MediaForm, UserRegistrationForm, UserUpdateForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required


def accueil(request):
    """Vue pour la page d'accueil"""
    voitures = Car.objects.all()[:3]
    return render(request, 'cars/accueil.html', {'voitures': voitures})

def filtrer_et_paginer_voitures(request, queryset):
    """Fonction utilitaire pour filtrer et paginer les voitures"""
    # Filtres
    marque = request.GET.get('marque')
    modele = request.GET.get('modele')
    annee_min = request.GET.get('annee_min')
    prix_max = request.GET.get('prix_max')
    
    if marque:
        queryset = queryset.filter(marque__icontains=marque)
    if modele:
        queryset = queryset.filter(modele__icontains=modele)
    if annee_min:
        queryset = queryset.filter(annee__gte=annee_min)
    if prix_max:
        # Check against both location and vente price depending on type_offre
        # OR simply check if either is less than max
        queryset = queryset.filter(models.Q(prix_vente__lte=prix_max) | models.Q(prix_location__lte=prix_max))

    # Pagination (9 items per page)
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return page_obj

from django.db import models

def catalogue(request):
    """Vue affichant le catalogue complet de toutes les voitures"""
    voitures = Car.objects.all()
    page_obj = filtrer_et_paginer_voitures(request, voitures)
    
    context = {
        'page_obj': page_obj,
        'titre': 'Catalogue complet',
    }
    return render(request, 'cars/catalogue.html', context)

def location(request):
    """Vue affichant uniquement les voitures disponibles à la location"""
    voitures = Car.objects.filter(type_offre='location')
    page_obj = filtrer_et_paginer_voitures(request, voitures)
    
    context = {
        'page_obj': page_obj,
        'titre': 'Voitures à louer',
    }
    return render(request, 'cars/location.html', context)

def vente(request):
    """Vue affichant uniquement les voitures disponibles à la vente"""
    voitures = Car.objects.filter(type_offre='vente')
    page_obj = filtrer_et_paginer_voitures(request, voitures)
    
    context = {
        'page_obj': page_obj,
        'titre': 'Voitures à vendre',
    }
    return render(request, 'cars/vente.html', context)

def detail(request, car_id):
    """Vue affichant le détail complet d'une voiture spécifique"""
    voiture = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = TestDriveForm(request.POST)
        if form.is_valid():
            test_drive = form.save(commit=False)
            test_drive.voiture = voiture
            test_drive.save()
            
            # Email Admin
            send_mail(
                subject=f"Nouvelle demande d'essai : {voiture.marque} {voiture.modele}",
                message=f"Nouvelle demande d'essai reçue de {test_drive.nom}.\nEmail : {test_drive.email}\nTéléphone : {test_drive.telephone}\nDate souhaitée : {test_drive.date_souhaitee}\nVéhicule : {voiture.marque} {voiture.modele}",
                from_email='noreply@parkingmediator.com',
                recipient_list=['admin@parkingmediator.com'],
                fail_silently=True,
            )
            # Email Client
            send_mail(
                subject="Confirmation de votre demande d'essai - Parking Mediator",
                message=f"Bonjour {test_drive.nom},\n\nNous avons bien reçu votre demande d'essai pour le véhicule {voiture.marque} {voiture.modele}.\nNotre équipe vous contactera très prochainement pour confirmer ce rendez-vous.\n\nÀ très vite,\nL'équipe Parking Mediator",
                from_email='noreply@parkingmediator.com',
                recipient_list=[test_drive.email],
                fail_silently=True,
            )
            
            messages.success(request, "Votre demande d'essai a bien été envoyée. Nous vous recontacterons très vite !")
            return redirect('detail', car_id=voiture.id)
    else:
        form = TestDriveForm()
        
    # Véhicules similaires (même marque ou type d'offre, max 3)
    vehicules_similaires = Car.objects.filter(
        models.Q(marque=voiture.marque) | models.Q(type_offre=voiture.type_offre)
    ).exclude(id=voiture.id).order_by('?')[:3]
    
    context = {
        'voiture': voiture,
        'form': form,
        'vehicules_similaires': vehicules_similaires,
    }
    return render(request, 'cars/detail.html', context)

def contact(request):
    """Vue affichant la page de contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            
            # Email Admin
            send_mail(
                subject=f"Nouveau message de contact : {contact_msg.sujet}",
                message=f"Message de : {contact_msg.nom}\nEmail : {contact_msg.email}\nTéléphone : {contact_msg.telephone}\n\nMessage :\n{contact_msg.message}",
                from_email='noreply@parkingmediator.com',
                recipient_list=['admin@parkingmediator.com'],
                fail_silently=True,
            )
            # Email Client
            send_mail(
                subject="Nous avons bien reçu votre message - Parking Mediator",
                message=f"Bonjour {contact_msg.nom},\n\nMerci de nous avoir contactés. Nous avons bien reçu votre message concernant \"{contact_msg.sujet}\".\nNotre équipe y répondra dans les plus brefs délais.\n\nCordialement,\nL'équipe Parking Mediator",
                from_email='noreply@parkingmediator.com',
                recipient_list=[contact_msg.email],
                fail_silently=True,
            )
            
            messages.success(request, "Votre message a été envoyé avec succès. Notre équipe vous répondra dans les plus brefs délais.")
            return redirect('contact')
    else:
        form = ContactForm()
        
    return render(request, 'cars/contact.html', {'form': form})

def a_propos(request):
    """Vue pour la page À propos"""
    return render(request, 'cars/a_propos.html', {'titre': 'À propos de nous'})

def mentions_legales(request):
    """Vue pour les mentions légales"""
    return render(request, 'cars/mentions_legales.html', {'titre': 'Mentions Légales'})


@staff_member_required
def admin_dashboard(request):
    """Vue du tableau de bord administrateur"""
    voitures = Car.objects.all().order_by('-date_ajout')
    total_voitures = voitures.count()
    total_locations = voitures.filter(type_offre='location').count()
    total_ventes = voitures.filter(type_offre='vente').count()
    messages_non_lus = ContactMessage.objects.filter(lu=False).count()
    demandes_essai = TestDriveRequest.objects.filter(statut_demande='en_attente').count()
    
    # Données pour les graphiques
    status_counts = {
        'disponible': voitures.filter(statut='disponible').count(),
        'reserve': voitures.filter(statut='reserve').count(),
        'vendu': voitures.filter(statut='vendu').count(),
    }
    
    context = {
        'voitures': voitures[:10],  # Les 10 dernières voitures
        'total_voitures': total_voitures,
        'total_locations': total_locations,
        'total_ventes': total_ventes,
        'messages_non_lus': messages_non_lus,
        'demandes_essai': demandes_essai,
        'status_counts': status_counts,
    }
    return render(request, 'cars/admin/dashboard.html', context)

@staff_member_required
def admin_car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            voiture = form.save()
            image = form.cleaned_data.get('image_principale')
            if image:
                Media.objects.create(car=voiture, file=image, media_type='image')
            messages.success(request, 'Véhicule ajouté avec succès.')
            return redirect('dashboard')
    else:
        form = CarForm()
    
    return render(request, 'cars/admin/car_form.html', {'form': form, 'titre': 'Ajouter un véhicule'})

@staff_member_required
def admin_car_update(request, car_id):
    voiture = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=voiture)
        if form.is_valid():
            voiture = form.save()
            image = form.cleaned_data.get('image_principale')
            if image:
                Media.objects.create(car=voiture, file=image, media_type='image')
            messages.success(request, 'Véhicule modifié avec succès.')
            return redirect('dashboard')
    else:
        form = CarForm(instance=voiture)
    
    return render(request, 'cars/admin/car_form.html', {'form': form, 'titre': 'Modifier le véhicule', 'voiture': voiture})

@staff_member_required
def admin_car_delete(request, car_id):
    voiture = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        voiture.delete()
        messages.success(request, 'Véhicule supprimé avec succès.')
        return redirect('dashboard')
    
    return render(request, 'cars/admin/car_confirm_delete.html', {'voiture': voiture})

@staff_member_required
def admin_messages(request):
    """Vue pour lister les messages de contact et demandes d'essai"""
    contacts = ContactMessage.objects.all()
    test_drives = TestDriveRequest.objects.all()
    
    # Marquer comme lu si demandé (via GET par exemple ?lu_id=X)
    lu_id = request.GET.get('lu_id')
    if lu_id:
        msg = get_object_or_404(ContactMessage, id=lu_id)
        msg.lu = True
        msg.save()
        messages.success(request, "Message marqué comme lu.")
        return render(request, 'cars/admin/messages.html', {
        'contacts': contacts,
        'test_drives': test_drives
    })

# --- GESTION DES MÉDIAS (Admin) ---

@staff_member_required
def admin_media_list(request):
    """Lister tous les médias regroupés par voiture"""
    medias = Media.objects.select_related('car').all().order_by('-id')
    return render(request, 'cars/admin/media_list.html', {'medias': medias})

@staff_member_required
def admin_media_create(request):
    """Uploader plusieurs médias pour une voiture"""
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid():
            car = form.cleaned_data['car']
            media_type = form.cleaned_data['media_type']
            for f in files:
                Media.objects.create(car=car, media_type=media_type, file=f)
            messages.success(request, f"{len(files)} média(s) ajouté(s) avec succès.")
            return redirect('admin_media_list')
    else:
        # Si une voiture est passée en paramètre
        car_id = request.GET.get('car_id')
        initial = {}
        if car_id:
            initial['car'] = car_id
        form = MediaForm(initial=initial)
    return render(request, 'cars/admin/media_form.html', {'form': form, 'titre': 'Ajouter des médias'})

@staff_member_required
def admin_media_delete(request, media_id):
    """Supprimer un média"""
    media = get_object_or_404(Media, id=media_id)
    if request.method == 'POST':
        media.delete()
        messages.success(request, "Le média a été supprimé.")
        return redirect('admin_media_list')
    return render(request, 'cars/admin/confirm_delete.html', {'objet': f"le média de {media.car.marque}", 'cancel_url': 'admin_media_list'})

# --- GESTION DES UTILISATEURS (Admin) ---

@staff_member_required
def admin_user_list(request):
    """Lister tous les administrateurs"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'cars/admin/user_list.html', {'users': users})

@staff_member_required
def admin_user_create(request):
    """Créer un nouvel utilisateur (administrateur)"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Par défaut, on crée des administrateurs pour le dashboard
            user.save()
            messages.success(request, f"L'utilisateur {user.username} a été créé avec succès.")
            return redirect('admin_user_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'cars/admin/user_form.html', {'form': form, 'titre': 'Ajouter un utilisateur'})

@staff_member_required
def admin_user_update(request, user_id):
    """Modifier un utilisateur existant"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'utilisateur {user.username} a été mis à jour.")
            return redirect('admin_user_list')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'cars/admin/user_form.html', {'form': form, 'titre': f'Modifier {user.username}'})

@staff_member_required
def admin_user_delete(request, user_id):
    """Supprimer un utilisateur"""
    user = get_object_or_404(User, id=user_id)
    # Empêcher l'utilisateur de se supprimer lui-même
    if request.user.id == user.id:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect('admin_user_list')
        
    if request.method == 'POST':
        user.delete()
        messages.success(request, f"L'utilisateur {user.username} a été supprimé.")
        return redirect('admin_user_list')
    return render(request, 'cars/admin/confirm_delete.html', {'objet': f"l'utilisateur {user.username}", 'cancel_url': 'admin_user_list'})
