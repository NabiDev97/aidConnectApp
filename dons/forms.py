from django import forms
from django.contrib.auth.models import User
from .models import Don, CampagneDon
from associations.models import Association


class DonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = [
            'type_don', 'description', 'montant', 'quantite',
            'association', 'signalement', 'commentaire_donateur',
            'telephone_contact', 'adresse_remise'
        ]
        widgets = {
            'type_don': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez votre don...'
            }),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Montant en FCFA'
            }),
            'quantite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 10 boîtes, 5 kg, 20 pièces...'
            }),
            'association': forms.Select(attrs={
                'class': 'form-control'
            }),
            'signalement': forms.Select(attrs={
                'class': 'form-control'
            }),
            'commentaire_donateur': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Commentaire optionnel...'
            }),
            'telephone_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+221 XX XXX XX XX'
            }),
            'adresse_remise': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Adresse où remettre le don...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_don'].required = True
        self.fields['description'].required = True
        self.fields['association'].required = True
        
        # Filtrer les associations actives
        self.fields['association'].queryset = Association.objects.filter(est_active=True)
        
        # Rendre les champs optionnels selon le type de don
        self.fields['montant'].required = False
        self.fields['quantite'].required = False
        self.fields['signalement'].required = False
        self.fields['commentaire_donateur'].required = False
        self.fields['telephone_contact'].required = False
        self.fields['adresse_remise'].required = False


class DonRapideForm(forms.ModelForm):
    """Formulaire simplifié pour don rapide"""
    class Meta:
        model = Don
        fields = ['type_don', 'description', 'montant', 'association']
        widgets = {
            'type_don': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description rapide de votre don...'
            }),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Montant en FCFA'
            }),
            'association': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_don'].required = True
        self.fields['description'].required = True
        self.fields['association'].required = True
        self.fields['montant'].required = False
        
        # Filtrer les associations actives
        self.fields['association'].queryset = Association.objects.filter(est_active=True)


class CampagneDonForm(forms.ModelForm):
    class Meta:
        model = CampagneDon
        fields = [
            'titre', 'description', 'association', 'objectif_montant',
            'date_debut', 'date_fin', 'image'
        ]
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la campagne'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description de la campagne...'
            }),
            'association': forms.Select(attrs={
                'class': 'form-control'
            }),
            'objectif_montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Objectif en FCFA'
            }),
            'date_debut': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'date_fin': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titre'].required = True
        self.fields['description'].required = True
        self.fields['association'].required = True
        self.fields['date_debut'].required = True
        self.fields['date_fin'].required = True
        
        # Filtrer les associations actives
        self.fields['association'].queryset = Association.objects.filter(est_active=True)
