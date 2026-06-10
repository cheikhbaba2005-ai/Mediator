"""Configuration du panneau d'administration Django pour les voitures et médias

Ce module configure comment les modèles Car et Media sont affichés et gérés
dans le panneau d'administration Django.
"""

from django.contrib import admin
from .models import Car, Media, ContactMessage, TestDriveRequest
from django.utils.html import format_html


class MediaInline(admin.TabularInline):
    """Affiche les médias associés à une voiture dans la même page d'édition"""
    model = Media
    extra = 1  # Ajoute 1 ligne vide pour ajouter un nouveau média
    fields = ['file', 'media_type', 'uploaded_at']
    readonly_fields = ['uploaded_at']  # Empêche la modification de la date


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Configuration de l'affichage des voitures dans l'admin Django"""
    
    list_display = ('marque', 'modele', 'annee', 'type_offre', 'prix_affiche', 'statut', 'nb_medias')
    list_filter = ('type_offre', 'statut', 'marque', 'annee')
    search_fields = ('marque', 'modele', 'description')
    inlines = [MediaInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('marque', 'modele', 'annee', 'type_offre', 'statut')
        }),
        ('Prix', {
            'fields': ('prix_location', 'prix_vente'),
            'description': 'Remplissez le prix correspondant au type d\'offre. Laissez vide l\'autre.'
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )
    
    list_editable = ['statut']
    list_per_page = 25

    def nb_medias(self, obj):
        count = obj.medias.count()
        return format_html('<span class="badge badge-secondary">{}</span>', count)
    
    nb_medias.short_description = 'Médias'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('medias')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Configuration de l'affichage des médias dans l'admin Django"""
    list_display = ('car', 'media_type', 'filename', 'uploaded_at')
    list_filter = ('media_type',)
    search_fields = ('car__marque', 'car__modele', 'file')
    readonly_fields = ['uploaded_at']

    def filename(self, obj):
        return obj.filename()
    
    filename.short_description = 'Fichier'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi', 'lu')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('nom', 'email', 'sujet', 'message')
    list_editable = ['lu']
    readonly_fields = ['date_envoi']


@admin.register(TestDriveRequest)
class TestDriveRequestAdmin(admin.ModelAdmin):
    list_display = ('voiture', 'nom', 'telephone', 'date_souhaitee', 'statut_demande', 'date_creation')
    list_filter = ('statut_demande', 'date_creation')
    search_fields = ('nom', 'email', 'telephone', 'voiture__marque', 'voiture__modele')
    list_editable = ['statut_demande']
    readonly_fields = ['date_creation']