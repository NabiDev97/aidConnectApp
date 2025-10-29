# AidConnect - Plateforme de Soutien aux Malades Mentaux

## 🎯 Description du Projet

AidConnect est une plateforme web solidaire développée pour le Sénégal, permettant de signaler des malades mentaux dans les rues, d'alerter les associations locales et de faciliter les dons pour soutenir les actions d'aide.

## ✨ Fonctionnalités Principales

### 🔍 Signalements
- **Signalement rapide** : Formulaire simple pour signaler un cas
- **Géolocalisation** : Récupération automatique des coordonnées GPS
- **Photos** : Ajout d'images pour mieux décrire la situation
- **Niveaux d'urgence** : Classification des cas (faible, moyenne, élevée, critique)
- **Anonymat** : Possibilité de signaler sans compte utilisateur

### 🏥 Associations
- **Inscription** : Les associations peuvent s'inscrire sur la plateforme
- **Tableau de bord** : Gestion des signalements assignés
- **Besoins urgents** : Publication de besoins spécifiques
- **Zones d'intervention** : Définition des zones géographiques couvertes

### 💝 Dons
- **Dons multiples** : Argent, médicaments, vêtements, nourriture
- **Campagnes** : Création de campagnes de collecte
- **Transparence** : Suivi des dons et de leur utilisation
- **Mobile Money** : Intégration des moyens de paiement locaux

### 🗺️ Carte Interactive
- **Visualisation** : Carte en temps réel des signalements
- **Filtres** : Par statut, urgence, zone géographique
- **Statistiques** : Données en temps réel sur les signalements

## 🛠️ Technologies Utilisées

- **Backend** : Django 5.2.4
- **Frontend** : HTML5, CSS3, JavaScript (ES6+)
- **Framework CSS** : Tailwind CSS
- **Base de données** : SQLite (développement)
- **Cartes** : Leaflet.js
- **Icônes** : Font Awesome
- **Formulaires** : Django Crispy Forms avec Tailwind

## 📋 Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Git

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd Projet_Soutient_Maldes_Mentaux
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

**Windows :**
```bash
venv\Scripts\activate
```

**Linux/Mac :**
```bash
source venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 5. Configurer la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur de développement
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : http://127.0.0.1:8000/

## 📁 Structure du Projet

```
aidconnect/
├── aidconnect/           # Configuration principale
│   ├── settings.py       # Paramètres Django
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # Configuration WSGI
├── signalements/         # Application signalements
│   ├── models.py        # Modèles Signalement, Intervention
│   ├── views.py         # Vues pour signalements
│   ├── forms.py         # Formulaires de signalement
│   ├── admin.py         # Interface d'administration
│   └── urls.py          # URLs des signalements
├── associations/         # Application associations
│   ├── models.py        # Modèles Association, BesoinUrgent
│   ├── views.py         # Vues pour associations
│   ├── forms.py         # Formulaires d'association
│   ├── admin.py         # Interface d'administration
│   └── urls.py          # URLs des associations
├── dons/                # Application dons
│   ├── models.py        # Modèles Don, CampagneDon, HistoriqueDon
│   ├── views.py         # Vues pour dons
│   ├── forms.py         # Formulaires de don
│   ├── admin.py         # Interface d'administration
│   └── urls.py          # URLs des dons
├── templates/           # Templates HTML
│   ├── base/           # Template de base
│   ├── signalements/   # Templates signalements
│   ├── associations/   # Templates associations
│   └── dons/           # Templates dons
├── static/             # Fichiers statiques
│   ├── css/           # Styles CSS
│   ├── js/            # JavaScript
│   └── images/        # Images
├── media/             # Fichiers uploadés
├── requirements.txt   # Dépendances Python
└── README.md         # Documentation
```

## 👥 Types d'Utilisateurs

### 1. Citoyens
- Signaler des cas de malades mentaux
- Faire des dons
- Consulter les informations publiques

### 2. Associations
- Gérer les signalements assignés
- Publier des besoins urgents
- Suivre les dons reçus
- Gérer les campagnes

### 3. Donateurs
- Faire des dons en ligne
- Suivre l'utilisation de leurs dons
- Participer aux campagnes

### 4. Administrateurs
- Gérer la plateforme
- Modérer les contenus
- Vérifier les associations
- Accéder aux statistiques

## 🔧 Configuration

### Variables d'environnement
Créer un fichier `.env` à la racine du projet :

```env
SECRET_KEY=votre_clé_secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuration de production
Pour la production, modifier `settings.py` :
- `DEBUG = False`
- Configurer une base de données PostgreSQL/MySQL
- Configurer les fichiers statiques avec WhiteNoise
- Ajouter les domaines autorisés

## 📊 Modèles de Données

### Signalement
- Lieu, description, photo
- Coordonnées GPS, adresse
- Niveau d'urgence, statut
- Utilisateur, contact téléphone

### Association
- Nom, type, zone d'intervention
- Contact, adresse, site web
- Comptes pour dons (Mobile Money, PayPal)
- Statut de vérification

### Don
- Type, description, montant/quantité
- Donateur, association destinataire
- Statut, commentaires
- Informations de remise

## 🚀 Déploiement

### Heroku
1. Créer un `Procfile`
2. Configurer les variables d'environnement
3. Déployer avec Git

### VPS
1. Installer Nginx, PostgreSQL
2. Configurer Gunicorn
3. Configurer les fichiers statiques
4. Configurer SSL

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Contact

- **Email** : contact@aidconnect.sn
- **Site web** : https://aidconnect.sn
- **GitHub** : https://github.com/aidconnect

## 🙏 Remerciements

- Associations de santé mentale du Sénégal
- Communauté Django
- Contributeurs open source
- Bénévoles et testeurs

---

**AidConnect** - Ensemble, changeons les choses pour les malades mentaux au Sénégal 🇸🇳
