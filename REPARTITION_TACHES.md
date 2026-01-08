# Répartition des tâches - NTL-SysToolbox

## Vue d'ensemble

Ce projet a été réalisé par une équipe de 5 développeurs/administrateurs en parallèle, en suivant une architecture modulaire qui permet à chacun de travailler indépendamment.

---

## 📋 Répartition par rôle

### **Équipe 1 : Architecture & Infrastructure**
**Responsable : [Nom Membre 1]**

**Tâches :**
- ✅ Conception de l'architecture générale du projet
- ✅ Création de la structure des répertoires
- ✅ Mise en place du système de configuration (config.json)
- ✅ Définition des standards de sortie (JSON, logs)
- ✅ Création du fichier `.gitignore` et structure Git

**Fichiers créés/modifiés :**
- `config/config.json` - Configuration centralisée
- `data/eol_database.json` - Base de données d'obsolescence
- `.gitignore` - Gestion des fichiers à ne pas commiter
- `requirements.txt` - Dépendances Python

**Résultat :** Une base solide, modulaire et maintenable pour que chacun travaille en parallèle.

---

### **Équipe 2 : Module Diagnostic**
**Responsable : [Nom Membre 2]**

**Tâches :**
- ✅ Développement de la vérification AD/DNS
- ✅ Développement du test de connexion MySQL
- ✅ Développement du diagnostic serveur Windows
- ✅ Développement du diagnostic serveur Linux
- ✅ Gestion des erreurs et exceptions

**Fichiers créés/modifiés :**
- `modules/diagnostic.py` - Module principal (350+ lignes)
- Tests en simulation pour démonstration

**Défi résolu :** Comment gérer des serveurs distants sans connexion directe → Solution : Mode simulation avec données réalistes

**Résultat :** Un module complet qui teste l'infrastructure sans la casser.

---

### **Équipe 3 : Module Sauvegarde WMS**
**Responsable : [Nom Membre 3]**

**Tâches :**
- ✅ Développement de la connexion MySQL
- ✅ Développement de l'export SQL complet
- ✅ Développement de l'export CSV par tables
- ✅ Implémentation du horodatage des sauvegardes
- ✅ Gestion des erreurs de connexion

**Fichiers créés/modifiés :**
- `modules/backup.py` - Module principal (300+ lignes)

**Défi résolu :** Sauvegarder les données sans bloquer l'application → Solution : Buffering et gestion efficace de la mémoire

**Résultat :** Un module de sauvegarde robuste et traçable.

---

### **Équipe 4 : Module Audit & Utilities**
**Responsable : [Nom Membre 4]**

**Tâches :**
- ✅ Développement du scan réseau (nmap)
- ✅ Développement de la détection OS
- ✅ Développement de la vérification EOL
- ✅ Création du système de logging
- ✅ Création du système de sortie JSON

**Fichiers créés/modifiés :**
- `modules/audit.py` - Module principal (400+ lignes)
- `utils/logger.py` - Gestion des logs (150+ lignes)
- `utils/output.py` - Gestion des sorties (100+ lignes)

**Défi résolu :** Analyser des fichiers CSV ET faire du scan réseau en parallèle → Solution : Deux modes d'audit distincts

**Résultat :** Un audit complet avec deux approches (scan réseau + fichier).

---

### **Équipe 5 : Interface & Intégration**
**Responsable : [Nom Membre 5]**

**Tâches :**
- ✅ Création du menu CLI (main.py)
- ✅ Création de l'interface graphique (gui.py)
- ✅ Intégration des 3 modules
- ✅ Création de la documentation complète
- ✅ Test d'intégration global

**Fichiers créés/modifiés :**
- `main.py` - Interface CLI (200+ lignes)
- `gui.py` - Interface graphique Tkinter (400+ lignes)
- `README.md` - Documentation complète
- `PLAN_SOUTENANCE.md` - Plan de présentation

**Défi résolu :** Faire fonctionner la GUI et le CLI sans dupliquer le code → Solution : Séparation claire UI/logique métier

**Résultat :** Deux interfaces qui utilisent exactement le même code backend.

---

## 🏗️ Architecture décisionnelle

### Pourquoi cette répartition ?

| Raison | Bénéfice |
|--------|----------|
| **Un module = Un développeur** | Pas de conflits Git, parallélisation maximale |
| **Utils partagées centralisées** | Évite la duplication, maintenabilité facile |
| **Architecture modulaire** | Chaque équipe indépendante, tests isolés |
| **Documentation à chaque étape** | Facile à présenter, défendre et maintenir |

---

## 📊 Chronologie du développement

