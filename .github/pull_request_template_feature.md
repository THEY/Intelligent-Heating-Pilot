---
name: Feature / Bug Fix Pull Request
about: Template pour les PR de feature/* vers integration
title: 'feat/fix: [courte description]'
labels: ''
assignees: ''
---

## 🎯 Objectif

<!-- Décrivez brièvement l'objectif de cette PR -->

Implémente l'Issue #XX : [Titre de l'issue]

## 📝 Changements

<!-- Listez les principaux changements apportés -->

- [ ] Ajout de ...
- [ ] Modification de ...
- [ ] Suppression de ...

## 🏗️ Architecture

<!-- Expliquez les choix architecturaux (DDD, services domaine, etc.) -->

### Domain Layer
- ...

### Infrastructure Layer
- ...

### Application Layer
- ...

## ✅ Checklist Développement

Avant de demander une review, vérifiez que :

### Tests
- [ ] Tests unitaires ajoutés pour le code domaine (>80% coverage)
- [ ] Tests d'intégration ajoutés si nécessaire
- [ ] Tous les tests passent (`pytest tests/`)
- [ ] Pas de régression sur les tests existants

### Architecture DDD
- [ ] Domain layer pur (NO `homeassistant.*` imports)
- [ ] Interfaces (ABCs) utilisées pour les dépendances externes
- [ ] Value objects immutables (`@dataclass(frozen=True)`)
- [ ] Services domaine sans dépendances infrastructure

### Code Quality
- [ ] Type hints complets sur toutes les fonctions/méthodes
- [ ] Docstrings ajoutés (Google style)
- [ ] PEP 8 respecté (formatage cohérent)
- [ ] Pas de code commenté ou de `print()` debug
- [ ] Pas de "magic numbers" (constantes nommées)

### Documentation
- [ ] README.md mis à jour si nécessaire
- [ ] Docstrings complets et clairs
- [ ] Exemples d'utilisation ajoutés si API publique
- [ ] CHANGELOG.md sera mis à jour lors du merge

### Intégration
- [ ] Pas de conflit avec `integration`
- [ ] Les changements sont backward compatible si possible
- [ ] Configuration utilisateur ajoutée si nécessaire

## 🧪 Tests Effectués

<!-- Décrivez comment vous avez testé vos changements -->

### Environnement de Test
- Home Assistant version : 
- Python version : 
- VTherm version : 

### Scénarios Testés
1. ...
2. ...

### Résultats
- [ ] Tests unitaires : ✅ PASS
- [ ] Tests d'intégration : ✅ PASS
- [ ] Tests manuels : ✅ PASS

## 📊 Impact

<!-- Quel est l'impact de ce changement ? -->

- **Performance** : [Aucun impact / Amélioration / Dégradation mineure]
- **Breaking changes** : [Oui / Non]
- **Migration nécessaire** : [Oui / Non]
- **Nouvelles dépendances** : [Oui / Non]

## 🔗 Issues Liées

<!-- Liez les issues GitHub concernées -->

Closes #XX
Relates to #YY

## 📸 Screenshots / Logs

<!-- Si applicable, ajoutez des captures d'écran ou logs -->

```
Logs pertinents ici
```

## 💭 Notes pour le Reviewer

<!-- Informations supplémentaires pour faciliter la review -->

- Point d'attention particulier : ...
- Alternatives considérées : ...
- Questions ouvertes : ...

---

## 🔄 Merge Strategy

**Cette PR doit être mergée avec SQUASH MERGE** (un seul commit dans `integration`)

Message du commit squashé suggéré :
```
feat/fix: [description courte] (#XX)

- [Changement principal 1]
- [Changement principal 2]
- [Changement principal 3]

Closes #XX
```
