from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Don(models.Model):
    TYPE_DON_CHOICES = [
        ('argent', 'Argent'),
        ('medicament', 'Médicament'),
        ('vetement', 'Vêtement'),
        ('nourriture', 'Nourriture'),
        ('autre', 'Autre'),
    ]
    
    STATUT_DON_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('recu', 'Reçu'),
        ('annule', 'Annulé'),
    ]
    
    type_don = models.CharField(
        max_length=50,
        choices=TYPE_DON_CHOICES,
        verbose_name="Type de don"
    )
    description = models.TextField(verbose_name="Description du don")
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)],
        verbose_name="Montant (FCFA)"
    )
    quantite = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Quantité"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date du don")
    statut = models.CharField(
        max_length=20,
        choices=STATUT_DON_CHOICES,
        default='en_attente',
        verbose_name="Statut du don"
    )
    donateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Donateur"
    )
    association = models.ForeignKey(
        'associations.Association',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Association destinataire"
    )
    signalement = models.ForeignKey(
        'signalements.Signalement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Signalement lié"
    )
    commentaire_donateur = models.TextField(
        null=True,
        blank=True,
        verbose_name="Commentaire du donateur"
    )
    commentaire_association = models.TextField(
        null=True,
        blank=True,
        verbose_name="Commentaire de l'association"
    )
    
    # Informations de contact pour la remise
    telephone_contact = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Téléphone de contact"
    )
    adresse_remise = models.TextField(
        null=True,
        blank=True,
        verbose_name="Adresse de remise"
    )
    
    class Meta:
        verbose_name = "Don"
        verbose_name_plural = "Dons"
        ordering = ['-date']
    
    def __str__(self):
        return f"Don {self.get_type_don_display()} - {self.donateur.username}"


class HistoriqueDon(models.Model):
    don = models.ForeignKey(
        Don,
        on_delete=models.CASCADE,
        related_name='historique',
        verbose_name="Don"
    )
    ancien_statut = models.CharField(max_length=20, verbose_name="Ancien statut")
    nouveau_statut = models.CharField(max_length=20, verbose_name="Nouveau statut")
    date_changement = models.DateTimeField(auto_now_add=True, verbose_name="Date du changement")
    commentaire = models.TextField(
        null=True,
        blank=True,
        verbose_name="Commentaire"
    )
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Utilisateur"
    )
    
    class Meta:
        verbose_name = "Historique de don"
        verbose_name_plural = "Historiques de dons"
        ordering = ['-date_changement']
    
    def __str__(self):
        return f"Changement {self.ancien_statut} → {self.nouveau_statut}"


class CampagneDon(models.Model):
    STATUT_CAMPAGNE_CHOICES = [
        ('active', 'Active'),
        ('terminee', 'Terminée'),
        ('suspendue', 'Suspendue'),
    ]
    
    titre = models.CharField(max_length=255, verbose_name="Titre de la campagne")
    description = models.TextField(verbose_name="Description")
    association = models.ForeignKey(
        'associations.Association',
        on_delete=models.CASCADE,
        verbose_name="Association"
    )
    objectif_montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Objectif de montant (FCFA)"
    )
    montant_collecte = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Montant collecté (FCFA)"
    )
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(verbose_name="Date de fin")
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CAMPAGNE_CHOICES,
        default='active',
        verbose_name="Statut"
    )
    image = models.ImageField(
        upload_to='campagnes/',
        null=True,
        blank=True,
        verbose_name="Image"
    )
    
    class Meta:
        verbose_name = "Campagne de don"
        verbose_name_plural = "Campagnes de dons"
        ordering = ['-date_debut']
    
    def __str__(self):
        return self.titre
    
    @property
    def pourcentage_collecte(self):
        """Retourne le pourcentage de collecte par rapport à l'objectif"""
        if self.objectif_montant and self.objectif_montant > 0:
            return (self.montant_collecte / self.objectif_montant) * 100
        return 0