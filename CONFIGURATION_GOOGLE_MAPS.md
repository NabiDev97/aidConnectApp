# 🗺️ Configuration Google Maps - AidConnect

## ⚠️ Problème Actuel

L'erreur `TemplateSyntaxError` est résolue, mais vous devez configurer votre clé API Google Maps pour utiliser la carte interactive.

## 🚀 Solutions Disponibles

### Option 1 : Template Simple (Actuel)
- ✅ **Fonctionne immédiatement** sans configuration
- ✅ **Formulaire complet** avec géolocalisation GPS
- ✅ **Interface moderne** avec Tailwind CSS
- ❌ Pas de carte interactive

### Option 2 : Template avec Google Maps
- ✅ **Carte interactive** pour sélection visuelle
- ✅ **Géocodage automatique** des adresses
- ✅ **Interface moderne** avec marqueurs
- ⚠️ Nécessite une clé API Google Maps

## 🔧 Configuration Google Maps (Option 2)

### 1. Obtenir une clé API

1. **Allez sur [Google Cloud Console](https://console.cloud.google.com/)**
2. **Créez un projet** ou sélectionnez un projet existant
3. **Activez les APIs** :
   - Maps JavaScript API
   - Places API
   - Geocoding API
4. **Créez une clé API** dans "APIs & Services" > "Credentials"

### 2. Configurer la clé

Modifiez `aidconnect/settings.py` :

```python
# Google Maps Configuration
GOOGLE_MAPS_API_KEY = 'VOTRE_VRAIE_CLE_API_ICI'
```

### 3. Activer Google Maps

Modifiez `signalements/views.py` ligne 53 :

```python
# Pour utiliser Google Maps
return render(request, 'signalements/signaler_google_maps.html', context)

# Pour utiliser le template simple (actuel)
return render(request, 'signalements/signaler_simple.html', context)
```

## 📱 Fonctionnalités Actuelles

### ✅ Template Simple (Actif)
- **Formulaire complet** avec tous les champs
- **Géolocalisation GPS** via bouton
- **Upload de photos** avec prévisualisation
- **Validation** des champs obligatoires
- **Interface responsive** mobile/desktop

### ✅ Template Google Maps (Disponible)
- **Carte interactive** pour sélection de position
- **Marqueurs draggables** modernes
- **Géocodage automatique** des adresses
- **Centrage intelligent** sur Dakar
- **Position actuelle** en un clic

## 🎯 Recommandation

### Pour le développement :
- **Utilisez le template simple** (actuel) pour tester rapidement
- **Configurez Google Maps** quand vous êtes prêt pour la production

### Pour la production :
- **Configurez Google Maps** pour une meilleure expérience utilisateur
- **Testez** avec votre vraie clé API

## 🔄 Basculer entre les Templates

### Utiliser le template simple :
```python
# Dans signalements/views.py ligne 53
return render(request, 'signalements/signaler_simple.html', context)
```

### Utiliser Google Maps :
```python
# Dans signalements/views.py ligne 53
return render(request, 'signalements/signaler_google_maps.html', context)
```

## 🧪 Test de l'Application

1. **Accédez à** : http://127.0.0.1:8000/signaler/
2. **Vérifiez** : Le formulaire s'affiche sans erreur
3. **Testez** : Remplissez et soumettez un signalement
4. **Vérifiez** : Le signalement est enregistré en base

## 📋 Prochaines Étapes

1. **Testez** l'interface de signalement actuelle
2. **Configurez** Google Maps si souhaité
3. **Personnalisez** les champs selon vos besoins
4. **Déployez** en production

---

**🎯 Votre application fonctionne maintenant parfaitement avec le template simple !**
