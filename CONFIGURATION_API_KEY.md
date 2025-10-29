# 🔑 Configuration de la Clé API Google Maps

## ⚠️ Problème Actuel

Vous voyez l'erreur `InvalidKeyMapError` car la clé API n'est pas configurée. Voici comment la résoudre :

## 🚀 Solution Rapide

### 1. Obtenir une clé API Google Maps

1. **Allez sur [Google Cloud Console](https://console.cloud.google.com/)**
2. **Créez un projet** ou sélectionnez un projet existant
3. **Activez les APIs nécessaires** :
   - Maps JavaScript API
   - Places API
   - Geocoding API
4. **Créez une clé API** dans "APIs & Services" > "Credentials"

### 2. Configurer la clé dans AidConnect

#### Option A : Modification directe (Rapide)

Modifiez le fichier `aidconnect/settings.py` :

```python
# Google Maps Configuration
GOOGLE_MAPS_API_KEY = 'VOTRE_VRAIE_CLE_API_ICI'
```

#### Option B : Variable d'environnement (Recommandé)

1. **Créez un fichier `.env`** à la racine du projet :
```env
GOOGLE_MAPS_API_KEY=votre_cle_api_ici
```

2. **Modifiez `aidconnect/settings.py`** :
```python
import os
from decouple import config

# Google Maps Configuration
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='YOUR_API_KEY')
```

### 3. Redémarrer le serveur

```bash
# Arrêter le serveur (Ctrl+C)
# Puis relancer
python manage.py runserver
```

## 🔧 Corrections Appliquées

### ✅ Marker Modernisé
- **Avant** : `google.maps.Marker` (déprécié)
- **Après** : `google.maps.marker.AdvancedMarkerElement` (moderne)

### ✅ Bibliothèques Mises à Jour
- **Ajouté** : `libraries=places,marker` pour les nouveaux marqueurs
- **Événements** : `gmpDragend` au lieu de `dragend`

### ✅ Gestion Centralisée
- **Template tags** : `{% google_maps_script %}` pour la clé API
- **Settings** : Configuration centralisée dans `settings.py`

## 🧪 Test de la Configuration

1. **Accédez à** : http://127.0.0.1:8000/signaler/
2. **Vérifiez** : La carte Google Maps s'affiche sans erreur
3. **Testez** : Cliquez sur la carte pour marquer une position
4. **Vérifiez** : Le marqueur est draggable et l'adresse se remplit

## 🛡️ Sécurité

### Restrictions de la Clé API

1. **Restrictions d'application** :
   - Type : HTTP referrers
   - Sites autorisés : `localhost:8000/*`, `127.0.0.1:8000/*`

2. **Restrictions d'API** :
   - Maps JavaScript API
   - Places API
   - Geocoding API

3. **Quotas** :
   - Définissez des limites pour éviter les coûts inattendus

## 💰 Coûts

- **Gratuit** : 28,500 chargements de carte/mois
- **Gratuit** : 40,000 requêtes de géocodage/mois
- **Au-delà** : Tarifs payants (voir [Google Maps Pricing](https://cloud.google.com/maps-platform/pricing))

## 🐛 Dépannage

### Erreur "InvalidKeyMapError"
- ✅ Vérifiez que la clé API est correcte
- ✅ Vérifiez que l'API Maps JavaScript est activée
- ✅ Vérifiez les restrictions de domaine

### Erreur "This page can't load Google Maps"
- ✅ Vérifiez que le domaine est autorisé dans les restrictions
- ✅ Vérifiez que la clé API a les bonnes permissions

### Carte ne s'affiche pas
- ✅ Vérifiez la console du navigateur pour les erreurs
- ✅ Vérifiez que la clé API est bien configurée
- ✅ Vérifiez la connexion internet

## 📝 Exemple de Configuration Complète

```python
# aidconnect/settings.py
import os
from decouple import config

# Google Maps Configuration
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='YOUR_API_KEY')

# Ou directement (moins sécurisé)
# GOOGLE_MAPS_API_KEY = 'AIzaSyBvOkBwv90WRFQj4Qj4Qj4Qj4Qj4Qj4Qj4Q'
```

```env
# .env (à la racine du projet)
GOOGLE_MAPS_API_KEY=AIzaSyBvOkBwv90WRFQj4Qj4Qj4Qj4Qj4Qj4Qj4Q
```

---

**🎯 Une fois configurée, votre carte Google Maps fonctionnera parfaitement !**
