from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Signalement(models.Model):
    STATUT_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('en_cours', 'En cours de traitement'),
        ('pris_en_charge', 'Pris en charge'),
        ('resolu', 'Résolu'),
        ('ferme', 'Fermé'),
    ]
    
    URGENCE_CHOICES = [
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('elevee', 'Élevée'),
        ('critique', 'Critique'),
    ]
    
    lieu = models.CharField(max_length=255, verbose_name="Lieu du signalement")
    description = models.TextField(verbose_name="Description de la situation")
    photo = models.ImageField(upload_to='signalements/photos/', null=True, blank=True, verbose_name="Photo (optionnelle)")
    date_signalement = models.DateTimeField(auto_now_add=True, verbose_name="Date du signalement")
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='nouveau',
        verbose_name="Statut"
    )
    niveau_urgence = models.CharField(
        max_length=20,
        choices=URGENCE_CHOICES,
        default='moyenne',
        verbose_name="Niveau d'urgence"
    )
    utilisateur = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Utilisateur"
    )
    contact_telephone = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        verbose_name="Téléphone de contact"
    )
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitude")
    adresse_complete = models.TextField(null=True, blank=True, verbose_name="Adresse complète")
    
    class Meta:
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"
        ordering = ['-date_signalement']
    
    def __str__(self):
        return f"Signalement du {self.date_signalement.strftime('%d/%m/%Y')} - {self.lieu}"
    
    @property
    def est_ancien(self):
        """Retourne True si le signalement a plus de 7 jours"""
        return (timezone.now() - self.date_signalement).days > 7


class Intervention(models.Model):
    signalement = models.ForeignKey(
        Signalement, 
        on_delete=models.CASCADE, 
        related_name='interventions',
        verbose_name="Signalement"
    )
    association = models.ForeignKey(
        'associations.Association',
        on_delete=models.CASCADE,
        verbose_name="Association"
    )
    date_intervention = models.DateTimeField(auto_now_add=True, verbose_name="Date d'intervention")
    commentaire = models.TextField(verbose_name="Commentaire sur l'intervention")
    statut_intervention = models.CharField(
        max_length=20,
        choices=[
            ('en_cours', 'En cours'),
            ('terminee', 'Terminée'),
            ('annulee', 'Annulée'),
        ],
        default='en_cours',
        verbose_name="Statut de l'intervention"
    )
    
    class Meta:
        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"
        ordering = ['-date_intervention']
    
    def __str__(self):
        return f"Intervention {self.association.nom} - {self.signalement.lieu}"