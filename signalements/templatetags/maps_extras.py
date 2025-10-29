from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def google_maps_api_key():
    """Retourne la clé API Google Maps depuis les settings"""
    return getattr(settings, 'GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY')

@register.simple_tag
def google_maps_script():
    """Génère le script Google Maps avec la clé API"""
    api_key = google_maps_api_key()
    return f'https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=places,marker&callback=initMap'
