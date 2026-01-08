# Répartition des tâches et choix technologiques - NTL-SysToolbox

## Contexte global

NTL (NordTransit Logistics) gère 5 sites (Lille, Lens, Valenciennes, Arras + cross-dock saisonnier). Chaque site a son infrastructure avec serveurs, bases de données, et systèmes critiques. L'outil doit pouvoir diagnostiquer les problèmes **rapidement**, sauvegarder les données **sans perte**, et identifier les systèmes **obsolètes**.

**Défi** : Un outil qui marche sur Windows ET Linux, qu'un admin peut lancer sans être développeur.

**Solution** : Python (langage universel) + Interface graphique simple + Modules indépendants.

---

## Personne 1 : Setup & Configuration

### Tâches exactes
- Créer la structure des dossiers du projet
- Rédiger `requirements.txt` avec les dépendances
- Créer et remplir `config/config.json` avec toute l'infra NTL
- Créer les dossiers `output/`, `data/`, `utils/`, `modules/`
- Initialiser le projet Git avec `.gitignore`

### Fichiers concernés
```
config/config.json          ← Configuration complète de NTL
requirements.txt            ← Liste des librairies Python
.gitignore                  ← Quoi ignorer dans Git
```

### Pourquoi ces choix ?

**JSON pour la config** : 
- Facile à lire et modifier pour un admin (pas de codage requis)
- Pas besoin d'une vraie base de données
- Portable, pas de dépendance système

**Hiérarchie des dossiers** :
- Chaque module indépendant facilite le travail en parallèle
- Les logs, backups, et rapports séparés = facile à archiver
- Clair pour le jury = vous aviez une vision d'ensemble

### Exemple de config
```json
"servers": {
  "DC01": "192.168.10.10",
  "WMS-DB": "192.168.10.21"
}
```
Juste modifier cette ligne = ça teste une autre IP. C'est ça que l'admin veut.

---

## Personne 2 : Module Diagnostic

### Tâches exactes
- Vérifier que les serveurs répondent au ping
- Tester la connexion au Domain Controller (AD)
- Vérifier le DNS
- Se connecter à la base MySQL et tester sa réactivité
- Récupérer les stats système (CPU, RAM, disque) sur Windows/Linux

### Fichier concerné
```
modules/diagnostic.py       ← Tout le code de diagnostic
```

### Dépendances utilisées
- `psutil` : Récupère les stats système (mémoire, CPU, disque)
- `mysql-connector-python` : Se connecte à MySQL et lance des requêtes
- Librairies Python standard : `subprocess` (pour le ping), `socket` (pour DNS)

### Pourquoi psutil ?
- Alternative à faire des commandes système complexes
- Fonctionne identique sur Windows, Linux, macOS
- Pas besoin d'être root/admin pour lire les infos
- Résultats fiables et standardisés

### Exemple de ce que le module retourne
```
{
  "ping_DC01": "OK - 2ms",
  "mysql_connection": "OK - 15ms",
  "cpu_usage": "45%",
  "ram_total": "16 GB",
  "ram_used": "7.2 GB",
  "disk_free": "250 GB"
}
```

L'admin sait **tout de suite** si c'est bloquant ou non.

---

## Personne 3 : Module Sauvegarde

### Tâches exactes
- Se connecter à la base MySQL du WMS
- Exporter COMPLÈTEMENT la base de données en fichier `.sql`
- Exporter aussi les tables critiques en `.csv` (pour lisibilité)
- Vérifier que l'export n'est pas corrompu (checksum)
- Sauvegarder tout dans `output/backups/` avec un nom horodaté

### Fichier concerné
```
modules/backup.py           ← Tout le code de backup
```

### Dépendances utilisées
- `mysql-connector-python` : Connexion et requêtes MySQL
- Python standard : `datetime` (horodatage), `hashlib` (vérifier intégrité)

### Pourquoi ces formats ?

**SQL** : 
- Format standard MySQL
- Peut se restaurer sur n'importe quel serveur MySQL
- Contient la structure ET les données

**CSV** :
- Lisible par un humain avec Excel
- Permet des audits rapides
- Facile à partager avec la direction

### Exemple de fichier généré
```
output/backups/
  └── wms_backup_2025-01-15_143000.sql    (50 MB complète)
  └── wms_backup_2025-01-15_143000.csv    (version lisible)
```

Si la base plante, NTL peut restaurer en 30 secondes au lieu de perdre tout.

---

## Personne 4 : Module Audit

### Tâches exactes
- Scanner le réseau (par exemple 192.168.10.0/24) pour trouver TOUS les ordinateurs
- Identifier l'OS de chaque machine détecté
- Vérifier dans la base EOL (End of Life) : quand ce système n'est plus supporté ?
- Générer un rapport d'alerte (critique/warning/ok)
- Sauvegarder en JSON pour traitement automatisé

### Fichiers concernés
```
modules/audit.py            ← Code du scan
data/eol_database.json      ← Dates de fin de support pour chaque OS
```

### Dépendances utilisées
- `python-nmap` : Scanner le réseau avec Nmap
- Python standard : `json` (lire EOL database)

### Pourquoi Nmap ?
- Outil standard en admin système
- Détecte les OS avec précision
- Rapide même sur gros réseau
- Résultats XML/JSON exploitables

