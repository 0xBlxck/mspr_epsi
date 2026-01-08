# Répartition des tâches - 5 étudiants

## Personne 1 : Setup & Config
- Crée la structure du projet
- Configure les dépendances (requirements.txt)
- Prépare config.json avec les IP

## Personne 2 : Module Diagnostic
- Code la vérification des serveurs (ping, AD, DNS, MySQL)
- Teste que ça marche
- Fichier : `modules/diagnostic.py`

## Personne 3 : Module Sauvegarde
- Code l'export MySQL
- Code l'export CSV
- Fichier : `modules/backup.py`

## Personne 4 : Module Audit
- Code le scan réseau
- Code la détection d'obsolescence
- Fichier : `modules/audit.py` + utils

## Personne 5 : Interface & Doc
- Menu CLI (main.py)
- Interface graphique (gui.py)
- Documentation (README.md)

---

## C'est tout !

Chacun code sa partie, tout s'assemble, ça marche.
