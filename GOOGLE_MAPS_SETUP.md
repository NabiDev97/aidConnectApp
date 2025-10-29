# Configuration Google Maps pour AidConnect

## 🗺️ Intégration de Google Maps

AidConnect utilise l'API Google Maps pour permettre aux utilisateurs de sélectionner facilement la position des signalements.

## 🔑 Configuration de l'API Key

### 1. Obtenir une clé API Google Maps

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez les APIs suivantes :
   - **Maps JavaScript API**
   - **Places API** (pour l'autocomplétion des adresses)
   - **Geocoding API** (pour convertir les coordonnées en adresses)

### 2. Créer une clé API

1. Dans la console Google Cloud, allez dans "APIs & Services" > "Credentials"
2. Cliquez sur "Create Credentials" > "API Key"
3. Copiez votre clé API

### 3. Configurer la clé dans AidConnect

#### Option 1 : Variable d'environnement (Recommandé)

Créez un fichier `.env` à la racine du projet :

```env
GOOGLE_MAPS_API_KEY=votre_cle_api_ici
```

Puis modifiez `aidconnect/settings.py` :

```python
import os
from decouple import config

GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='')
```

#### Option 2 : Configuration directe

Modifiez le fichier `aidconnect/google_maps_config.py` :

```python
GOOGLE_MAPS_API_KEY = "votre_cle_api_ici"
```

### 4. Mettre à jour les templates

Dans tous les templates qui utilisent Google Maps, remplacez `YOUR_API_KEY` par votre clé :

```html
<script async defer src="https://maps.googleapis.com/maps/api/js?key=VOTRE_CLE_API&libraries=places&callback=initMap"></script>
```

## 🛠️ Fonctionnalités Google Maps

### Signalement avec carte interactive

- **Sélection de position** : Cliquez sur la carte pour marquer l'emplacement
- **Géolocalisation** : Bouton pour récupérer la position actuelle
- **Géocodage** : Conversion automatique des coordonnées en adresse
- **Marqueur draggable** : Glissez le marqueur pour ajuster la position

### Carte de visualisation

- **Marqueurs colorés** : Couleurs différentes selon le statut et l'urgence
- **Popups informatifs** : Détails du signalement au clic
- **Filtres dynamiques** : Filtrage en temps réel
- **Centrage automatique** : Ajustement de la vue selon les signalements

## 📍 Zones d'intervention configurées

Le système est pré-configuré pour les principales villes du Sénégal :

- **Dakar** (14.6928, -17.4467)
- **Thiès** (14.7894, -16.9260)
- **Kaolack** (14.1514, -16.0736)
- **Saint-Louis** (16.0179, -16.4896)
- **Ziguinchor** (12.5831, -16.2719)
- **Tambacounda** (13.7689, -13.6673)
- **Kolda** (12.8833, -14.9500)
- **Matam** (15.6559, -13.2554)

## 🔧 Personnalisation

### Styles de carte personnalisés

Modifiez `aidconnect/google_maps_config.py` pour personnaliser l'apparence :

```python
CUSTOM_MAP_STYLES = [
    {
        "featureType": "poi",
        "elementType": "labels",
        "stylers": [{"visibility": "off"}]
    }
]
```

### Centres de carte par défaut

Ajustez les coordonnées par défaut dans `google_maps_config.py` :

```python
DEFAULT_MAP_CENTER = {
    'lat': 14.6928,  # Votre latitude
    'lng': -17.4467  # Votre longitude
}
```

## 🚀 Déploiement

### Variables d'environnement en production

Assurez-vous de définir la variable d'environnement :

```bash
export GOOGLE_MAPS_API_KEY="votre_cle_api"
```

### Restrictions de l'API Key

Pour la sécurité, configurez des restrictions sur votre clé API :

1. **Restrictions d'application** : Limitez aux domaines de votre site
2. **Restrictions d'API** : Limitez aux APIs nécessaires
3. **Quotas** : Définissez des limites d'utilisation

## 🐛 Dépannage

### Erreurs courantes

1. **"Google Maps JavaScript API error"**
   - Vérifiez que votre clé API est correcte
   - Assurez-vous que l'API Maps JavaScript est activée

2. **"This page can't load Google Maps correctly"**
   - Vérifiez les restrictions de domaine
   - Assurez-vous que le domaine est autorisé

3. **"Geocoding API error"**
   - Activez l'API Geocoding dans Google Cloud Console
   - Vérifiez les quotas d'utilisation

### Mode développement

Pour le développement local, vous pouvez utiliser `localhost` dans les restrictions de domaine.

## 📊 Monitoring

Surveillez l'utilisation de votre API dans Google Cloud Console :

- **APIs & Services** > **Quotas**
- **APIs & Services** > **Credentials** > Votre clé API

## 💰 Coûts

Google Maps propose un crédit gratuit mensuel :
- **28 500 chargements de carte** par mois
- **40 000 requêtes de géocodage** par mois

Au-delà, les tarifs s'appliquent. Consultez la [page de tarification](https://cloud.google.com/maps-platform/pricing) pour plus de détails.

---

**Note** : Gardez votre clé API secrète et ne la commitez jamais dans votre dépôt Git !
