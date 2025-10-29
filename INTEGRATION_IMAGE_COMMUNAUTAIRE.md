# Intégration de l'Image Communautaire

## Description de l'image
L'image proposée représente une scène de solidarité communautaire au Sénégal, montrant :
- Des femmes en t-shirts bleu clair avec un logo d'organisation
- Une interaction humaine directe et bienveillante
- Un environnement urbain modeste mais chaleureux
- Des gestes de soutien et d'entraide

## Intégration dans l'interface

### 1. Section Hero (En-tête)
- **Emplacement** : `templates/signalements/home.html` (lignes 8-35)
- **Utilisation** : Image de fond avec overlay pour créer un effet visuel impactant
- **Style** : Opacité réduite (20%) avec gradient bleu par-dessus

### 2. Section "Notre Mission"
- **Emplacement** : `templates/signalements/home.html` (lignes 37-86)
- **Utilisation** : Image principale avec légende et effet de gradient
- **Style** : Image complète avec ombre et texte superposé

### 3. Section Témoignages
- **Emplacement** : `templates/signalements/home.html` (lignes 224-235)
- **Utilisation** : Image d'introduction aux témoignages
- **Style** : Image avec texte superposé et gradient

## Instructions pour ajouter l'image réelle

### Étape 1 : Préparer l'image
1. Nommer l'image : `community_support.jpg`
2. Dimensions recommandées : 1200x800 pixels minimum
3. Format : JPG ou PNG
4. Taille : Moins de 2MB pour un chargement rapide

### Étape 2 : Remplacer le fichier
1. Supprimer le fichier actuel : `static/images/community_support.jpg`
2. Copier votre image dans : `static/images/community_support.jpg`

### Étape 3 : Vérifier l'intégration
1. Démarrer le serveur Django : `python manage.py runserver`
2. Visiter la page d'accueil : `http://localhost:8000`
3. Vérifier que l'image s'affiche correctement dans les 3 sections

## Avantages de cette intégration

### Impact visuel
- **Authenticité** : L'image reflète la réalité sénégalaise
- **Émotion** : Crée une connexion émotionnelle avec les utilisateurs
- **Crédibilité** : Montre l'engagement communautaire réel

### Amélioration UX
- **Navigation** : L'image guide l'œil vers les actions importantes
- **Compréhension** : Illustre concrètement la mission d'AidConnect
- **Engagement** : Encourage la participation des utilisateurs

### Cohérence visuelle
- **Couleurs** : S'harmonise avec la palette bleue du site
- **Style** : S'intègre naturellement dans le design moderne
- **Message** : Renforce le thème de solidarité communautaire

## Personnalisation possible

### Ajustements CSS
```css
/* Modifier l'opacité de l'image hero */
.hero-image {
    opacity: 0.3; /* Au lieu de 0.2 */
}

/* Ajuster la hauteur de l'image dans la section mission */
.mission-image {
    height: 400px; /* Au lieu de 384px (h-96) */
}
```

### Responsive Design
L'image s'adapte automatiquement aux différentes tailles d'écran grâce aux classes Tailwind CSS utilisées.

## Support technique

Pour toute question sur l'intégration de l'image :
- Vérifier que le fichier est bien dans `static/images/`
- S'assurer que Django collecte les fichiers statiques : `python manage.py collectstatic`
- Vérifier les permissions de lecture du fichier
