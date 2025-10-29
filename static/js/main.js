// Fonction pour basculer le menu mobile avec animations
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuButton = document.querySelector('.mobile-menu-btn');
    
    if (mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.remove('hidden');
        mobileMenu.classList.add('slide-down');
        menuButton.innerHTML = '<i class="fas fa-times text-lg"></i>';
        menuButton.classList.add('bg-primary-100', 'text-primary-600');
    } else {
        mobileMenu.classList.add('hidden');
        mobileMenu.classList.remove('slide-down');
        menuButton.innerHTML = '<i class="fas fa-bars text-lg"></i>';
        menuButton.classList.remove('bg-primary-100', 'text-primary-600');
    }
}

// Fermer le menu mobile quand on clique à l'extérieur
document.addEventListener('click', function(event) {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuButton = event.target.closest('.mobile-menu-btn');
    
    if (!mobileMenu.contains(event.target) && !menuButton && !mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.add('hidden');
        mobileMenu.classList.remove('slide-down');
        const menuBtn = document.querySelector('.mobile-menu-btn');
        menuBtn.innerHTML = '<i class="fas fa-bars text-lg"></i>';
        menuBtn.classList.remove('bg-primary-100', 'text-primary-600');
    }
});

// Fonction pour fermer le menu mobile automatiquement
function closeMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuButton = document.querySelector('.mobile-menu-btn');
    
    if (!mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.add('hidden');
        mobileMenu.classList.remove('slide-down');
        menuButton.innerHTML = '<i class="fas fa-bars text-lg"></i>';
        menuButton.classList.remove('bg-primary-100', 'text-primary-600');
    }
}

// Fonction pour afficher les coordonnées GPS
function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                // Remplir les champs latitude et longitude
                const latField = document.getElementById('id_latitude');
                const lngField = document.getElementById('id_longitude');
                
                if (latField) latField.value = lat.toFixed(6);
                if (lngField) lngField.value = lng.toFixed(6);
                
                // Afficher un message de succès
                showNotification('Position GPS récupérée avec succès !', 'success');
            },
            function(error) {
                console.error('Erreur de géolocalisation:', error);
                showNotification('Impossible de récupérer votre position GPS', 'error');
            }
        );
    } else {
        showNotification('La géolocalisation n\'est pas supportée par votre navigateur', 'error');
    }
}

