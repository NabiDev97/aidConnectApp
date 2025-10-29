from django.urls import path
from . import views

app_name = 'dons'

urlpatterns = [
    path('', views.liste_dons, name='liste'),
    path('faire-don/', views.faire_don, name='faire_don'),
    path('don-rapide/', views.don_rapide, name='don_rapide'),
    path('mes-dons/', views.mes_dons, name='mes_dons'),
    path('don/<int:pk>/', views.don_detail, name='detail'),
    path('campagnes/', views.campagnes_dons, name='campagnes'),
    path('campagne/<int:pk>/', views.campagne_detail, name='campagne_detail'),
    path('creer-campagne/', views.creer_campagne, name='creer_campagne'),
    path('mes-campagnes/', views.mes_campagnes, name='mes_campagnes'),
    path('statistiques/', views.statistiques_dons, name='statistiques'),
    path('gerer-don/<int:pk>/', views.gerer_don, name='gerer_don'),
]
