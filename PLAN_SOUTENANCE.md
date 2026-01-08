# Plan de Soutenance NTL-SysToolbox
## Répartition par présentateur (5 personnes - 20 minutes)

---

## ⏱️ CHRONOLOGIE TOTALE : 20 minutes

| Partie | Présentateur | Durée | Sujet |
|--------|--------------|-------|-------|
| 1 | Présentateur 1 | 3 min | Contexte client & Présentation générale |
| 2 | Présentateur 2 | 4 min | Architecture technique & Choix technologies |
| 3 | Présentateur 3 | 4 min | Module Diagnostic (vérifications critiques) |
| 4 | Présentateur 4 | 4 min | Module Sauvegarde + Audit d'obsolescence |
| 5 | Présentateur 5 | 5 min | Démo + Bilan & Perspectives |

---

## 📋 DÉTAIL DE CHAQUE PARTIE

### **PARTIE 1 - CONTEXTE CLIENT & PRÉSENTATION (3 min)**
**Présentateur 1 : [NOM]**

**Objectif** : Planter le décor et justifier le projet

**Points à couvrir** :
1. **NordTransit Logistics (NTL)** - Qui sont-ils ?
   - PME de logistique basée aux Hauts-de-France
   - 4 sites : siège (Lille) + 3 entrepôts (Lens, Valenciennes, Arras)
   - ~240 personnes en vitesse de croisière

2. **Les enjeux IT critiques**
   - Dépendance forte au Warehouse Management System (WMS)
   - Fenêtres de maintenance très courtes (exploitation 24/7)
   - Équipe IT réduite (4 personnes) → automatisation nécessaire

3. **La mission confiée**
   - Concevoir un outil pour industrialiser les vérifications
   - Sécuriser les sauvegardes du WMS (données critiques)
   - Auditer l'obsolescence de l'infrastructure

4. **Résultat attendu**
   - Un outil fonctionnel + livrables documentés

**Slide 1** : NordTransit Logistics (contexte, sites, enjeux)  
**Slide 2** : Les 3 problèmes majeurs à résoudre  
**Slide 3** : NTL-SysToolbox = la solution  

---

### **PARTIE 2 - ARCHITECTURE TECHNIQUE & CHOIX (4 min)**
**Présentateur 2 : [NOM]**

**Objectif** : Montrer que les choix techniques sont réfléchis et justifiés

**Points à couvrir** :

1. **Pourquoi Python ?**
   - Exécutable sur Windows ET Linux (contrainte cahier des charges)
   - Riche écosystème (psutil, requests, nmap, MySQL)
   - Communauté active + maintenance long terme

2. **Architecture modulaire**
   - 3 modules indépendants = testables séparément
   - Utilitaires partagés (logging, output)
   - Configuration externalisée (JSON + variables env)
   - Facilite la maintenance et l'évolution

3. **Interfaces utilisateur**
   - CLI interactif (mode production/serveur)
   - GUI Tkinter (ergonomie pour les admins)
   - Les deux partagent la même logique métier

4. **Sécurité & Fiabilité**
   - Gestion des erreurs robuste
   - Logs horodatés et traçables
   - Outputs JSON pour intégration monitoring
   - Pas de hardcoding de credentials

5. **Artefacts produits**
   - Code source sur Git (branches, tags)
   - Documentation technique complète
   - Manuel d'installation/utilisation

**Slide 1** : Diagramme architecture générale  
**Slide 2** : Stack technologique + justifications  
**Slide 3** : Structure modulaire du code  
**Slide 4** : Sorties JSON + codes de retour  

---

### **PARTIE 3 - MODULE DIAGNOSTIC (4 min)**
**Présentateur 3 : [NOM]**

**Objectif** : Montrer comment on détecte les défaillances critiques

**Points à couvrir** :

1. **Contexte du module**
   - NTL a besoin de vérifier ses services critiques rapidement
   - Les admins n'ont que quelques minutes avant mise en prod
   - Doit donner un état synthétique du siège

2. **Fonctionnalités implémentées**
   - Vérifier l'état AD/DNS (requête LDAP/DNS)
   - Tester la base MySQL (connexion + perf)
   - Diagnostiquer un serveur Windows (CPU/RAM/Disques/Uptime)
   - Diagnostiquer un serveur Linux (Ubuntu)
   - **Nouveauté : Test de ping réseau** (connectivité)

