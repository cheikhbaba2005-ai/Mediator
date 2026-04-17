"""Configuration du panneau d'administration Django pour les voitures et médias

Ce module configure comment les modèles Car et Media sont affichés et gérés
dans le panneau d'administration Django.
"""

from django.contrib import admin
from .models import Car, Media
from django.utils.html import format_html


class MediaInline(admin.TabularInline):
    """Affiche les médias associés à une voiture dans la même page d'édition
    
    Cette classe permet d'ajouter, modifier et supprimer des médias directement
    depuis la page d'édition d'une voiture.
    """
    model = Media
    extra = 1  # Ajoute 1 ligne vide pour ajouter un nouveau média
    fields = ['file', 'media_type', 'uploaded_at']
    readonly_fields = ['uploaded_at']  # Empêche la modification de la date


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Configuration de l'affichage des voitures dans l'admin Django
    
    Personnalise la liste, les filtres, la recherche et les détails des voitures.
    """
    
    # Colonnes affichées dans la liste
    list_display = ('marque', 'modele', 'annee', 'type_offre', 'prix_affiche', 'disponibilite', 'nb_medias')
    
    # Filtres disponibles à gauche
    list_filter = ('type_offre', 'disponibilite', 'marque', 'annee')
    
    # Champs dans lesquels on peut chercher
    search_fields = ('marque', 'modele', 'description')
    
    # Affiche les médias dans la même page
    inlines = [MediaInline]
    
    # Organisation des champs dans le formulaire
    fieldsets = (
        ('Informations générales', {
            'fields': ('marque', 'modele', 'annee', 'type_offre', 'disponibilite')
        }),
        ('Prix', {
            'fields': ('prix_location', 'prix_vente'),
            'description': 'Remplissez le prix correspondant au type d\'offre. Laissez vide l\'autre.'
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )
    
    # Permet d'éditer la disponibilité directement dans la liste
    list_editable = ['disponibilite']
    
    # Nombre de voitures affichées par page
    list_per_page = 25

    def nb_medias(self, obj):
        """Affiche le nombre de médias avec un badge
        
        Args:
            obj: L'objet Car
            
        Returns:
            HTML formé avec le nombre de médias
        """
        # Compte le nombre de médias associés
        count = obj.medias.count()
        # Affiche un badge avec le nombre
        return format_html('<span class="badge badge-secondary">{}</span>', count)
    
    nb_medias.short_description = 'Médias'

    def get_queryset(self, request):
        """Optimise la requête pour charger les médias en une seule requête
        
        Args:
            request: L'objet requête HTTP
            
        Returns:
            QuerySet optimisé avec les médias pré-chargés
        """
        # Optimisation avec prefetch_related pour éviter les requêtes N+1
        return super().get_queryset(request).prefetch_related('medias')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Configuration de l'affichage des médias dans l'admin Django"""
    
    # Colonnes affichées dans la liste
    list_display = ('car', 'media_type', 'filename', 'uploaded_at')
    
    # Filtres disponibles à gauche
    list_filter = ('media_type',)
    
    # Champs dans lesquels on peut chercher
    search_fields = ('car__marque', 'car__modele', 'file')
    
    # Champs non éditables
    readonly_fields = ['uploaded_at']

    def filename(self, obj):
        """Retourne le nom du fichier pour l'affichage dans la liste
        
        Args:
            obj: L'objet Media
            
        Returns:
            str: Le nom du fichier
        """
        return obj.filename()
    
    filename.short_description = 'Fichier'