// Fonction pour afficher des notifications modernes
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `toast-modern ${type} transform translate-x-full transition-all duration-300`;
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    notification.innerHTML = `
        <div class="flex items-start">
            <div class="flex-shrink-0">
                <i class="fas ${icons[type]} text-lg"></i>
            </div>
            <div class="ml-3 flex-1">
                <p class="text-sm font-medium">${message}</p>
            </div>
            <div class="ml-4 flex-shrink-0">
                <button onclick="this.closest('.toast-modern').remove()" class="text-gray-400 hover:text-gray-600 transition-colors duration-200">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animation d'entrée
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Supprimer automatiquement
    setTimeout(() => {
        if (notification.parentElement) {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }, duration);
}

// Fonction pour afficher un toast de succès
function showSuccess(message, duration = 5000) {
    showNotification(message, 'success', duration);
}

// Fonction pour afficher un toast d'erreur
function showError(message, duration = 7000) {
    showNotification(message, 'error', duration);
}

// Fonction pour afficher un toast d'avertissement
function showWarning(message, duration = 6000) {
    showNotification(message, 'warning', duration);
}

// Fonction pour afficher un toast d'information
function showInfo(message, duration = 5000) {
    showNotification(message, 'info', duration);
}

// Fonction pour confirmer la suppression
function confirmDelete(message = 'Êtes-vous sûr de vouloir supprimer cet élément ?') {
    return confirm(message);
}

// Fonction pour formater les montants
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
    }).format(amount);
}

// Fonction pour formater les dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Initialisation de la carte Leaflet
function initMap(containerId, signalements = []) {
    const map = L.map(containerId).setView([14.6928, -17.4467], 13); // Dakar par défaut
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Ajouter les marqueurs pour chaque signalement
    signalements.forEach(signalement => {
        const marker = L.marker([signalement.lat, signalement.lng]).addTo(map);
        
        const popupContent = `
            <div class="p-2">
                <h3 class="font-semibold text-sm">${signalement.lieu}</h3>
                <p class="text-xs text-gray-600 mt-1">${signalement.description}</p>
                <div class="mt-2">
                    <span class="inline-block px-2 py-1 text-xs rounded-full ${
                        signalement.statut === 'nouveau' ? 'bg-red-100 text-red-800' :
                        signalement.statut === 'en_cours' ? 'bg-yellow-100 text-yellow-800' :
                        signalement.statut === 'pris_en_charge' ? 'bg-blue-100 text-blue-800' :
                        'bg-green-100 text-green-800'
                    }">
                        ${signalement.statut.replace('_', ' ')}
                    </span>
                    <span class="inline-block px-2 py-1 text-xs rounded-full ml-1 ${
                        signalement.urgence === 'critique' ? 'bg-red-100 text-red-800' :
                        signalement.urgence === 'elevee' ? 'bg-orange-100 text-orange-800' :
                        signalement.urgence === 'moyenne' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                    }">
                        ${signalement.urgence}
                    </span>
                </div>
                <p class="text-xs text-gray-500 mt-1">${signalement.date}</p>
            </div>
        `;
        
        marker.bindPopup(popupContent);
    });
    
    return map;
}

// Fonction pour charger les signalements via API
async function loadSignalements() {
    try {
        const response = await fetch('/api/signalements/');
        const signalements = await response.json();
        return signalements;
    } catch (error) {
        console.error('Erreur lors du chargement des signalements:', error);
        return [];
    }
}

// Fonction pour valider les formulaires
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('border-red-500');
            isValid = false;
        } else {
            field.classList.remove('border-red-500');
        }
    });
    
    return isValid;
}

// Fonction pour afficher un spinner de chargement
function showLoading(element) {
    element.innerHTML = '<div class="flex justify-center items-center"><i class="fas fa-spinner fa-spin text-2xl"></i></div>';
}

// Fonction pour masquer un spinner de chargement
function hideLoading(element, content) {
    element.innerHTML = content;
}

// Fonction pour créer un modal moderne
function createModal(title, content, actions = []) {
    const modal = document.createElement('div');
    modal.className = 'modal-modern';
    modal.innerHTML = `
        <div class="modal-content-modern">
            <div class="p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">${title}</h3>
                <div class="text-gray-600">${content}</div>
                <div class="flex justify-end space-x-3 mt-6">
                    ${actions.map(action => `
                        <button onclick="${action.onclick}" class="px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${action.class || 'bg-gray-100 text-gray-700 hover:bg-gray-200'}">
                            ${action.text}
                        </button>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    return modal;
}

// Fonction pour fermer un modal
function closeModal(modal) {
    modal.remove();
}

// Fonction pour afficher un modal de confirmation
function showConfirmModal(title, message, onConfirm, onCancel = null) {
    const modal = createModal(title, message, [
        {
            text: 'Annuler',
            class: 'bg-gray-100 text-gray-700 hover:bg-gray-200',
            onclick: `closeModal(this.closest('.modal-modern')); ${onCancel ? onCancel : ''}`
        },
        {
            text: 'Confirmer',
            class: 'bg-red-600 text-white hover:bg-red-700',
            onclick: `closeModal(this.closest('.modal-modern')); ${onConfirm}`
        }
    ]);
}

// Fonction pour créer un spinner de chargement
function createSpinner(size = 'md') {
    const spinner = document.createElement('div');
    spinner.className = `spinner-modern spinner-modern-${size}`;
    return spinner;
}

// Fonction pour afficher un état de chargement
function showLoading(element, text = 'Chargement...') {
    const originalContent = element.innerHTML;
    element.innerHTML = `
        <div class="flex items-center justify-center space-x-2">
            <div class="spinner-modern spinner-modern-md"></div>
            <span class="text-gray-600">${text}</span>
        </div>
    `;
    return originalContent;
}

// Fonction pour masquer l'état de chargement
function hideLoading(element, originalContent) {
    element.innerHTML = originalContent;
}

// Fonction pour créer un skeleton de chargement
function createSkeleton(type = 'text', count = 1) {
    const skeletons = [];
    for (let i = 0; i < count; i++) {
        const skeleton = document.createElement('div');
        switch (type) {
            case 'text':
                skeleton.className = 'loading-skeleton-text mb-2';
                break;
            case 'avatar':
                skeleton.className = 'loading-skeleton-avatar';
                break;
            case 'card':
                skeleton.className = 'loading-skeleton h-32 rounded-lg';
                break;
            default:
                skeleton.className = 'loading-skeleton h-4 rounded';
        }
        skeletons.push(skeleton);
    }
    return skeletons;
}

// Fonction pour animer les éléments au scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.fade-in, .slide-up');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, { threshold: 0.1 });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Fonction pour améliorer les formulaires
function enhanceForms() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Ajouter des classes modernes aux inputs
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (!input.classList.contains('form-control-modern')) {
                input.classList.add('form-control-modern');
            }
        });
        
        // Ajouter des classes modernes aux labels
        const labels = form.querySelectorAll('label');
        labels.forEach(label => {
            if (!label.classList.contains('form-label-modern')) {
                label.classList.add('form-label-modern');
            }
        });
        
        // Ajouter des classes modernes aux boutons
        const buttons = form.querySelectorAll('button, input[type="submit"]');
        buttons.forEach(button => {
            if (!button.classList.contains('btn-modern')) {
                button.classList.add('btn-modern', 'btn-primary-modern');
            }
        });
    });
}

// Fonction pour améliorer les cartes
function enhanceCards() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        if (!card.classList.contains('card-modern')) {
            card.classList.add('card-modern');
        }
    });
}

// Fonction pour améliorer les tableaux
function enhanceTables() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        if (!table.classList.contains('table-modern')) {
            table.classList.add('table-modern');
        }
    });
}

// Fonction pour ajouter des tooltips
function addTooltips() {
    const elements = document.querySelectorAll('[data-tooltip]');
    elements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip-modern';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
            
            setTimeout(() => tooltip.classList.add('show'), 100);
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip-modern');
            if (tooltip) tooltip.remove();
        });
    });
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Améliorer les composants
    enhanceForms();
    enhanceCards();
    enhanceTables();
    addTooltips();
    animateOnScroll();
    
    // Fermer le menu mobile automatiquement sur les liens
    const mobileLinks = document.querySelectorAll('#mobile-menu a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
    
    // Ajouter des animations aux éléments
    const animatedElements = document.querySelectorAll('.card, .btn, .nav-link');
    animatedElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});
