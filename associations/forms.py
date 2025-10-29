from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Association, BesoinUrgent


class AssociationForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = [
            'nom', 'type_association', 'zone_intervention', 'description',
            'contact_telephone', 'contact_email', 'adresse', 'site_web',
            'logo', 'compte_mobile_money', 'compte_paypal'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'association',
                'required': True
            }),
            'type_association': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'zone_intervention': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description de l\'association et de ses activités...',
                'required': True
            }),
            'contact_telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+221 XX XXX XX XX',
                'required': True
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@association.sn',
                'required': True
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Adresse complète de l\'association...',
                'required': True
            }),
            'site_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.association.sn'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'compte_mobile_money': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+221 XX XXX XX XX'
            }),
            'compte_paypal': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'paypal@association.sn'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom'].required = True
        self.fields['type_association'].required = True
        self.fields['zone_intervention'].required = True
        self.fields['description'].required = True
        self.fields['contact_telephone'].required = True
        self.fields['contact_email'].required = True
        self.fields['adresse'].required = True


class BesoinUrgentForm(forms.ModelForm):
    class Meta:
        model = BesoinUrgent
        fields = [
            'type_besoin', 'description', 'quantite_demandee', 
            'montant_estime', 'est_urgent'
        ]
        widgets = {
            'type_besoin': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le besoin en détail...'
            }),
            'quantite_demandee': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 10 boîtes, 5 kg, 20 pièces...'
            }),
            'montant_estime': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Montant en FCFA'
            }),
            'est_urgent': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_besoin'].required = True
        self.fields['description'].required = True
        self.fields['quantite_demandee'].required = True


class AssociationUserForm(UserCreationForm):
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
