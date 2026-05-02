"""
Fichier WSGI pour PythonAnywhere.

Dans le tableau de bord PythonAnywhere → Web → WSGI configuration file,
remplacez TOUT le contenu par ce fichier (ou pointez vers lui).

⚠️  Adaptez le chemin /home/VOTRE_USERNAME/gestion_etudiants/ à votre compte.
"""
import sys
import os

# ── Adaptez ce chemin ──────────────────────────────────────────────────
project_home = '/home/VOTRE_USERNAME/gestion_etudiants'
# ───────────────────────────────────────────────────────────────────────

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Initialise la BDD au premier démarrage
from app import init_db, application
init_db()
