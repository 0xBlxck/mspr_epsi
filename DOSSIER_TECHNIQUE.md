# Dossier Technique et Fonctionnel - NTL-SysToolbox

## 1. Présentation du Projet
Ce document présente les choix techniques, l'architecture et le fonctionnement de l'outil **NTL-SysToolbox**, développé pour répondre aux besoins d'administration système de NordTransit Logistics (NTL).

L'outil permet de :
- Diagnostiquer l'état des services critiques (Windows, Linux, AD, MySQL).
- Sécuriser les sauvegardes de la base WMS.
- Auditer l'obsolescence du parc informatique.

## 2. Architecture Logique

### 2.1 Structure Modulaire
L'application est construite autour d'une architecture modulaire en Python, favorisant la maintenance et l'évolutivité. Chaque fonctionnalité majeure est isolée dans un module dédié :

- **`main.py`** : Point d'entrée de l'application (CLI). Gère le menu interactif et l'orchestration.
- **`modules/diagnostic.py`** : Contient la logique de connexion et d'interrogation des serveurs (SSH, WinRM, MySQL, Socket).
- **`modules/backup.py`** : Gère les dumps SQL et exports CSV via `mysql-connector`.
- **`modules/audit.py`** : Implémente le scan réseau et la comparaison avec la base de données EOL (End-of-Life).
- **`utils/`** : Fonctions transverses (logging, formatage JSON).

### 2.2 Choix Techniques

| Composant | Technologie | Justification |
|-----------|-------------|---------------|
| **Langage** | Python 3 | Portabilité Windows/Linux, richesse des bibliothèques système. |
| **Linux (SSH)** | `paramiko` | Standard robuste pour SSH en Python. Permet d'exécuter des commandes (`top`, `free`) sans agent. |
| **Windows (WinRM)** | `pywinrm` | Protocole natif de gestion Windows. Évite d'installer des agents tiers. Utilise PowerShell à distance. |
| **Base de Données** | `mysql-connector` | Driver officiel, performant pour les dumps et requêtes. |
| **Config** | JSON | Format standard, lisible par l'humain et facile à parser. |
| **Logs/Rapports** | JSON & Texte | JSON pour l'exploitation machine (supervision), Texte pour la lecture humaine. |

## 3. Fonctionnement des Modules

### 3.1 Module Diagnostic
Ce module se connecte aux serveurs pour récupérer des métriques en temps réel.
- **Windows** : Connexion via WinRM (port 5985). Exécution de commandes PowerShell (`Get-CimInstance`, `Get-ComputerInfo`) pour récupérer CPU, RAM, Disques et Uptime.
- **Linux** : Connexion via SSH (port 22). Exécution de commandes bash (`cat /etc/os-release`, `uptime`, `df -h`, `free -m`).
- **Services** : Tests de port TCP pour AD/DNS et requêtes SQL simples pour MySQL.

### 3.2 Module Sauvegarde
Assure la continuité d'activité du WMS.
- **Sauvegarde SQL** : Dump complet de la structure et des données.
- **Export CSV** : Extraction granulaire par table pour analyse ou migration.
- **Sécurité** : Les fichiers produits sont horodatés pour éviter les écrasements.

### 3.3 Module Audit d'Obsolescence
Démarche retenue :
1.  **Scan Réseau** : Balayage des IPs actives sur une plage donnée (ping + test ports).
2.  **Fingerprinting** : Déduction de l'OS basée sur les ports ouverts (ex: 3389/WinRM = Windows, 22 = Linux).
3.  **Comparaison EOL** : Croisement des versions détectées avec une base de données locale (`data/eol_database.json`) contenant les dates de fin de support.
4.  **Rapport** : Génération d'un JSON listant les machines obsolètes ou à risque.

## 4. Gestion de la Configuration et des Secrets

### 4.1 Configuration (`config.json`)
Les paramètres non sensibles (IPs, ports par défaut, seuils d'alerte) sont stockés dans `config/config.json`. Cela permet de modifier la cible de l'audit sans toucher au code.

### 4.2 Gestion des Secrets
Pour respecter les bonnes pratiques de sécurité (aucun mot de passe en dur) :
- **Variables d'Environnement** : L'outil privilégie l'usage de variables d'environnement (`MYSQL_PASSWORD`, `SSH_PASSWORD`, `WINRM_PASSWORD`).
- **Fichier `.env`** : Un fichier `.env` peut être utilisé localement pour charger ces variables automatiquement (via `python-dotenv`).
- **Interaction** : Si les variables ne sont pas définies, l'outil les demande interactivement à l'utilisateur (sans affichage des caractères saisis).

## 5. Ergonomie

L'interface CLI a été conçue pour être utilisable sans documentation complexe :
- **Menu Numéroté** : Navigation simple par choix chiffrés.
- **Valeurs par Défaut** : Les prompts proposent des valeurs par défaut (issues de `config.json` ou des variables d'env).
- **Feedback** : Utilisation d'emojis (✅, ❌, 📊) pour une lecture rapide des status.

## 6. Conclusion
NTL-SysToolbox répond au besoin d'industrialisation et de fiabilité demandé. Son architecture ouverte permet d'ajouter facilement de nouveaux types de checks ou de supporter d'autres OS à l'avenir.
