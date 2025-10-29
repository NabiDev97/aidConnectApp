from django.contrib import admin
from .models import Don, CampagneDon, HistoriqueDon


@admin.register(Don)
class DonAdmin(admin.ModelAdmin):
    list_display = [
        'donateur', 'type_don', 'montant', 'association', 
        'statut', 'date'
    ]
    list_filter = [
        'type_don', 'statut', 'date', 'association'
    ]
    search_fields = [
        'donateur__username', 'donateur__first_name', 
        'donateur__last_name', 'description', 'association__nom'
    ]
    readonly_fields = ['date']
    ordering = ['-date']
    
    fieldsets = (
        ('Don', {
            'fields': ('donateur', 'type_don', 'description', 'montant', 'quantite')
        }),
        ('Destinataire', {
            'fields': ('association', 'signalement')
        }),
        ('Statut', {
            'fields': ('statut',)
        }),
        ('Contact', {
            'fields': ('telephone_contact', 'adresse_remise'),
            'classes': ('collapse',)
        }),
        ('Commentaires', {
            'fields': ('commentaire_donateur', 'commentaire_association'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('date',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'donateur', 'association', 'signalement'
        )


@admin.register(CampagneDon)
class CampagneDonAdmin(admin.ModelAdmin):
    list_display = [
        'titre', 'association', 'objectif_montant', 
        'montant_collecte', 'statut', 'date_debut', 'date_fin'
    ]
    list_filter = [
        'statut', 'date_debut', 'date_fin', 'association'
    ]
    search_fields = [
        'titre', 'description', 'association__nom'
    ]
    ordering = ['-date_debut']
    
    fieldsets = (
        ('Campagne', {
            'fields': ('titre', 'description', 'association', 'image')
        }),
        ('Objectifs', {
            'fields': ('objectif_montant', 'montant_collecte')
        }),
        ('Période', {
            'fields': ('date_debut', 'date_fin', 'statut')
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('association')


@admin.register(HistoriqueDon)
class HistoriqueDonAdmin(admin.ModelAdmin):
    list_display = [
        'don', 'ancien_statut', 'nouveau_statut', 
        'date_changement', 'utilisateur'
    ]
    list_filter = [
        'ancien_statut', 'nouveau_statut', 'date_changement'
    ]
    search_fields = [
        'don__donateur__username', 'commentaire', 'utilisateur__username'
    ]
    readonly_fields = ['date_changement']
    ordering = ['-date_changement']
    
    fieldsets = (
        ('Changement', {
            'fields': ('don', 'ancien_statut', 'nouveau_statut')
        }),
        ('Détails', {
            'fields': ('commentaire', 'utilisateur', 'date_changement')
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'don', 'don__donateur', 'utilisateur'
        )