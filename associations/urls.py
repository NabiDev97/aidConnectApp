from django.urls import path
from . import views

app_name = 'associations'

urlpatterns = [
    path('', views.liste_associations, name='liste'),
    path('association/<int:pk>/', views.association_detail, name='detail'),
    path('creer/', views.creer_association, name='creer'),
    path('register/', views.register_association, name='register'),
    path('tableau-bord/', views.tableau_bord_association, name='tableau_bord'),
    path('besoin-urgent/creer/', views.creer_besoin_urgent, name='creer_besoin_urgent'),
    path('mes-besoins/', views.mes_besoins_urgents, name='mes_besoins_urgents'),
    path('besoins-urgents/', views.besoins_urgents, name='besoins_urgents'),
]
