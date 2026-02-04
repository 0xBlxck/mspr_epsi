# NTL-SysToolbox v1.0

Outil d'administration système et réseau pour NordTransit Logistics

## Description

NTL-SysToolbox est un outil en ligne de commande développé pour industrialiser les vérifications d'exploitation, sécuriser la gestion des sauvegardes et produire des audits d'obsolescence pour l'infrastructure informatique de NordTransit Logistics.

## Fonctionnalités

### 1. Module Diagnostic
- Vérification des services AD/DNS sur les contrôleurs de domaine
- Test de connexion et performance de la base de données MySQL
- État des serveurs Windows (CPU, RAM, disques, uptime)
- État des serveurs Linux (ressources système)
- Diagnostic complet de l'infrastructure

### 2. Module Sauvegarde WMS
- Sauvegarde complète de la base de données au format SQL
- Export de tables individuelles au format CSV
- Sauvegarde automatique de toutes les tables
- Horodatage et traçabilité des sauvegardes

### 3. Module Audit d'obsolescence
- Scan de plages réseau pour détecter les composants actifs
- Détection automatique des systèmes d'exploitation
- Vérification des dates de fin de vie (EOL) des OS
- Analyse de fichiers CSV d'inventaire
- Génération de rapports complets avec recommandations

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Accès réseau aux serveurs à auditer
- Droits d'administration pour certaines opérations
- **Pour Linux** : SSH activé sur les serveurs cibles (port 22)
- **Pour Windows** : WinRM activé sur les serveurs cibles (port 5985)

### Activation WinRM sur Windows Server

