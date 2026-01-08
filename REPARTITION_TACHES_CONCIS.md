# Répartition des tâches - NTL-SysToolbox

## Personne 1 : Setup & Architecture
**Quoi** : Structure du projet, config, dossiers
**Fichiers** : `config/config.json`, `requirements.txt`, `.gitignore`
**Pourquoi JSON ?** Facile à modifier pour un admin, pas de code requis

## Personne 2 : Module Diagnostic
**Quoi** : Tester les serveurs (ping, AD, DNS, MySQL, CPU/RAM/Disque)
**Fichier** : `modules/diagnostic.py`
**Dépendances** : `psutil` (stats système), `mysql-connector-python`
**Pourquoi psutil ?** Marche identique Windows/Linux/Mac, fiable

## Personne 3 : Module Sauvegarde
**Quoi** : Exporter la BD MySQL en SQL + CSV avec vérification d'intégrité
**Fichier** : `modules/backup.py`
**Dépendances** : `mysql-connector-python`
**Pourquoi deux formats ?** SQL pour restauration, CSV pour audit lisible

## Personne 4 : Module Audit
**Quoi** : Scanner le réseau, détecter OS, comparer avec EOL database
**Fichiers** : `modules/audit.py`, `data/eol_database.json`
**Dépendances** : `python-nmap`
**Pourquoi Nmap ?** Standard admin système, détecte OS précisément

## Personne 5 : Interface & Documentation
**Quoi** : Menu CLI + Interface graphique + Documentation
**Fichiers** : `main.py`, `gui.py`, `README.md`
**Dépendances** : `tkinter` (inclus avec Python), `logging`
**Pourquoi Tkinter ?** Pré-installé, identique sur tous les OS

---

## Pourquoi Python ?
- Multiplateforme (Windows, Linux, macOS)
- Parfait pour admin système (bonnes librairies)
- Facile à apprendre + à maintenir
- CLI + GUI dans le même langage

**Alternatives rejetées** : C# (Windows only), Bash (trop faible), Go/Node (overkill)

---

## Architecture globale
```
Personne 1 (Setup) → Infrastructure commune
  ├── Personne 2 (Diagnostic) → teste serveurs
  ├── Personne 3 (Backup) → sauvegarde BD
  ├── Personne 4 (Audit) → scanne réseau
  └── Personne 5 (Interface) → affiche résultats
  
→ NTL-SysToolbox fonctionnel
```

**Avantage** : Chacun code seul, pas de conflits. Modules réutilisables.
