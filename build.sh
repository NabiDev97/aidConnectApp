#!/usr/bin/env bash
# Script de build pour Render

set -o errexit

# Installer les dépendances
pip install -r requirements.txt

# Exécuter les migrations
python manage.py migrate --noinput

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
