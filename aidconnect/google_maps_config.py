"""
Configuration pour l'API Google Maps
"""

# Clé API Google Maps (à remplacer par votre vraie clé)
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

# Configuration par défaut de la carte
DEFAULT_MAP_CENTER = {
    'lat': 14.6928,  # Dakar
    'lng': -17.4467
}

DEFAULT_ZOOM_LEVEL = 13

# Zones d'intervention au Sénégal
SENEGAL_ZONES = {
    'dakar': {
        'name': 'Dakar',
        'center': {'lat': 14.6928, 'lng': -17.4467},
        'zoom': 12
    },
    'thies': {
        'name': 'Thiès',
        'center': {'lat': 14.7894, 'lng': -16.9260},
        'zoom': 12
    },
    'kaolack': {
        'name': 'Kaolack',
        'center': {'lat': 14.1514, 'lng': -16.0736},
        'zoom': 12
    },
    'saint_louis': {
        'name': 'Saint-Louis',
        'center': {'lat': 16.0179, 'lng': -16.4896},
        'zoom': 12
    },
    'ziguinchor': {
        'name': 'Ziguinchor',
        'center': {'lat': 12.5831, 'lng': -16.2719},
        'zoom': 12
    },
    'tambacounda': {
        'name': 'Tambacounda',
        'center': {'lat': 13.7689, 'lng': -13.6673},
        'zoom': 12
    },
    'kolda': {
        'name': 'Kolda',
        'center': {'lat': 12.8833, 'lng': -14.9500},
        'zoom': 12
    },
    'matam': {
        'name': 'Matam',
        'center': {'lat': 15.6559, 'lng': -13.2554},
        'zoom': 12
    }
}

# Styles de carte personnalisés
CUSTOM_MAP_STYLES = [
    {
        "featureType": "poi",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    }
]
