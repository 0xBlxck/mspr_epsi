# Fiche Technique - Fichiers Clés

## main.py - Interface en ligne de commande

**Ce que c'est :**
- Le point d'entrée principal de l'application en mode terminal
- Affiche un menu interactif avec 3 modules et des sous-menus

**Pourquoi ce choix :**
- Accessible sur tous les serveurs (pas de dépendance graphique)
- Facile à utiliser pour un administrateur système
- Peut être automatisé via scripts

**À dire au jury :**
"main.py est notre CLI. C'est simple, efficace, et ça permet à un admin système de lancer les diagnostics directement depuis un terminal SSH sur n'importe quel serveur. Pas besoin d'interface graphique."

**Architecture :**
```
main.py
  ├─ Menu Principal
  ├─ DiagnosticModule (1 à 6)
  ├─ BackupModule (1 à 3)
  ├─ AuditModule (1 à 4)
  └─ Logs
```

---

## gui.py - Interface graphique

**Ce que c'est :**
- Interface graphique moderne avec Tkinter
- Affiche les 3 modules dans une fenêtre avec console intégrée
- Affiche les résultats en temps réel avec couleurs

**Pourquoi ce choix :**
- **Tkinter** : Bibliothèque Python standard, pas d'installation externe
- **Interface** : Plus conviviale pour des managers/consultants
- **Console intégrée** : Voir les résultats directement sans fichiers

**À dire au jury :**
"gui.py offre une alternative graphique à main.py. C'est plus beau, plus intuitif, mais basé sur la même logique. Un administrateur peut préférer le CLI, un consultant préférera la GUI. Les deux font exactement la même chose."

**Architecture :**
```
gui.py
  ├─ Window principale
  ├─ 3 Modules (boutons)
  ├─ Console résultats (temps réel)
  ├─ Dialogues pour saisie
  └─ Barre de statut
```

---

## README.md - Documentation

**Ce que c'est :**
- Documentation complète du projet
- Installation, utilisation, structure du projet
- Exemples concrets

**Pourquoi c'est important :**
- Explique comment utiliser l'outil
- Donne la structure du projet au jury
- Montre que vous maîtrisez la documentation

**À dire au jury :**
"Le README explique tout : comment installer, comment utiliser les deux interfaces, la structure du projet, et les formats de sortie. C'est la documentation qu'un devops trouvera sur GitHub pour comprendre l'outil."

---

## Résumé à présenter (30 secondes)

*"Nous avons 3 fichiers clés :*

1. **main.py** - CLI simple, rapide, pour les admins système
2. **gui.py** - Interface graphique, plus intuitive, même fonctionnalité
3. **README.md** - Doc complète pour comprendre et utiliser l'outil

*Les 3 pointent vers les mêmes modules (diagnostic, backup, audit). C'est juste deux interfaces différentes pour le même outil."*