\`\`\`powershell
# Sur le serveur Windows cible (en tant qu'administrateur)
Enable-PSRemoting -Force
winrm quickconfig
\`\`\`

### Installation des dépendances

\`\`\`bash
# Cloner le dépôt
git clone https://github.com/votre-organisation/ntl-systoolbox.git
cd ntl-systoolbox

# Installer les dépendances Python
pip install -r requirements.txt
\`\`\`

### Configuration

1. Éditer le fichier `config/config.json` pour adapter les paramètres à votre infrastructure
2. Les mots de passe peuvent être fournis via variables d'environnement :

\`\`\`bash
export MYSQL_PASSWORD="votre_mot_de_passe"
export SSH_PASSWORD="votre_mot_de_passe_ssh"
export WINRM_PASSWORD="votre_mot_de_passe_winrm"
\`\`\`

## Utilisation

### Interface en ligne de commande (CLI)

\`\`\`bash
python main.py
\`\`\`

### Interface graphique (GUI)

\`\`\`bash
python gui.py
\`\`\`

L'interface graphique offre une expérience utilisateur moderne avec :
- Navigation intuitive par modules
- Console de résultats en temps réel avec codes couleur
- Dialogues de saisie pour chaque fonction
- Barre de statut pour suivre les opérations en cours
- Exécution asynchrone pour ne pas bloquer l'interface

### Menu principal (CLI)

L'application présente un menu interactif avec les options suivantes :

\`\`\`
1. Module Diagnostic
2. Module Sauvegarde WMS
3. Module Audit d'obsolescence
4. Afficher les logs
0. Quitter
\`\`\`

### Exemples d'utilisation

#### Diagnostic d'un serveur MySQL

**Via CLI :**
1. Sélectionner "1. Module Diagnostic"
2. Choisir "2. Tester la base de données MySQL"
3. Saisir les informations de connexion

**Via GUI :**
1. Lancer `python gui.py`
2. Cliquer sur "Tester MySQL" dans le Module Diagnostic
3. Remplir le formulaire et cliquer sur "Tester"

#### Sauvegarde de la base WMS

**Via CLI :**
1. Sélectionner "2. Module Sauvegarde WMS"
2. Choisir "1. Sauvegarde complète de la base (SQL)"
3. Fournir les credentials MySQL

**Via GUI :**
1. Cliquer sur "Sauvegarde complète (SQL)" dans le Module Sauvegarde WMS
2. Remplir les paramètres de connexion
3. Cliquer sur "Sauvegarder"

#### Audit d'obsolescence

**Via CLI :**
1. Sélectionner "3. Module Audit d'obsolescence"
2. Choisir "4. Générer un rapport complet d'obsolescence"
3. Saisir la plage réseau (ex: 192.168.10.0/24)

**Via GUI :**
1. Cliquer sur "Rapport complet" dans le Module Audit d'obsolescence
2. Saisir la plage réseau
3. Cliquer sur "Générer"

## Structure du projet

\`\`\`
ntl-systoolbox/
├── main.py                    # Point d'entrée CLI
├── gui.py                     # Interface graphique
├── modules/
│   ├── diagnostic.py          # Module de diagnostic
│   ├── backup.py              # Module de sauvegarde
│   └── audit.py               # Module d'audit
├── utils/
│   ├── logger.py              # Gestion des logs
│   └── output.py              # Gestion des sorties JSON
├── config/
│   └── config.json            # Configuration
├── data/
│   └── eol_database.json      # Base de données EOL
├── output/
│   ├── backups/               # Sauvegardes générées
│   ├── reports/               # Rapports JSON
│   └── logs/                  # Fichiers de logs
├── requirements.txt           # Dépendances Python
└── README.md                  # Ce fichier
\`\`\`

## Sorties

### Formats de sortie

Tous les modules génèrent deux types de sorties :

1. **Affichage console** : Résultats lisibles en temps réel
2. **Fichiers JSON** : Rapports horodatés dans `output/reports/`

### Codes de retour

- `0` : Opération réussie
- `1` : Erreur fatale
- `2` : Interruption utilisateur

### Exemple de rapport JSON

\`\`\`json
{
  "metadata": {
    "generated_at": "2025-01-15T14:30:00",
    "tool": "NTL-SysToolbox v1.0",
    "format_version": "1.0"
  },
  "data": {
    "timestamp": "2025-01-15T14:30:00",
    "type": "MySQL_Check",
    "server": "192.168.10.21",
    "global_status": "OK",
    "tests": {
      "connection": {"status": "OK"},
      "version": {"status": "OK", "value": "8.0.33"}
    }
  }
}
\`\`\`

## Logs

Les logs sont automatiquement générés dans `output/logs/` avec un fichier par jour :
- Format : `ntl_systoolbox_YYYYMMDD.log`
- Niveau : INFO par défaut
- Contenu : Toutes les opérations effectuées

## Sécurité

- Ne jamais commiter les mots de passe dans le dépôt Git
- Utiliser des variables d'environnement pour les credentials
- Limiter les droits d'accès aux fichiers de configuration
- Chiffrer les sauvegardes sensibles

## Prérequis Réseau

### Pour le diagnostic Windows (WinRM)
- Port 5985 (HTTP) ou 5986 (HTTPS) ouvert
- Service WinRM activé sur le serveur cible
- Compte avec droits administrateur

### Pour le diagnostic Linux (SSH)
- Port 22 ouvert
- Service SSH activé sur le serveur cible
- Compte avec accès aux commandes système (top, free, df)

## Limitations connues

- Le scan réseau peut être lent sur de grandes plages d'adresses
- WinRM nécessite une configuration préalable sur les serveurs Windows
- Les pare-feux doivent autoriser les connexions entrantes

## Évolutions futures

- Support HTTPS pour WinRM (port 5986)
- Authentification par certificat
- Envoi de rapports par email
- Interface web de consultation des rapports
- Planification automatique des tâches

## Support

Pour toute question ou problème :
- Consulter les logs dans `output/logs/`
- Vérifier la configuration dans `config/config.json`
- Contacter l'équipe IT de NordTransit Logistics

## Licence

Usage interne NordTransit Logistics - Tous droits réservés

## Auteurs

Projet développé dans le cadre de la formation Administrateur Systèmes, Réseaux et Bases de Données

---

**Version** : 1.0  
**Date** : Janvier 2025  
**Statut** : Production