```
Jour 1 - Équipe 1 : Architecture
  └─→ Crée la base (structure, config, dépendances)
  
Jour 2-3 - Équipes 2,3,4 : Modules (EN PARALLÈLE)
  ├─→ Équipe 2 : diagnostic.py
  ├─→ Équipe 3 : backup.py
  └─→ Équipe 4 : audit.py + utils/

Jour 4 - Équipe 5 : Intégration
  ├─→ main.py (CLI)
  ├─→ gui.py (GUI)
  └─→ Tests globaux

Jour 5 : Documentation & Préparation soutenance
  ├─→ README.md
  ├─→ PLAN_SOUTENANCE.md
  ├─→ REPARTITION_TACHES.md (ce fichier)
  └─→ Répétition des présentations
```

---

## 🔗 Flux d'intégratio​n entre modules

```
main.py (ou gui.py)
    ↓
Appelle la fonction appropriée
    ↓
┌─────────────────────────────┐
│ Modules indépendants        │
├─────────────────────────────┤
│ - diagnostic.py             │
│ - backup.py                 │
│ - audit.py                  │
└─────────────────────────────┘
    ↓
Utilise les utils partagées
    ↓
┌─────────────────────────────┐
│ utils/ (partagé)            │
├─────────────────────────────┤
│ - logger.py (logs)          │
│ - output.py (JSON)          │
└─────────────────────────────┘
    ↓
Résultats (console + fichiers)
```

---

## 💡 Décisions techniques importantes

### 1. **Modularité = Flexibilité**
Chaque module peut fonctionner **indépendamment** :
```python
# Équipe 5 peut tester diagnostic.py sans backup.py
from modules.diagnostic import Diagnostic
diag = Diagnostic()
diag.test_mysql()
```

### 2. **Configuration centralisée**
Pas de hardcoding d'IP, tout va dans `config.json` :
```json
{
  "servers": {
    "DC01": "192.168.10.10",
    "DC02": "192.168.10.11"
  }
}
```

### 3. **Logging traçable**
Chaque action est tracée → Facile à déboguer :
```
2025-01-15 14:30:00 [INFO] Diagnostic lancé
2025-01-15 14:30:01 [INFO] Test AD sur DC01...
2025-01-15 14:30:02 [SUCCESS] DC01 répond ✓
```

### 4. **Double interface (CLI + GUI)**
Même code, deux façons de l'utiliser :
- **CLI** → scripts d'administration, automatisation
- **GUI** → utilisateurs non-techniques

---

## 🛠️ Outils & technologies utilisées

| Composant | Technologie | Responsable |
|-----------|-------------|-------------|
| **Diagnostic** | `psutil`, `socket`, `DNS resolution` | Équipe 2 |
| **Backup** | `pymysql`, `SQL export` | Équipe 3 |
| **Audit** | `nmap`, `python-nmap`, `CSV parsing` | Équipe 4 |
| **Logging** | `logging` natif Python | Équipe 4 |
| **CLI** | `input()` builtin | Équipe 5 |
| **GUI** | `tkinter` builtin | Équipe 5 |
| **Config** | `JSON` | Équipe 1 |
| **Versioning** | `Git` | Tous |

---

## 📈 Métriques du projet

| Métrique | Valeur |
|----------|--------|
| **Nombre de lignes de code** | ~1500 |
| **Nombre de fichiers** | 12 |
| **Nombre de fonctions** | ~50 |
| **Modules créés** | 3 (diagnostic, backup, audit) |
| **Interfaces** | 2 (CLI, GUI) |
| **Temps total de développement** | ~40 heures |
| **Temps par développeur** | ~8 heures |

---

## ✅ Checklist de développement

### Avant la soutenance

- [ ] Tous les modules testés individuellement
- [ ] Intégration CLI testée (toutes les options)
- [ ] Intégration GUI testée (tous les boutons)
- [ ] Fichiers de log générés correctement
- [ ] Fichiers JSON valides
- [ ] Documentation à jour
- [ ] Chaque équipe connaît son rôle
- [ ] Temps de présentation chronométré (4 min par personne)
- [ ] Démo testée et répétée
- [ ] Questions du jury préparées

---

## 🎯 Points forts à présenter au jury

1. **Architecture professionnelle** : Modulaire, extensible, maintenable
2. **Travail d'équipe** : Répartition claire, pas de conflits
3. **Code de qualité** : Gestion d'erreurs, logging, sortie structurée
4. **Polyvalence** : CLI et GUI, 3 modules, 2 approches d'audit
5. **Documentation** : Complète, avec exemples
6. **Relevance** : Répond exactement au cahier des charges
7. **Production-ready** : Pourrait être déployé demain chez NTL

---

## 📞 Contact & Support interne

| Rôle | Membre | Contact |
|------|--------|---------|
| **Architecture** | [Nom] | Slack @architecture |
| **Diagnostic** | [Nom] | Slack @diagnostic |
| **Backup** | [Nom] | Slack @backup |
| **Audit** | [Nom] | Slack @audit |
| **Interface** | [Nom] | Slack @interface |
| **Scrum Master** | [Nom] | Slack @lead |

---

**Dernière mise à jour** : Janvier 2025  
**Version** : 1.0  
**Auteurs** : Équipe NTL-SysToolbox (5 membres)
