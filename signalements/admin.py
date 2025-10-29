from django.contrib import admin
from .models import Signalement, Intervention


@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = [
        'lieu', 'niveau_urgence', 'statut', 'date_signalement', 
        'utilisateur', 'contact_telephone'
    ]
    list_filter = [
        'statut', 'niveau_urgence', 'date_signalement', 'utilisateur'
    ]
    search_fields = ['lieu', 'description', 'contact_telephone']
    readonly_fields = ['date_signalement']
    ordering = ['-date_signalement']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('lieu', 'description', 'photo', 'niveau_urgence', 'statut')
        }),
        ('Contact', {
            'fields': ('utilisateur', 'contact_telephone')
        }),
        ('Localisation', {
            'fields': ('latitude', 'longitude', 'adresse_complete')
        }),
        ('Métadonnées', {
            'fields': ('date_signalement',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('utilisateur')


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = [
        'signalement', 'association', 'date_intervention', 
        'statut_intervention'
    ]
    list_filter = [
        'statut_intervention', 'date_intervention', 'association'
    ]
    search_fields = ['signalement__lieu', 'association__nom', 'commentaire']
    readonly_fields = ['date_intervention']
    ordering = ['-date_intervention']
    
    fieldsets = (
        ('Intervention', {
            'fields': ('signalement', 'association', 'statut_intervention')
        }),
        ('Détails', {
            'fields': ('commentaire', 'date_intervention')
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('signalement', 'association')