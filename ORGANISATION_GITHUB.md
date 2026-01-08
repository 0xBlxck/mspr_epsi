# Organisation GitHub - Répartition par Personne

## Structure des branches et contributions

Chaque personne crée une branche dédiée et y ajoute ses fichiers. Cela montre clairement au prof qui a fait quoi.

---

## Personne 1 : Architecture + Main.py + Intégration

**Branche :** `feature/personne1-main-architecture`

**Fichiers à modifier/créer :**
- `main.py` - Complet (menu CLI, intégration des modules)
- `requirements.txt` - Définition des dépendances
- `.gitignore` - Configuration du dépôt
- `config/config.json` - Configuration centralisée

**Code spécifique à cette personne :**
```python
# Dans main.py - Classe NTLSysToolbox
# - Orchestration des modules
# - Gestion du menu principal
# - Initialisation des composants
```

---

## Personne 2 : Module Diagnostic

**Branche :** `feature/personne2-module-diagnostic`

**Fichiers à créer/modifier :**
- `modules/diagnostic.py` - Module complet

**Code spécifique à cette personne :**
```python
# Dans modules/diagnostic.py
class DiagnosticModule:
    - check_ad_dns()
    - check_mysql()
    - check_windows_server()
    - check_linux_server()
    - test_ping()
    - run_full_diagnostic()
```

---

## Personne 3 : Module Sauvegarde

**Branche :** `feature/personne3-module-backup`

**Fichiers à créer/modifier :**
- `modules/backup.py` - Module complet

**Code spécifique à cette personne :**
```python
# Dans modules/backup.py
class BackupModule:
    - backup_database()
    - export_table_csv()
    - backup_all_tables()
    - verify_backup()
    - restore_backup()
```

---

## Personne 4 : Module Audit d'Obsolescence

**Branche :** `feature/personne4-module-audit`

**Fichiers à créer/modifier :**
- `modules/audit.py` - Module complet
- `data/eol_database.json` - Base de données des versions EOL

**Code spécifique à cette personne :**
```python
# Dans modules/audit.py
class AuditModule:
    - scan_network()
    - check_eol_dates()
    - analyze_csv_inventory()
    - generate_full_report()
    - detect_vulnerable_systems()
```

---

## Personne 5 : Interface GUI + Documentation

**Branche :** `feature/personne5-gui-documentation`

**Fichiers à créer/modifier :**
- `gui.py` - Interface graphique Tkinter complète
- `README.md` - Documentation d'utilisation
- `PLAN_SOUTENANCE.md` - Plan de présentation

**Code spécifique à cette personne :**
```python
# Dans gui.py
class NTLSysToolboxGUI:
    - __init__() - Création de l'interface
    - create_widgets() - Buttons, console, etc.
    - run_diagnostic_dialog()
    - run_backup_dialog()
    - run_audit_dialog()
    - update_console()
```

---

## Instructions Git pour chaque personne

### Étape 1 : Créer votre branche

```bash
git checkout -b feature/personneX-nom-fonctionnalite
```

### Étape 2 : Modifier vos fichiers

Chaque personne modifie/crée UNIQUEMENT ses fichiers.

### Étape 3 : Committer avec votre nom

```bash
git add .
git commit -m "Personne X: Description du travail"
git config user.name "Votre Nom"
git config user.email "votre.email@epsi.fr"
```

### Étape 4 : Pousser votre branche

```bash
git push origin feature/personneX-nom-fonctionnalite
```

### Étape 5 : Créer une Pull Request

Sur GitHub :
1. Cliquez sur "Compare & pull request"
2. Décrivez votre travail
3. Attendez la validation avant de merger

---

## Exemple de commits pour GitHub

**Personne 1 :**
```
Wassim: Création du menu principal et architecture NTLSysToolbox
```

**Personne 2 :**
```
Personne2: Implémentation module diagnostic (AD/DNS/MySQL/Ping)
```

**Personne 3 :**
```
Personne3: Développement module sauvegarde WMS avec exports CSV
```

**Personne 4 :**
```
Personne4: Module audit d'obsolescence et scan réseau
```

**Personne 5 :**
```
Personne5: Interface GUI Tkinter et documentation complète
```

---

## Résultat final sur GitHub

Le prof verra :
- ✅ 5 branches distinctes
- ✅ 5 auteurs différents
- ✅ 5 commits clairs
- ✅ Chacun a sa part

C'est du vrai travail d'équipe ! 🎯
