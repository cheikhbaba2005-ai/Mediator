"""Modèles (Models) du module Cars - Définition de la structure des données

Ce module contient les modèles de base de données pour les voitures et les médias.
Chaque classe modèle représente une table dans la base de données.
"""

from django.db import models
from django.contrib.auth.models import User  # Modèle d'utilisateur intégré à Django
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


def validate_video_extension(value):
    """Valide que le fichier uploadé a une extension vidéo acceptée
    
    Args:
        value: Le fichier à valider (FileField)
        
    Raises:
        ValidationError: Si l'extension n'est pas dans la liste des formats acceptés
    """
    # Récupère l'extension du fichier (ex: '.mp4')
    ext = os.path.splitext(value.name)[1]
    
    # Liste des formats vidéo acceptés
    valid_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
    
    # Vérifie si l'extension est acceptée (insensible à la casse)
    if not ext.lower() in valid_extensions:
        raise ValidationError("Format de fichier non supporté. Utilisez : mp4, avi, mov, wmv, flv, webm, mkv.")

class Car(models.Model):
    """Modèle pour les voitures (Véhicules)
    
    Cette classe représente une voiture qui peut être mise en location ou en vente.
    Elle contient toutes les informations nécessaires pour afficher une voiture.
    
    Attributes:
        marque (str): La marque du véhicule (Toyota, BMW, Renault, etc.)
        modele (str): Le modèle du véhicule (Corolla, X3, Clio, etc.)
        annee (int): L'année de fabrication du véhicule
        prix_location (Decimal): Le prix de location par jour (optionnel)
        prix_vente (Decimal): Le prix de vente (optionnel)
        type_offre (str): Le type d'offre (location ou vente)
        description (str): Une description détaillée du véhicule
        disponibilite (bool): Indique si le véhicule est disponible
        date_ajout (DateTime): La date à laquelle le véhicule a été ajouté
    """
    
    # Choix disponibles pour le type d'offre
    OFFRE_CHOICES = [
        ('location', 'Location'),  # Pour les voitures à louer
        ('vente', 'Vente'),        # Pour les voitures à vendre
    ]

    # Champs de base du modèle
    marque = models.CharField(max_length=100, verbose_name="Marque")
    modele = models.CharField(max_length=100, verbose_name="Modèle")
    annee = models.IntegerField(verbose_name="Année")
    
    # Champs de prix (optionnels selon le type d'offre)
    prix_location = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix location (par jour)")
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix vente")
    
    # Champ pour définir le type d'offre
    type_offre = models.CharField(max_length=10, choices=OFFRE_CHOICES, verbose_name="Type d'offre")
    
    # Autres informations
    description = models.TextField(verbose_name="Description détaillée")
    # Statut du véhicule
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('reserve', 'Réservé'),
        ('vendu', 'Vendu'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible', verbose_name="Statut")
    
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    # Configuration du modèle
    class Meta:
        verbose_name = "Voiture"                    # Nom singulier dans l'admin
        verbose_name_plural = "Voitures"           # Nom pluriel dans l'admin
        ordering = ['-date_ajout']                  # Tri par date d'ajout décroissant

    def __str__(self):
        """Retourne une représentation textuelle de la voiture
        
        Returns:
            str: Format: "Marque Modèle (Année)"
        """
        return f"{self.marque} {self.modele} ({self.annee})"

    def prix_affiche(self):
        """Retourne le prix formaté selon le type d'offre
        
        Returns:
            str: Le prix avec l'unité appropriée (€/jour pour location, € pour vente)
        """
        if self.type_offre == 'location':
            return f"{self.prix_location} € / jour"  # Format pour location
        else:
            return f"{self.prix_vente} €"            # Format pour vente


# Modèle pour les médias (photos/vidéos)
class Media(models.Model):
    """Modèle pour les médias (photos et vidéos)
    
    Cette classe représente un fichier média (image ou vidéo) associé à une voiture.
    Chaque voiture peut avoir plusieurs médias (galerie d'images/vidéos).
    
    Attributes:
        car (ForeignKey): Référence à la voiture associée
        file (FileField): Le fichier média stocké dans le dossier media/
        media_type (str): Le type de média (image ou vidéo)
        uploaded_at (DateTime): La date d'upload du fichier
    """
    
    # Choix disponibles pour le type de média
    MEDIA_CHOICES = [
        ('image', 'Image'),  # Pour les fichiers images
        ('video', 'Vidéo'),  # Pour les fichiers vidéos
    ]

    # Relation avec la voiture (une voiture peut avoir plusieurs médias)
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE,          # Supprime les médias si la voiture est supprimée
        related_name='medias',             # Permet d'accéder aux médias via voiture.medias
        verbose_name="Voiture associée"
    )
    
    # Le fichier lui-même (image ou vidéo)
    file = models.FileField(
        upload_to='media/',                # Les fichiers sont stockés dans le dossier media/
        verbose_name="Fichier"
    )
    
    # Le type de média
    media_type = models.CharField(
        max_length=5, 
        choices=MEDIA_CHOICES, 
        verbose_name="Type de média"
    )
    
    # Timestamp de l'upload
    uploaded_at = models.DateTimeField(
        auto_now_add=True,                 # Défini automatiquement à la création
        verbose_name="Date d'upload"
    )

    # Configuration du modèle
    class Meta:
        verbose_name = "Média"             # Nom singulier dans l'admin
        verbose_name_plural = "Médias"    # Nom pluriel dans l'admin
        ordering = ['-uploaded_at']        # Tri par date d'upload décroissant

    def __str__(self):
        """Retourne une représentation textuelle du média
        
        Returns:
            str: Format: "Type de média pour Marque Modèle"
        """
        return f"{self.get_media_type_display()} pour {self.car}"

    def filename(self):
        """Retourne le nom du fichier seulement (sans le chemin)
        
        Returns:
            str: Le nom du fichier (ex: 'image.jpg')
        """
        return os.path.basename(self.file.name)
        
    def save(self, *args, **kwargs):
        """Surcharge de la méthode save pour optimiser les images avant sauvegarde"""
        if self.media_type == 'image' and self.file:
            # Ouvrir l'image avec Pillow
            img = Image.open(self.file)
            # Convertir en RGB si nécessaire (ex: PNG avec transparence vers JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Redimensionner si l'image est trop grande (max 1200px)
            max_size = (1200, 1200)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Sauvegarder dans un buffer en mémoire
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85, optimize=True)
            buffer.seek(0)
            
            # Changer le nom et le contenu du fichier
            original_filename = os.path.basename(self.file.name)
            filename_without_ext = os.path.splitext(original_filename)[0]
            new_filename = f"{filename_without_ext}_optim.jpg"
            
            self.file.save(new_filename, ContentFile(buffer.read()), save=False)
            
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """Modèle pour stocker les messages de contact"""
    nom = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    sujet = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Lu")
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']
        
    def __str__(self):
        return f"Message de {self.nom} - {self.sujet}"


class TestDriveRequest(models.Model):
    """Modèle pour les demandes d'essai routier"""
    STATUT_DEMANDE = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]
    
    voiture = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='test_drives', verbose_name="Véhicule")
    nom = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    date_souhaitee = models.DateTimeField(verbose_name="Date souhaitée pour l'essai", null=True, blank=True)
    statut_demande = models.CharField(max_length=20, choices=STATUT_DEMANDE, default='en_attente', verbose_name="Statut de la demande")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de la demande")
    
    class Meta:
        verbose_name = "Demande d'essai"
        verbose_name_plural = "Demandes d'essai"
        ordering = ['-date_creation']
        
    def __str__(self):
        return f"Essai pour {self.voiture} par {self.nom}"
    
    