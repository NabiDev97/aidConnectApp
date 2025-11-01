#!/usr/bin/env bash
# Script de démarrage pour Render
# Exécute les migrations avant de démarrer le serveur

set -o errexit

echo "Exécution des migrations..."
python manage.py migrate --noinput

echo "Démarrage du serveur Gunicorn..."
exec gunicorn aidconnect.wsgi:application