### Exemple de rapport
```json
{
  "scan_date": "2025-01-15",
  "vulnerabilities": [
    {
      "machine": "WH2-SERVEUR",
      "os": "Windows Server 2012",
      "eol_date": "2018-10-09",
      "status": "CRITIQUE - EOL DEPASSEE",
      "days_since_eol": 2309
    }
  ]
}
```

La direction voit immédiatement : "On a des trucs qui ne sont plus supportés depuis 6 ans, c'est un risque de sécurité."

---

## Personne 5 : Interface & Documentation

### Tâches exactes - CLI (main.py)
- Créer un menu principal avec les 3 options modules
- Afficher les résultats de manière lisible
- Gérer les erreurs si l'admin tape mal
- Sauvegarder un log de chaque action

### Tâches exactes - GUI (gui.py)
- Créer une fenêtre avec des boutons visuels
- Afficher une console en temps réel
- Permettre à l'admin de modifier les paramètres (IP, BD, réseau)
- Même fonctionnalité que le CLI mais plus user-friendly

### Tâches exactes - Documentation
- README complet (installation, utilisation, examples)
- Commentaires dans le code
- Plan de soutenance
- Guide de troubleshooting

### Fichiers concernés
```
main.py                     ← Menu terminal
gui.py                      ← Interface graphique
README.md                   ← Documentation
```

### Dépendances utilisées
- `tkinter` : Librairie GUI standard Python (incluse)
- Python standard : `logging` (traces d'exécution)

### Pourquoi Tkinter ?
- Pré-installé avec Python (pas de dépendance supplémentaire)
- Marche sur Windows, Linux, macOS identiquement
- Simple à utiliser, pas besoin d'apprendre React/Vue
- Suffisant pour une app d'admin système

### Exemple d'interface
```
┌─── NTL-SysToolbox v1.0 ────────────┐
│                                    │
│  [Diagnostic Complet]              │
│  [Sauvegarde WMS]                  │
│  [Audit Obsolescence]              │
│  [Tester Connexion]                │
│                                    │
├─ Console de résultats ─────────────┤
│ > Diagnostic lancé...              │
│ > MySQL OK - 15ms                  │
│ > CPU : 45%, RAM : 7GB/16GB        │
│ > Diagnostic terminé               │
└────────────────────────────────────┘
```

L'admin clique une fois, résultats en 5 secondes. C'est ça qu'il veut.

---

## Vue d'ensemble : Comment tout s'assemble

```
Personne 1 (Setup)
    ↓ Crée la structure et config
    ├── Personne 2 (Diagnostic) : Teste les serveurs
    ├── Personne 3 (Backup) : Sauvegarde la BD
    ├── Personne 4 (Audit) : Scanne le réseau
    └── Personne 5 (Interface) : Affiche tout proprement
    
Résultat final : NTL-SysToolbox qui marche
```

**Avantage de cette architecture** :
- Chacun code indépendamment (pas de conflits)
- Chaque module peut être testé seul
- Facile à corriger un module sans toucher aux autres
- Extensible : ajouter un module 6 prend 30 min
- Professionnel : c'est comme ça qu'on code en vrai entreprise

---

## Pourquoi Python et pas autre chose ?

### Python : Pourquoi ?
- Disponible sur Windows, Linux, macOS
- Facile à apprendre (bon pour des étudiants)
- Excellentes librairies système (psutil, paramiko, nmap)
- Code lisible = facile à maintenir
- Idéal pour scripting admin

### Alternatives considérées et rejetées :
- **C#/.NET** : Windows uniquement, pas Linux
- **Bash** : Trop faible pour une vraie app
- **Go** : Overkill, plus difficile à apprendre
- **Node.js** : Moins bon pour l'administration système

**Verdict** : Python = équilibre parfait entre puissance et simplicité.

---

## Les dépendances : Pourquoi chacune ?

| Librairie | Utilité | Personne |
|-----------|---------|----------|
| `psutil` | Lire CPU/RAM/Disque système | Personne 2 |
| `mysql-connector-python` | Se connecter à MySQL | Personne 2 + 3 |
| `python-nmap` | Scanner le réseau | Personne 4 |
| `python-dotenv` | Lire les variables d'env (optionnel) | Tous |
| `tkinter` | Interface graphique | Personne 5 |

Chacune a une raison précise. Pas de "bloatware".

---

## Résumé pour la présentation au jury

**"Nous avons divisé le projet en 5 modules indépendants, chaque personne responsable d'une partie :**

1. **Setup** : Structure et configuration (JSON facile à modifier)
2. **Diagnostic** : Tests de connectivité et santé système (psutil)
3. **Sauvegarde** : Export MySQL sécurisé (backup)
4. **Audit** : Scan réseau pour trouver les vieux systèmes (nmap)
5. **Interface** : Tout accessible via CLI ET GUI (tkinter)

**Avantages :**
- Chacun code seul = pas de conflits Git
- Architecture modulaire = prêt pour la production
- Python multiplateforme = fonctionne partout
- Chaque module réutilisable = extensible

C'est du vrai code, pas du prototype."**

---

## Checklist pour le jury (ce qu'on doit montrer)

- [ ] Code compilé et qui marche (démo en live)
- [ ] Architecture claire (fichiers et dossiers organisés)
- [ ] Dépendances justifiées (pourquoi Python, pourquoi Tkinter)
- [ ] Résultats réalistes (données cohérentes de NTL)
- [ ] Documentation complète (README + commentaires)
- [ ] Logs propres (chaque action tracée)
- [ ] Modularité (montrer qu'on peut ajouter un module facilement)
