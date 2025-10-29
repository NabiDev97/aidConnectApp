from django.contrib import admin
from .models import Association, BesoinUrgent


@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = [
        'nom', 'type_association', 'zone_intervention', 
        'est_verifiee', 'est_active', 'date_creation'
    ]
    list_filter = [
        'type_association', 'zone_intervention', 'est_verifiee', 
        'est_active', 'date_creation'
    ]
    search_fields = [
        'nom', 'description', 'contact_telephone', 
        'contact_email', 'utilisateur__username'
    ]
    readonly_fields = ['date_creation']
    ordering = ['nom']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'type_association', 'zone_intervention', 'description')
        }),
        ('Contact', {
            'fields': ('contact_telephone', 'contact_email', 'adresse', 'site_web')
        }),
        ('Comptes pour dons', {
            'fields': ('compte_mobile_money', 'compte_paypal'),
            'classes': ('collapse',)
        }),
        ('Utilisateur et statut', {
            'fields': ('utilisateur', 'est_verifiee', 'est_active')
        }),
        ('Métadonnées', {
            'fields': ('logo', 'date_creation'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('utilisateur')


@admin.register(BesoinUrgent)
class BesoinUrgentAdmin(admin.ModelAdmin):
    list_display = [
        'association', 'type_besoin', 'quantite_demandee', 
        'montant_estime', 'est_urgent', 'est_satisfait', 'date_creation'
    ]
    list_filter = [
        'type_besoin', 'est_urgent', 'est_satisfait', 
        'date_creation', 'association'
    ]
    search_fields = [
        'description', 'quantite_demandee', 'association__nom'
    ]
    readonly_fields = ['date_creation']
    ordering = ['-date_creation']
    
    fieldsets = (
        ('Besoin', {
            'fields': ('association', 'type_besoin', 'description')
        }),
        ('Détails', {
            'fields': ('quantite_demandee', 'montant_estime')
        }),
        ('Statut', {
            'fields': ('est_urgent', 'est_satisfait')
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('association')