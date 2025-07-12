#!/usr/bin/env bash
# Exit on error
set -o errexit

# Installe les dépendances depuis requirements.txt
pip install -r requirements.txt

# Collecte les fichiers statiques pour la production
python manage.py collectstatic --no-input

# Applique les migrations de la base de données
python manage.py migrate