3. **Exemple concret**
   - Scénario : Le WMS ne répond plus
   - On lance le diagnostic
   - Outil teste : AD → DNS → MySQL → Réseau
   - Résultat : "MySQL down on 192.168.10.21 - Connexion timeout"
   - Admin gagne 10 minutes de troubleshooting

4. **Sortie du module**
   - Console lisible + codes couleur
   - Fichier JSON horodaté pour traçabilité
   - Code de retour exploitable (0=OK, 1=Erreur)

**Démo courte possible** :
- Montrer menu diagnostic
- Lancer test ping
- Afficher résultat en console + fichier JSON

**Slide 1** : Architecture du module diagnostic  
**Slide 2** : Les 5 types de contrôles  
**Slide 3** : Exemple d'exécution (output console + JSON)  
**Slide 4** : Cas d'usage réels pour l'admin NTL  

---

### **PARTIE 4 - SAUVEGARDE WMS + AUDIT OBSOLESCENCE (4 min)**
**Présentateur 4 : [NOM]**

**Objectif** : Montrer les deux modules restants et leur valeur ajoutée

#### **4A - Module Sauvegarde (2 min)**

1. **Contexte critique**
   - Le WMS = données stratégiques (réception/expédition)
   - Perte de données = arrêt production = clients mécontents
   - NTL a des sauvegardes, mais jamais testées → risqué

2. **Ce que fait le module**
   - Sauvegarde SQL complète de la base MySQL
   - Export CSV de table par table
   - Horodatage systématique
   - Trace complète de qui/quand/quoi

3. **Sécurité**
   - Vérification du MD5/intégrité
   - Stockage dans dossier output/backups/
   - Logs de chaque opération

#### **4B - Module Audit d'obsolescence (2 min)**

1. **Contexte**
   - Infrastructure NTL vieillit (Windows Server 2012, CentOS ancien)
   - Microsoft/distributeurs stoppent le support
   - Risque sécurité + légal si data sensibles

2. **Ce que fait le module**
   - Scanner réseau pour découvrir les machines
   - Détecter automatiquement l'OS de chaque IP
   - Croiser avec base de données EOL (dates de fin de support)
   - Générer rapport : "OK", "Warning" (fin support proche), "Critique" (EOL dépassé)

3. **Exemple**
   - Scan réseau 192.168.10.0/24
   - Trouve : DC01 (Windows Server 2016), WMS-DB (Ubuntu 20.04)
   - Rapport : "DC01 = fin de support 2026 ⚠️ prévoir upgrade" | "Ubuntu 20.04 = OK jusqu'2025"

4. **Sortie**
   - Rapport JSON avec actions recommandées
   - Exportable pour documenter le patrimoine

**Slide 1** : Module Sauvegarde = garantir la récupération  
**Slide 2** : Module Audit = identifier les risques EOL  
**Slide 3** : Exemple rapport complet d'obsolescence  
**Slide 4** : Impact pour NTL = plan d'upgrade informatisé  

---

### **PARTIE 5 - DÉMONSTRATION + BILAN (5 min)**
**Présentateur 5 : [NOM]**

**Objectif** : Finaliser avec une démo concrète + vision projet

#### **5A - Courte démo (2-3 min)**

**Déroulement suggéré** :
1. Lancer `python gui.py` 
2. Montrer le menu graphique
3. Exécuter 1 diagnostic simple (ex: ping réseau)
4. Montrer console + fichier JSON produit
5. Montrer logs dans dossier output/

**OU mode CLI** :
1. `python main.py`
2. Menu interactif
3. Lancer audit réseau simplifié
4. Montrer résultat

#### **5B - Bilan du projet (1.5 min)**

**Compétences démontrées** (vis-à-vis du jury) :
- BC01.4 : Identifier les systèmes défaillants ✅ (Module Diagnostic)
- BC01.11 : Automatiser les sauvegardes ✅ (Module Sauvegarde)
- BC02.7 : Superviser l'infrastructure ✅ (Module Diagnostic)
- BC02.8 : Recenser les ressources ✅ (Module Audit)
- BC01.9 : Scripts de collecte de données ✅ (Tous modules)
- BC04.2 : Documentation technique ✅ (README + doc interne)

**Défis rencontrés & solutions** :
- **Défi** : Interaction multi-plateforme (Windows/Linux)
  - **Solution** : Python + gestion exceptions robuste
  
- **Défi** : Sécurité des credentials
  - **Solution** : Variables environnement + config file

