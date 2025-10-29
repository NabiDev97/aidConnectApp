from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.db import models
from .models import Don, CampagneDon, HistoriqueDon
from .forms import DonForm, DonRapideForm, CampagneDonForm
from associations.models import Association, BesoinUrgent


def liste_dons(request):
    """Liste de tous les dons publics"""
    dons = Don.objects.filter(statut__in=['confirme', 'recu']).order_by('-date')
    
    # Filtres
    type_don = request.GET.get('type')
    association_id = request.GET.get('association')
    
    if type_don:
        dons = dons.filter(type_don=type_don)
    if association_id:
        dons = dons.filter(association_id=association_id)
    
    # Pagination
    paginator = Paginator(dons, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'type_don': type_don,
        'association_id': association_id,
    }
    return render(request, 'dons/liste_dons.html', context)


@login_required
def faire_don(request):
    """Formulaire pour faire un don"""
    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.donateur = request.user
            don.save()
            messages.success(request, 'Votre don a été enregistré ! L\'association vous contactera bientôt.')
            return redirect('dons:mes_dons')
    else:
        form = DonForm()
    
    # Statistiques pour la page
    from associations.models import Association
    total_associations = Association.objects.count()
    total_dons = Don.objects.count()
    montant_total = Don.objects.aggregate(total=models.Sum('montant'))['total'] or 0
    
    context = {
        'form': form,
        'total_associations': total_associations,
        'total_dons': total_dons,
        'montant_total': montant_total
    }
    
    return render(request, 'dons/faire_don.html', context)


@login_required
def don_rapide(request):
    """Formulaire de don rapide"""
    if request.method == 'POST':
        form = DonRapideForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.donateur = request.user
            don.save()
            messages.success(request, 'Votre don rapide a été enregistré !')
            return redirect('dons:mes_dons')
    else:
        form = DonRapideForm()
    
    return render(request, 'dons/don_rapide.html', {'form': form})


@login_required
def mes_dons(request):
    """Dons de l'utilisateur connecté"""
    dons = Don.objects.filter(donateur=request.user).order_by('-date')
    
    # Statistiques personnelles
    total_dons = dons.count()
    montant_total = dons.aggregate(total=models.Sum('montant'))['total'] or 0
    dons_confirmes = dons.filter(statut='confirme').count()
    associations_soutenues = dons.values('association').distinct().count()
    
    paginator = Paginator(dons, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_dons': total_dons,
        'montant_total': montant_total,
        'dons_confirmes': dons_confirmes,
        'associations_soutenues': associations_soutenues,
    }
    return render(request, 'dons/mes_dons.html', context)


def don_detail(request, pk):
    """Détail d'un don"""
    don = get_object_or_404(Don, pk=pk)
    
    # Vérifier si l'utilisateur peut voir ce don
    if not request.user.is_authenticated or (don.donateur != request.user and not don.association.utilisateur == request.user):
        messages.error(request, 'Vous n\'avez pas accès à ce don.')
        return redirect('dons:liste_dons')
    
    context = {
        'don': don,
    }
    return render(request, 'dons/don_detail.html', context)


def campagnes_dons(request):
    """Liste des campagnes de dons actives"""
    campagnes = CampagneDon.objects.filter(statut='active').order_by('-date_debut')
    
    # Pagination
    paginator = Paginator(campagnes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'dons/campagnes_dons.html', context)


def campagne_detail(request, pk):
    """Détail d'une campagne de don"""
    campagne = get_object_or_404(CampagneDon, pk=pk)
    
    # Dons récents pour cette campagne
    dons_campagne = Don.objects.filter(
        association=campagne.association,
        date__gte=campagne.date_debut,
        statut__in=['confirme', 'recu']
    ).order_by('-date')[:10]
    
    context = {
        'campagne': campagne,
        'dons_campagne': dons_campagne,
    }
    return render(request, 'dons/campagne_detail.html', context)


@login_required
def creer_campagne(request):
    """Création d'une campagne de don"""
    try:
        association = Association.objects.get(utilisateur=request.user)
    except Association.DoesNotExist:
        messages.error(request, 'Vous devez être associé à une association pour créer une campagne.')
        return redirect('associations:creer_association')
    
    if request.method == 'POST':
        form = CampagneDonForm(request.POST, request.FILES)
        if form.is_valid():
            campagne = form.save(commit=False)
            campagne.association = association
            campagne.save()
            messages.success(request, 'Votre campagne de don a été créée !')
            return redirect('dons:campagne_detail', pk=campagne.pk)
    else:
        form = CampagneDonForm()
    
    return render(request, 'dons/creer_campagne.html', {'form': form})


@login_required
def mes_campagnes(request):
    """Campagnes de l'association de l'utilisateur"""
    try:
        association = Association.objects.get(utilisateur=request.user)
    except Association.DoesNotExist:
        messages.error(request, 'Vous devez être associé à une association.')
        return redirect('associations:creer_association')
    
    campagnes = CampagneDon.objects.filter(association=association).order_by('-date_debut')
    
    paginator = Paginator(campagnes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'association': association,
    }
    return render(request, 'dons/mes_campagnes.html', context)


def statistiques_dons(request):
    """Page de statistiques des dons"""
    # Statistiques générales
    total_dons = Don.objects.count()
    montant_total = Don.objects.aggregate(total=Sum('montant'))['total'] or 0
    dons_confirmes = Don.objects.filter(statut='confirme').count()
    dons_recus = Don.objects.filter(statut='recu').count()
    
    # Dons par type
    dons_par_type = Don.objects.values('type_don').annotate(
        count=Count('id'),
        montant=Sum('montant')
    ).order_by('-count')
    
    # Top associations
    top_associations = Association.objects.annotate(
        nombre_dons=Count('don'),
        montant_total=Sum('don__montant')
    ).order_by('-nombre_dons')[:5]
    
    context = {
        'total_dons': total_dons,
        'montant_total': montant_total,
        'dons_confirmes': dons_confirmes,
        'dons_recus': dons_recus,
        'dons_par_type': dons_par_type,
        'top_associations': top_associations,
    }
    return render(request, 'dons/statistiques.html', context)


@login_required
def gerer_don(request, pk):
    """Gestion d'un don par l'association"""
    don = get_object_or_404(Don, pk=pk)
    
    # Vérifier que l'utilisateur est de l'association destinataire
    if don.association.utilisateur != request.user:
        messages.error(request, 'Vous ne pouvez pas gérer ce don.')
        return redirect('dons:mes_dons')
    
    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        commentaire = request.POST.get('commentaire', '')
        
        if nouveau_statut and nouveau_statut != don.statut:
            # Créer un historique
            HistoriqueDon.objects.create(
                don=don,
                ancien_statut=don.statut,
                nouveau_statut=nouveau_statut,
                commentaire=commentaire,
                utilisateur=request.user
            )
            
            # Mettre à jour le statut
            don.statut = nouveau_statut
            if commentaire:
                don.commentaire_association = commentaire
            don.save()
            
            messages.success(request, f'Le statut du don a été mis à jour : {don.get_statut_display()}')
            return redirect('dons:don_detail', pk=don.pk)
    
    context = {
        'don': don,
    }
    return render(request, 'dons/gerer_don.html', context)