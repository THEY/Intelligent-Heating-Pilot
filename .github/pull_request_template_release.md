---
name: Release Pull Request
about: Template pour les PR de integration vers main (Release)
title: 'release: v[X.Y.Z] - [Titre de la Release]'
labels: 'release'
assignees: '@RastaChaum'
---

## 🚀 Release v[X.Y.Z]

<!-- Version à publier (ex: v0.4.0) -->

**Type de Release** : [Major / Minor / Patch]  
**Date Prévue** : [JJ/MM/AAAA]  
**Pré-release testée** : [v0.4.0-beta.1, v0.4.0-beta.2, ...]

---

## 📝 Changements Principaux

### ✨ Nouvelles Fonctionnalités

<!-- Listez toutes les nouvelles features ajoutées -->

- **Issue #XX** : [Titre] - [Description courte]
- **Issue #YY** : [Titre] - [Description courte]

### 🐛 Corrections de Bugs

<!-- Listez tous les bugs corrigés -->

- **Issue #XX** : [Titre] - [Description courte]
- **Issue #YY** : [Titre] - [Description courte]

### 🔧 Améliorations Techniques

<!-- Listez les refactorings, optimisations, etc. -->

- Architecture DDD renforcée
- Tests unitaires étendus (coverage : XX%)
- Documentation enrichie

### ⚠️ Breaking Changes

<!-- S'il y a des changements incompatibles avec les versions précédentes -->

- [ ] Aucun breaking change
- [ ] Breaking changes présents (voir détails ci-dessous)

**Détails des Breaking Changes** :
```
[Description des changements incompatibles et migration nécessaire]
```

---

## ✅ Checklist Release

### Documentation
- [ ] **CHANGELOG.md** mis à jour avec tous les changements
- [ ] **README.md** mis à jour (features, configuration, exemples)
- [ ] **ARCHITECTURE.md** mis à jour si changements architecturaux
- [ ] **manifest.json** : version incrémentée (v[X.Y.Z])
- [ ] **hacs.json** : version synchronisée si nécessaire
- [ ] **Release notes** rédigées (voir GITHUB_RELEASE_v[X.Y.Z].md)

### Tests et Qualité
- [ ] **Tous les tests unitaires passent** (`pytest tests/unit/`)
- [ ] **Tests d'intégration passent** (`pytest tests/integration/`)
- [ ] **Pré-release testée** en environnement réel (Docker / HA instance)
- [ ] **Pas de régression** identifiée sur les fonctionnalités existantes
- [ ] **Erreurs/warnings** vérifiés dans les logs Home Assistant

### Validation Fonctionnelle
- [ ] **Nouvelles features testées** manuellement
- [ ] **Configuration utilisateur** testée (config flow, options flow)
- [ ] **Sensors** affichent les bonnes valeurs
- [ ] **Anticipation** fonctionne correctement
- [ ] **Services HA** répondent correctement
- [ ] **Compatibilité VTherm** vérifiée (v8.0.0+)

### Pré-release (Beta)
- [ ] **Pré-release créée** : [v[X.Y.Z]-beta.N]
- [ ] **Testée pendant** : [X jours/semaines]
- [ ] **Feedback utilisateurs** : [Positif / Négatif / Aucun]
- [ ] **Issues critiques** : [Aucune / Résolues]

### Préparation Merge
- [ ] **Pas de conflit** avec `main`
- [ ] **Historique propre** dans `integration` (commits squashés)
- [ ] **Tag de release préparé** : v[X.Y.Z]

---

## 📊 Statistiques de la Release

### Issues
- **Issues fermées** : #XX, #YY, #ZZ
- **Total** : [N] issues

### Commits
- **Commits intégrés dans `integration`** : [N]
- **Période de développement** : [date début] → [date fin]

### Code
- **Fichiers modifiés** : [N]
- **Lignes ajoutées** : +[N]
- **Lignes supprimées** : -[N]
- **Coverage tests** : [XX]%

### Contributeurs
- [@RastaChaum](https://github.com/RastaChaum)
- [Autres contributeurs si applicable]

---

## 🧪 Tests de Validation

### Environnement de Test
- **Home Assistant version** : 2025.X.X
- **Python version** : 3.12.X
- **Versatile Thermostat version** : v8.X.X
- **Scheduler Component version** : v3.X.X

### Scénarios de Test Réussis
- [ ] Installation via HACS
- [ ] Configuration initiale (config flow)
- [ ] Modification options (options flow)
- [ ] Anticipation normale (pré-chauffage)
- [ ] Overshoot prevention (revert)
- [ ] Reset slopes (service)
- [ ] Logs sans erreurs critiques
- [ ] Sensors mis à jour correctement

### Test de Migration (si applicable)
- [ ] Migration depuis v[X.Y.Z-1] → v[X.Y.Z] testée
- [ ] Données persistées correctement
- [ ] Pas de perte de configuration

---

## 📚 Documentation Externe

<!-- Liens vers la documentation générée -->

- **Release Notes** : [GITHUB_RELEASE_v[X.Y.Z].md](.github/GITHUB_RELEASE_v[X.Y.Z].md)
- **CHANGELOG** : [CHANGELOG.md](../CHANGELOG.md)
- **README** : [README.md](../README.md)

---

## 🔄 Merge Strategy

**Cette PR doit être mergée avec MERGE COMMIT** (préserve l'historique complet)

Message du merge commit suggéré :
```
release: v[X.Y.Z] - [Titre de la Release]

Merge integration branch with all features and fixes from v[X.Y.Z-1] to v[X.Y.Z]

Features:
- Issue #XX: [Titre]
- Issue #YY: [Titre]

Bug Fixes:
- Issue #ZZ: [Titre]

See CHANGELOG.md for complete release notes.
```

---

## 📋 Actions Post-Merge

Après le merge de cette PR, effectuer :

1. **Tagger la release** :
   ```bash
   git checkout main
   git pull origin main
   git tag v[X.Y.Z] -m "Release v[X.Y.Z]: [Titre]"
   git push origin v[X.Y.Z]
   ```

2. **Vérifier la release automatique** :
   - Vérifier que le workflow `.github/workflows/create-release.yml` a créé la release
   - Vérifier que les issues liées sont automatiquement fermées

3. **Synchroniser `integration` avec `main`** :
   ```bash
   git checkout integration
   git merge main --ff-only
   git push origin integration
   ```

4. **Communiquer** :
   - Annoncer la release sur GitHub Discussions
   - Mettre à jour HACS si nécessaire
   - Annoncer sur forums/Discord si applicable

---

## 💬 Notes pour l'Administrateur

<!-- Informations supplémentaires pour l'approbation -->

- Points d'attention : ...
- Décisions critiques prises : ...
- Dépendances externes : ...

---

**Reviewer** : @RastaChaum  
**Deadline** : [JJ/MM/AAAA]

See [CHANGELOG.md](../CHANGELOG.md) for full details.
