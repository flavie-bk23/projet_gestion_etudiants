from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Chemin absolu vers la base de données (corrige l'erreur de chemin)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_db():
    """Connexion à la base de données avec chemin absolu."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialise la base de données avec la colonne moyenne."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nom      TEXT    NOT NULL,
            prenom   TEXT    NOT NULL,
            age      INTEGER,
            sexe     TEXT,
            filiere  TEXT,
            niveau   TEXT,
            moyenne  REAL    DEFAULT 0.0
        )
    """)
    conn.commit()

    # Insérer des données de test si la table est vide
    count = conn.execute("SELECT COUNT(*) FROM etudiants").fetchone()[0]
    if count == 0:
        test_data = [
            ("Mbarga", "Paul",      21, "Homme",  "Informatique",   "L3", 16.5),
            ("Ngo",    "Marie",     20, "Femme",  "Informatique",   "L2", 14.2),
            ("Ateba",  "Jean",      22, "Homme",  "Mathématiques",  "L3", 12.8),
            ("Bello",  "Fatouma",   19, "Femme",  "Physique",       "L1",  9.5),
            ("Manga",  "Eric",      23, "Homme",  "Informatique",   "L3", 18.0),
            ("Essono", "Claire",    21, "Femme",  "Mathématiques",  "L2", 11.3),
            ("Ondo",   "Christian", 20, "Homme",  "Physique",       "L2", 13.7),
            ("Ella",   "Sophie",    22, "Femme",  "Informatique",   "L1",  8.4),
            ("Mvondo", "Alexis",    24, "Homme",  "Mathématiques",  "L3", 15.9),
            ("Abena",  "Rachel",    20, "Femme",  "Physique",       "L1",  7.2),
            ("Fouda",  "Patrick",   21, "Homme",  "Informatique",   "L2", 17.5),
            ("Zang",   "Pauline",   19, "Femme",  "Mathématiques",  "L1", 10.6),
        ]
        conn.executemany(
            "INSERT INTO etudiants (nom,prenom,age,sexe,filiere,niveau,moyenne) VALUES (?,?,?,?,?,?,?)",
            test_data
        )
        conn.commit()
    conn.close()


# ── ROUTES ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) as n FROM etudiants").fetchone()["n"]
    conn.close()
    return render_template("index.html", total=total)


@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        try:
            nom     = request.form.get("nom", "").strip()
            prenom  = request.form.get("prenom", "").strip()
            age     = request.form.get("age", "0").strip() or "0"
            sexe    = request.form.get("sexe", "")
            filiere = request.form.get("filiere", "").strip()
            niveau  = request.form.get("niveau", "")
            moyenne = request.form.get("moyenne", "0").strip() or "0"

            age     = int(age)
            moyenne = float(moyenne)

            conn = get_db()
            conn.execute(
                "INSERT INTO etudiants (nom,prenom,age,sexe,filiere,niveau,moyenne) VALUES (?,?,?,?,?,?,?)",
                (nom, prenom, age, sexe, filiere, niveau, moyenne)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("liste"))
        except Exception as e:
            return render_template("ajouter.html", error=str(e))
    return render_template("ajouter.html", error=None)


@app.route("/liste")
def liste():
    conn = get_db()
    etudiants = conn.execute("SELECT * FROM etudiants ORDER BY nom, prenom").fetchall()
    conn.close()
    return render_template("liste.html", etudiants=etudiants)


@app.route("/supprimer/<int:id>")
def supprimer(id):
    conn = get_db()
    conn.execute("DELETE FROM etudiants WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("liste"))


@app.route("/stats")
def stats():
    conn = get_db()

    total         = conn.execute("SELECT COUNT(*) as total FROM etudiants").fetchone()
    moyenne       = conn.execute("SELECT AVG(moyenne) as moy FROM etudiants").fetchone()
    filieres      = conn.execute(
        "SELECT filiere, AVG(moyenne) as moy, COUNT(*) as nb FROM etudiants GROUP BY filiere ORDER BY moy DESC"
    ).fetchall()
    meilleure_filiere = conn.execute(
        "SELECT filiere, AVG(moyenne) as moy FROM etudiants GROUP BY filiere ORDER BY moy DESC LIMIT 1"
    ).fetchone()
    pire_filiere  = conn.execute(
        "SELECT filiere, AVG(moyenne) as moy FROM etudiants GROUP BY filiere ORDER BY moy ASC LIMIT 1"
    ).fetchone()
    classement    = conn.execute(
        "SELECT nom, prenom, moyenne, filiere, niveau FROM etudiants ORDER BY moyenne DESC"
    ).fetchall()
    conn.close()

    return render_template("stats.html",
        total=total,
        moyenne=moyenne,
        filieres=filieres,
        meilleure_filiere=meilleure_filiere,
        pire_filiere=pire_filiere,
        classement=classement,
    )


# ── WSGI & DEV ────────────────────────────────────────────────────────

# Variable WSGI pour PythonAnywhere
application = app

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
