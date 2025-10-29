from django.urls import path
from . import views

app_name = 'signalements'

urlpatterns = [
    path('', views.home, name='home'),
    path('signaler/', views.signaler, name='signaler'),
    path('signalement/<int:pk>/', views.signalement_detail, name='detail'),
    path('liste/', views.liste_signalements, name='liste'),
    path('carte/', views.carte_signalements, name='carte'),
    path('register/', views.register, name='register'),
    path('mes-signalements/', views.mes_signalements, name='mes_signalements'),
    path('api/signalements/', views.api_signalements, name='api_signalements'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
