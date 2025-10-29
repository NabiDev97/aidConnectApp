from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Signalement


class SignalementForm(forms.ModelForm):
    class Meta:
        model = Signalement
        fields = [
            'lieu', 'description', 'photo', 'niveau_urgence', 
            'contact_telephone', 'latitude', 'longitude', 'adresse_complete'
        ]
        widgets = {
            'lieu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Marché Sandaga, Dakar'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez la situation observée...'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'niveau_urgence': forms.Select(attrs={
                'class': 'form-control'
            }),
            'contact_telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+221 XX XXX XX XX'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Ex: 14.6928'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Ex: -17.4467'
            }),
            'adresse_complete': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Adresse complète du lieu...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lieu'].required = True
        self.fields['description'].required = True
        self.fields['niveau_urgence'].required = True


class SignalementAnonymeForm(forms.ModelForm):
    """Formulaire pour signalement anonyme (sans compte utilisateur)"""
    class Meta:
        model = Signalement
        fields = [
            'lieu', 'description', 'photo', 'niveau_urgence', 
            'contact_telephone', 'latitude', 'longitude', 'adresse_complete'
        ]
        widgets = {
            'lieu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Marché Sandaga, Dakar'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez la situation observée...'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'niveau_urgence': forms.Select(attrs={
                'class': 'form-control'
            }),
            'contact_telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+221 XX XXX XX XX (optionnel)'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Ex: 14.6928'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Ex: -17.4467'
            }),
            'adresse_complete': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Adresse complète du lieu...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lieu'].required = True
        self.fields['description'].required = True
        self.fields['niveau_urgence'].required = True
        self.fields['contact_telephone'].required = False


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
