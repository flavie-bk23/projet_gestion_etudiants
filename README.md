# UniGestion — Guide de déploiement

## Structure du projet

```
gestion_etudiants/
├── app.py              ← Application Flask (corrigée)
├── init_db.py          ← Script d'init de la BDD
├── wsgi.py             ← Config WSGI pour PythonAnywhere
├── requirements.txt
└── templates/
    ├── base.html
    ├── index.html
    ├── ajouter.html
    ├── liste.html
    └── stats.html
```

---

## Démarrage en local

```bash
# 1. Installer Flask
pip install flask

# 2. Initialiser la base de données (données de test incluses)
python init_db.py

# 3. Lancer l'app
python app.py
# → http://127.0.0.1:5000
```

---

## Déploiement sur PythonAnywhere

### 1. Uploader les fichiers
```bash
# Via l'onglet Files de PythonAnywhere, ou via Git :
git clone https://github.com/votre-repo gestion_etudiants
```

### 2. Créer un virtualenv et installer Flask
```bash
# Dans la console Bash de PythonAnywhere :
cd ~
python3 -m venv venv
source venv/bin/activate
pip install flask
```

### 3. Initialiser la base de données
```bash
cd ~/gestion_etudiants
python init_db.py
# ✅ La BDD est créée avec des données de test
```

### 4. Configurer la Web App
- Onglet **Web** → **Add a new web app**
- Choisir **Manual configuration** → Python 3.x
- **Source code** : `/home/VOTRE_USERNAME/gestion_etudiants`
- **WSGI configuration file** : Ouvrir et remplacer par le contenu de `wsgi.py`
  (en adaptant `VOTRE_USERNAME`)
- **Virtualenv** : `/home/VOTRE_USERNAME/venv`

### 5. Permissions BDD
```bash
chmod 664 ~/gestion_etudiants/database.db
```

### 6. Recharger l'app
Cliquer sur **Reload** dans l'onglet Web.

---

## Corrections appliquées

| # | Erreur | Solution |
|---|--------|----------|
| 1 | `no such column: moyenne` | Colonne ajoutée dans `CREATE TABLE` |
| 2 | `'sqlite3.Row' has no attribute 'moyenne'` | Corrigé par correction #1 |
| 3 | `ModuleNotFoundError: No module named 'app'` | `wsgi.py` avec chemin absolu correct |
| 4 | Double dossier imbriqué | Structure plate, un seul niveau |
| 5 | Push GitHub rejeté | Hors scope (problème Git) |
| 6 | Chemin BDD relatif | `BASE_DIR` + `os.path.join()` |
| 7 | Routes manquantes | Toutes les routes dans `app.py` |
| 8 | BDD vide sur PythonAnywhere | `init_db.py` insère des données de test |
| 9 | `mkvirtualenv: command not found` | `python3 -m venv venv` dans le guide |
| 10 | `tail: invalid context -- 5` | `tail -n 50` dans le guide |
| 11 | Permission refusée sur BDD | `chmod 664 database.db` dans le guide |
| 12 | Syntaxe bash avec `#` | `wsgi.py` propre sans commentaires inline |

---

## Fonctionnalités

- ✅ Accueil avec carte de tableau de bord
- ✅ Formulaire d'ajout avec barre de progression de moyenne
- ✅ Liste avec recherche en temps réel et suppression
- ✅ Statistiques avec 4 graphiques Chart.js
- ✅ Statistiques descriptives (moyenne, médiane, quartiles, skewness…)
- ✅ Classement avec médailles or/argent/bronze
- ✅ Design sombre moderne, responsive mobile
