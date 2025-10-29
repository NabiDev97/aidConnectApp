from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Association(models.Model):
    TYPE_ASSOCIATION_CHOICES = [
        ('sante_mentale', 'Santé Mentale'),
        ('aide_sociale', 'Aide Sociale'),
        ('urgence', 'Urgence'),
        ('benevoles', 'Bénévoles'),
        ('autre', 'Autre'),
    ]
    
    ZONE_CHOICES = [
        ('dakar', 'Dakar'),
        ('thies', 'Thiès'),
        ('kaolack', 'Kaolack'),
        ('saint_louis', 'Saint-Louis'),
        ('ziguinchor', 'Ziguinchor'),
        ('tambacounda', 'Tambacounda'),
        ('kolda', 'Kolda'),
        ('matam', 'Matam'),
        ('autre', 'Autre'),
    ]
    
    nom = models.CharField(max_length=255, verbose_name="Nom de l'association")
    type_association = models.CharField(
        max_length=50,
        choices=TYPE_ASSOCIATION_CHOICES,
        default='sante_mentale',
        verbose_name="Type d'association"
    )
    zone_intervention = models.CharField(
        max_length=50,
        choices=ZONE_CHOICES,
        verbose_name="Zone d'intervention"
    )
    description = models.TextField(verbose_name="Description de l'association")
    contact_telephone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Format de téléphone invalide")],
        verbose_name="Téléphone de contact"
    )
    contact_email = models.EmailField(verbose_name="Email de contact")
    adresse = models.TextField(verbose_name="Adresse")
    site_web = models.URLField(blank=True, null=True, verbose_name="Site web")
    logo = models.ImageField(
        upload_to='associations/logos/', 
        null=True, 
        blank=True,
        verbose_name="Logo"
    )
    utilisateur = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Utilisateur responsable"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    est_verifiee = models.BooleanField(default=False, verbose_name="Association vérifiée")
    est_active = models.BooleanField(default=True, verbose_name="Association active")
    
    # Informations pour les dons
    compte_mobile_money = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Compte Mobile Money"
    )
    compte_paypal = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email PayPal"
    )
    
    class Meta:
        verbose_name = "Association"
        verbose_name_plural = "Associations"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    @property
    def nombre_interventions(self):
        """Retourne le nombre d'interventions de cette association"""
        return self.intervention_set.count()
    
    @property
    def nombre_signalements_actifs(self):
        """Retourne le nombre de signalements actifs pour cette association"""
        return self.intervention_set.filter(
            statut_intervention='en_cours'
        ).count()


class BesoinUrgent(models.Model):
    TYPE_BESOIN_CHOICES = [
        ('argent', 'Argent'),
        ('medicament', 'Médicament'),
        ('vetement', 'Vêtement'),
        ('nourriture', 'Nourriture'),
        ('transport', 'Transport'),
        ('autre', 'Autre'),
    ]
    
    association = models.ForeignKey(
        Association,
        on_delete=models.CASCADE,
        related_name='besoins_urgents',
        verbose_name="Association"
    )
    type_besoin = models.CharField(
        max_length=50,
        choices=TYPE_BESOIN_CHOICES,
        verbose_name="Type de besoin"
    )
    description = models.TextField(verbose_name="Description du besoin")
    quantite_demandee = models.CharField(
        max_length=100,
        verbose_name="Quantité demandée"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    est_urgent = models.BooleanField(default=True, verbose_name="Besoin urgent")
    est_satisfait = models.BooleanField(default=False, verbose_name="Besoin satisfait")
    montant_estime = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Montant estimé (FCFA)"
    )
    
    class Meta:
        verbose_name = "Besoin urgent"
        verbose_name_plural = "Besoins urgents"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.get_type_besoin_display()} - {self.association.nom}"