- **Défi** : Fiabilité des scans réseau
  - **Solution** : Timeouts, retry logic, logs détaillés

**Résultats atteints** :
- ✅ Outil fonctionnel, testé, documenté
- ✅ 3 modules indépendants
- ✅ Sorties JSON + logs
- ✅ Code source Git propre
- ✅ Prêt pour déploiement NTL

#### **5C - Perspectives/Évolutions** (0.5-1 min)

**Court terme** :
- Tests en environnement réel NTL
- Intégration avec monitoring Zabbix

**Moyen terme** :
- Alertes email automatiques
- Dashboard web pour consulter rapports

**Message final** :
> "NTL-SysToolbox = gagne du temps et sécurise l'infra. Les admins passent 30 min/semaine en moins à troubleshooting, plus de temps pour la stratégie."

**Slide 1** : Timeline démo (ce qu'on va montrer)  
**Slide 2** : Compétences certifiées couverte par le projet  
**Slide 3** : Défis techniques + solutions  
**Slide 4** : Résultats finaux + perspectives  

---

## 🎯 CONSEILS PRATIQUES POUR LA SOUTENANCE

### **Avant de commencer (5 min avant)**
- [ ] Vérifier que tous les fichiers sont à jour
- [ ] Tester la démo sur la machine de présentation
- [ ] Avoir un PC de secours avec l'outil prêt
- [ ] Imprimer les diapos ou les avoir offline

### **Pendant la soutenance**
- Parlez clair, pas trop vite (vous avez 3-5 min = ~600 paroles par personne)
- Regardez le jury, pas les slides
- Passez le bâton au présentateur suivant sans vide
- Chacun gère votre timing (chrono en coulisse)
- Préparez 1-2 questions d'anticipation pour le jury

### **Transitions entre présentateurs (critiques !)**
- Présentateur 1 → Présentateur 2 : "Now [Name] will present our technical architecture"
- Présentateur 2 → Présentateur 3 : "Let me hand over to [Name] who will walk through the Diagnostic module"
- Présentateur 3 → Présentateur 4 : "Moving on to the Backup and Obsolescence modules with [Name]"
- Présentateur 4 → Présentateur 5 : "[Name] will now demo the tool and wrap up with our conclusions"
- Présentateur 5 → Jury : "Merci, nous sommes prêts pour vos questions"

### **Si problème technique**
- Démo GUI ne marche pas ? Basculer mode CLI
- Fichier JSON absent ? Le regenerer live (peu importe l'IP, l'important c'est de montrer le processus)
- Pas de réseau ? Utiliser données pré-générées

### **Questions fréquentes du jury à anticiper**
- "Pourquoi Python et pas PowerShell ?" → Cross-plateforme
- "Comment gérez les credentials ?" → Env variables + config
- "Scalabilité : jusqu'où ça monte ?" → Bien pour PME, limites sur gros réseau
- "Comment on déploie ça en prod ?" → Git + pip install + doc = autonome
- "Et si le réseau est down ?" → Pas d'impact, on teste local ou on log l'erreur

---

## 📊 SLIDES RECOMMANDÉES (support visuel)

**Total : ~12-15 slides pour 20 min**

1. Title Slide : "NTL-SysToolbox - Projet MSPR EPSI"
2. Contexte NTL (sites, enjeux)
3. Les 3 problèmes
4. Architecture générale (schema boxes modules)
5. Stack technologique
6. Module Diagnostic - Architecture
7. Module Diagnostic - Contrôles
8. Module Sauvegarde - Processus
9. Module Audit - Processus
10. Exemple rapport audit
11. Démo - Timeline
12. Compétences couvertes (checklist)
13. Bilan + Perspectives
14. Questions ?

**Astuce** : Utilisez des images/diagrams plutôt que du texte → plus pro, plus lisible

---

## ✅ CHECKLIST AVANT SOUTENANCE

- [ ] Tous les fichiers commitées sur Git
- [ ] Code testable et exécutable
- [ ] Démo préparée et répétée 2x minimum
- [ ] Slides complètes et relues
- [ ] Chaque présentateur connaît son texte (pas de feuille)
- [ ] Timing respecté lors d'une répétition
- [ ] Questions d'anticipation préparées
- [ ] Dress code : tenue professionnelle
- [ ] Arriver 15 min avant avec le matériel

---

**Bonne soutenance ! 🚀**
