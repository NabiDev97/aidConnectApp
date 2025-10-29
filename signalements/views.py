from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from .models import Signalement, Intervention
from .forms import SignalementForm, SignalementAnonymeForm, UserRegistrationForm


def home(request):
    """Page d'accueil avec statistiques et derniers signalements"""
    signalements_recents = Signalement.objects.filter(statut='nouveau').order_by('-date_signalement')[:5]
    total_signalements = Signalement.objects.count()
    signalements_urgents = Signalement.objects.filter(niveau_urgence='critique').count()
    
    context = {
        'signalements_recents': signalements_recents,
        'total_signalements': total_signalements,
        'signalements_urgents': signalements_urgents,
    }
    return render(request, 'signalements/home.html', context)


def signaler(request):
    """Page de signalement - accessible avec ou sans compte"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = SignalementForm(request.POST, request.FILES)
        else:
            form = SignalementAnonymeForm(request.POST, request.FILES)
        
        if form.is_valid():
            signalement = form.save(commit=False)
            if request.user.is_authenticated:
                signalement.utilisateur = request.user
            signalement.save()
            messages.success(request, 'Votre signalement a été enregistré avec succès !')
            return redirect('signalements:detail', pk=signalement.pk)
    else:
        if request.user.is_authenticated:
            form = SignalementForm()
        else:
            form = SignalementAnonymeForm()
    
    context = {
        'form': form,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'signalements/signaler_simple.html', context)


def signalement_detail(request, pk):
    """Détail d'un signalement"""
    signalement = get_object_or_404(Signalement, pk=pk)
    interventions = signalement.interventions.all()
    
    context = {
        'signalement': signalement,
        'interventions': interventions,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'signalements/signalement_detail.html', context)


def liste_signalements(request):
    """Liste de tous les signalements avec filtres"""
    signalements = Signalement.objects.all().order_by('-date_signalement')
    
    # Filtres
    statut = request.GET.get('statut')
    urgence = request.GET.get('urgence')
    zone = request.GET.get('zone')
    recherche = request.GET.get('recherche')
    
    if statut:
        signalements = signalements.filter(statut=statut)
    if urgence:
        signalements = signalements.filter(niveau_urgence=urgence)
    if zone:
        signalements = signalements.filter(lieu__icontains=zone)
    if recherche:
        signalements = signalements.filter(
            Q(lieu__icontains=recherche) | 
            Q(description__icontains=recherche)
        )
    
    # Pagination
    paginator = Paginator(signalements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'statut': statut,
        'urgence': urgence,
        'zone': zone,
        'recherche': recherche,
    }
    return render(request, 'signalements/liste_signalements.html', context)


def carte_signalements(request):
    """Carte interactive des signalements"""
    signalements = Signalement.objects.all()
    
    # Préparer les données pour la carte
    signalements_data = []
    for signalement in signalements:
        if signalement.latitude and signalement.longitude:
            signalements_data.append({
                'id': signalement.id,
                'lieu': signalement.lieu,
                'description': signalement.description[:100] + '...' if len(signalement.description) > 100 else signalement.description,
                'statut': signalement.statut,
                'urgence': signalement.niveau_urgence,
                'date': signalement.date_signalement.strftime('%d/%m/%Y'),
                'lat': float(signalement.latitude),
                'lng': float(signalement.longitude),
            })
    
    context = {
        'signalements_data': signalements_data,
    }
    return render(request, 'signalements/carte.html', context)


def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('signalements:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'signalements/register.html', {'form': form})


@login_required
def mes_signalements(request):
    """Signalements de l'utilisateur connecté"""
    signalements = Signalement.objects.filter(utilisateur=request.user).order_by('-date_signalement')
    
    paginator = Paginator(signalements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'signalements/mes_signalements.html', context)


def api_signalements(request):
    """API pour récupérer les signalements (pour la carte)"""
    signalements = Signalement.objects.all()
    
    data = []
    for signalement in signalements:
        if signalement.latitude and signalement.longitude:
            data.append({
                'id': signalement.id,
                'lieu': signalement.lieu,
                'description': signalement.description,
                'statut': signalement.statut,
                'urgence': signalement.niveau_urgence,
                'date': signalement.date_signalement.isoformat(),
                'lat': float(signalement.latitude),
                'lng': float(signalement.longitude),
            })
    
    return JsonResponse(data, safe=False)


def logout_view(request):
    """Vue de déconnexion personnalisée"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('signalements:home')


class CustomLoginView(LoginView):
    """Vue de connexion personnalisée"""
    template_name = 'signalements/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirection après connexion réussie"""
        return '/'