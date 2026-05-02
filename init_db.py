"""
Script d'initialisation de la base de données.
Exécuter AVANT de lancer l'application :
    python init_db.py
"""
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DB_PATH)

conn.execute("DROP TABLE IF EXISTS etudiants")
conn.execute("""
    CREATE TABLE etudiants (
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
print(f"✅ Base initialisée avec {len(test_data)} étudiants → {DB_PATH}")
