"""Vues (Views) du module Cars - Gestion de l'affichage des voitures

Ce module contient toutes les vues (contrôleurs) pour l'affichage des voitures.
Les vues récupèrent les données de la base de données et les affichent dans les templates.
"""

from django.shortcuts import render, get_object_or_404
from .models import Car


def accueil(request):
    """Vue pour la page d'accueil
    
    Affiche la page d'accueil du site Parking Mediator.
    
    Args:
        request: L'objet requête HTTP
        
    Returns:
        HttpResponse: La page d'accueil avec le template accueil.html
    """
    return render(request, 'cars/accueil.html')

def catalogue(request):
    """Vue affichant le catalogue complet de toutes les voitures
    
    Récupère toutes les voitures de la base de données et les affiche
    dans un catalogue sous forme de grille.
    
    Args:
        request: L'objet requête HTTP
        
    Returns:
        HttpResponse: La page catalogue avec toutes les voitures
    
    Context:
        voitures: QuerySet contenant toutes les voitures
        titre: Le titre de la page
    """
    # Récupère toutes les voitures de la base de données
    voitures = Car.objects.all()
    
    # Prépare les données à envoyer au template
    context = {
        'voitures': voitures,  # Liste de toutes les voitures
        'titre': 'Catalogue complet',  # Titre affiché sur la page
    }
    
    # Affiche le template avec les données
    return render(request, 'cars/catalogue.html', context)

def location(request):
    """Vue affichant uniquement les voitures disponibles à la location
    
    Filtre les voitures pour afficher seulement celles avec type_offre='location'.
    
    Args:
        request: L'objet requête HTTP
        
    Returns:
        HttpResponse: La page des voitures à louer
        
    Context:
        voitures: QuerySet contenant les voitures à louer
        titre: Le titre de la page
    """
    # Filtre les voitures pour obtenir seulement celles à la location
    voitures = Car.objects.filter(type_offre='location')
    
    # Prépare les données à envoyer au template
    context = {
        'voitures': voitures,  # Liste des voitures à louer
        'titre': 'Voitures à louer',  # Titre affiché sur la page
    }
    
    # Affiche le template avec les données
    return render(request, 'cars/location.html', context)

def vente(request):
    """Vue affichant uniquement les voitures disponibles à la vente
    
    Filtre les voitures pour afficher seulement celles avec type_offre='vente'.
    
    Args:
        request: L'objet requête HTTP
        
    Returns:
        HttpResponse: La page des voitures à vendre
        
    Context:
        voitures: QuerySet contenant les voitures à vendre
        titre: Le titre de la page
    """
    # Filtre les voitures pour obtenir seulement celles à la vente
    voitures = Car.objects.filter(type_offre='vente')
    
    # Prépare les données à envoyer au template
    context = {
        'voitures': voitures,  # Liste des voitures à vendre
        'titre': 'Voitures à vendre',  # Titre affiché sur la page
    }
    
    # Affiche le template avec les données
    return render(request, 'cars/vente.html', context)

def detail(request, car_id):
    """Vue affichant le détail complet d'une voiture spécifique
    
    Récupère les informations détaillées d'une voiture par son ID.
    Retourne une erreur 404 si la voiture n'existe pas.
    
    Args:
        request: L'objet requête HTTP
        car_id: L'ID de la voiture à afficher (integer)
        
    Returns:
        HttpResponse: La page de détail de la voiture
        
    Raises:
        Http404: Si la voiture avec cet ID n'existe pas
        
    Context:
        voiture: L'objet Car contenant les détails de la voiture
    """
    # Récupère la voiture par son ID, ou retourne une erreur 404 si elle n'existe pas
    voiture = get_object_or_404(Car, id=car_id)
    
    # Prépare les données à envoyer au template
    context = {
        'voiture': voiture,  # Les détails complètes de la voiture
    }
    
    # Affiche le template avec les données
    return render(request, 'cars/detail.html', context)

def contact(request):
    """Vue affichant la page de contact
    
    Affiche le formulaire de contact pour les utilisateurs.
    
    Args:
        request: L'objet requête HTTP
        
    Returns:
        HttpResponse: La page de contact
    """
    # Affiche simplement la page de contact sans données spéciales
    return render(request, 'cars/contact.html')

