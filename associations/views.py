from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Association, BesoinUrgent
from .forms import AssociationForm, BesoinUrgentForm, AssociationUserForm
from signalements.models import Signalement


def liste_associations(request):
    """Liste de toutes les associations"""
    associations = Association.objects.filter(est_active=True).order_by('nom')
    
    # Filtres
    type_association = request.GET.get('type')
    zone = request.GET.get('zone')
    recherche = request.GET.get('recherche')
    
    if type_association:
        associations = associations.filter(type_association=type_association)
    if zone:
        associations = associations.filter(zone_intervention=zone)
    if recherche:
        associations = associations.filter(
            Q(nom__icontains=recherche) | 
            Q(description__icontains=recherche)
        )
    
    # Pagination
    paginator = Paginator(associations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'type_association': type_association,
        'zone': zone,
        'recherche': recherche,
    }
    return render(request, 'associations/liste_associations.html', context)


def association_detail(request, pk):
    """Détail d'une association"""
    association = get_object_or_404(Association, pk=pk, est_active=True)
    besoins_urgents = association.besoins_urgents.filter(est_satisfait=False).order_by('-date_creation')[:5]
    
    context = {
        'association': association,
        'besoins_urgents': besoins_urgents,
    }
    return render(request, 'associations/association_detail.html', context)


@login_required
def creer_association(request):
    """Création d'une nouvelle association"""
    if request.method == 'POST':
        form = AssociationForm(request.POST, request.FILES)
        if form.is_valid():
            association = form.save(commit=False)
            association.utilisateur = request.user
            association.save()
            messages.success(request, 'Votre association a été créée avec succès !')
            return redirect('associations:detail', pk=association.pk)
    else:
        form = AssociationForm()
    
    return render(request, 'associations/creer_association.html', {'form': form})


@login_required
def register_association(request):
    """Inscription d'un utilisateur pour une association"""
    if request.method == 'POST':
        user_form = AssociationUserForm(request.POST)
        association_form = AssociationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and association_form.is_valid():
            user = user_form.save()
            login(request, user)
            
            association = association_form.save(commit=False)
            association.utilisateur = user
            association.save()
            
            messages.success(request, 'Votre compte association a été créé avec succès !')
            return redirect('associations:detail', pk=association.pk)
    else:
        user_form = AssociationUserForm()
        association_form = AssociationForm()
    
    context = {
        'user_form': user_form,
        'association_form': association_form,
    }
    return render(request, 'associations/register_association.html', context)


@login_required
def tableau_bord_association(request):
    """Tableau de bord pour les associations"""
    try:
        association = Association.objects.get(utilisateur=request.user)
    except Association.DoesNotExist:
        messages.error(request, 'Vous devez être associé à une association pour accéder à cette page.')
        return redirect('associations:creer_association')
    
    # Statistiques
    signalements_assignes = Signalement.objects.filter(
        interventions__association=association
    ).distinct()
    
    signalements_nouveaux = signalements_assignes.filter(statut='nouveau').count()
    signalements_en_cours = signalements_assignes.filter(statut='en_cours').count()
    signalements_resolus = signalements_assignes.filter(statut='resolu').count()
    
    # Derniers signalements
    derniers_signalements = signalements_assignes.order_by('-date_signalement')[:10]
    
    # Besoins urgents
    besoins_urgents = association.besoins_urgents.filter(est_satisfait=False).order_by('-date_creation')[:5]
    
    context = {
        'association': association,
        'signalements_nouveaux': signalements_nouveaux,
        'signalements_en_cours': signalements_en_cours,
        'signalements_resolus': signalements_resolus,
        'derniers_signalements': derniers_signalements,
        'besoins_urgents': besoins_urgents,
    }
    return render(request, 'associations/tableau_bord.html', context)


@login_required
def creer_besoin_urgent(request):
    """Création d'un besoin urgent"""
    try:
        association = Association.objects.get(utilisateur=request.user)
    except Association.DoesNotExist:
        messages.error(request, 'Vous devez être associé à une association pour créer un besoin urgent.')
        return redirect('associations:creer_association')
    
    if request.method == 'POST':
        form = BesoinUrgentForm(request.POST)
        if form.is_valid():
            besoin = form.save(commit=False)
            besoin.association = association
            besoin.save()
            messages.success(request, 'Votre besoin urgent a été publié !')
            return redirect('associations:tableau_bord')
    else:
        form = BesoinUrgentForm()
    
    return render(request, 'associations/creer_besoin_urgent.html', {'form': form})


@login_required
def mes_besoins_urgents(request):
    """Liste des besoins urgents de l'association"""
    try:
        association = Association.objects.get(utilisateur=request.user)
    except Association.DoesNotExist:
        messages.error(request, 'Vous devez être associé à une association.')
        return redirect('associations:creer_association')
    
    besoins = association.besoins_urgents.all().order_by('-date_creation')
    
    paginator = Paginator(besoins, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'association': association,
    }
    return render(request, 'associations/mes_besoins_urgents.html', context)


def besoins_urgents(request):
    """Liste de tous les besoins urgents"""
    besoins = BesoinUrgent.objects.filter(est_satisfait=False).order_by('-date_creation')
    
    # Filtres
    type_besoin = request.GET.get('type')
    association_id = request.GET.get('association')
    
    if type_besoin:
        besoins = besoins.filter(type_besoin=type_besoin)
    if association_id:
        besoins = besoins.filter(association_id=association_id)
    
    # Pagination
    paginator = Paginator(besoins, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'type_besoin': type_besoin,
        'association_id': association_id,
    }
    return render(request, 'associations/besoins_urgents.html', context)