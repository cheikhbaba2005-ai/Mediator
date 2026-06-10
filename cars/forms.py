from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Car, Media, ContactMessage, TestDriveRequest

class CarForm(forms.ModelForm):
    """Formulaire complet pour l'ajout ou la modification d'un véhicule"""
    
    image_principale = forms.ImageField(
        required=False, 
        label="Image principale",
        help_text="Ajoutez l'image principale du véhicule (optionnel)"
    )

    class Meta:
        model = Car
        fields = [
            'marque', 'modele', 'annee', 'type_offre', 
            'prix_location', 'prix_vente', 'description', 'statut'
        ]
        widgets = {
            'marque': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Toyota'}),
            'modele': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Corolla'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2022'}),
            'type_offre': forms.Select(attrs={'class': 'form-select'}),
            'prix_location': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix en F CFA par jour'}),
            'prix_vente': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix en F CFA'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description complète du véhicule...'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }


class ContactForm(forms.ModelForm):
    """Formulaire pour la page de contact"""
    class Meta:
        model = ContactMessage
        fields = ['nom', 'email', 'telephone', 'sujet', 'message']


class TestDriveForm(forms.ModelForm):
    """Formulaire de demande d'essai routier"""
    class Meta:
        model = TestDriveRequest
        fields = ['nom', 'email', 'telephone', 'date_souhaitee']
        widgets = {
            'date_souhaitee': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MediaForm(forms.ModelForm):
    """Formulaire pour uploader plusieurs images/vidéos pour un véhicule."""
    file = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=True, 
        label="Fichiers"
    )

    class Meta:
        model = Media
        fields = ['car', 'media_type', 'file']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-select'}),
            'media_type': forms.Select(attrs={'class': 'form-select'}),
        }

class UserRegistrationForm(UserCreationForm):
    """Formulaire pour créer un nouvel administrateur."""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserUpdateForm(forms.ModelForm):
    """Formulaire pour modifier un utilisateur existant."""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
