# 🌳 Stratégie de Branches - Intelligent Heating Pilot

Ce document définit la stratégie de branches utilisée dans le projet Intelligent Heating Pilot et comment les contributeurs doivent l'utiliser.

## 📋 Vue d'Ensemble

Le projet utilise une stratégie de branches à 3 niveaux pour garantir la qualité et la stabilité du code :

```
main (production) ← integration (pré-release) ← feature/* (développement)
```

---

## 🎯 Les Trois Branches Principales

### 1. `main` - Production (Releases Stables)

**Rôle** : Contient uniquement le code **testé et validé** prêt pour la production.

**Caractéristiques** :
- ✅ Versions RELEASE uniquement (v0.3.0, v0.4.0, etc.)
- ✅ Code stable, testé et documenté
- ✅ Protégé : **personne ne développe directement dessus**
- ✅ Alimenté uniquement par des PR depuis `integration`
- ✅ Historique complet préservé (merge commits)

**Règles** :
- 🚫 **Interdit** : push direct, commits directs
- ✅ **Autorisé** : merge de `integration` via PR (après approbation admin)
- ✅ **Merge strategy** : **Merge commit** (garde l'historique complet)

**Quand utiliser** :
- Pour publier une nouvelle version RELEASE
- Après validation complète de `integration`
- Uniquement par l'administrateur

---

### 2. `integration` - Pré-Release (Agrégation)

**Rôle** : Branche d'**intégration et de pré-release** où convergent toutes les nouvelles features et corrections.

**Caractéristiques** :
- ✅ Reçoit les PR des branches `feature/*`
- ✅ Permet de tester l'intégration de plusieurs features ensemble
- ✅ Sert à créer les **pré-releases** (v0.4.0-beta.1, etc.)
- ✅ Historique condensé (squash merge des features)
- ✅ Protégé : nécessite des PR pour les features

**Règles** :
- 🚫 **Interdit** : développement de features directement dessus
- ✅ **Autorisé** : 
  - Merge de `feature/*` via PR avec **squash merge**
  - Push direct par admin/contributeurs (corrections mineures)
- ✅ **Merge strategy** : **Squash merge** (un seul commit par feature)

**Quand utiliser** :
- Pour intégrer une nouvelle feature terminée
- Pour créer une pré-release et la tester
- Pour corriger des bugs d'intégration

---

### 3. `feature/*` - Développement (Features Individuelles)

**Rôle** : Branches **temporaires** pour le développement de nouvelles features ou corrections de bugs.

**Caractéristiques** :
- ✅ Une branche par feature/bug (ex: `feature/issue-23-power-correlation`)
- ✅ Créée **toujours depuis `main`**
- ✅ Pas de protection (liberté de développement)
- ✅ Supprimée automatiquement après merge
- ✅ Commits multiples OK pendant le développement

**Règles** :
- ✅ **Naming convention** : `feature/issue-XX-description` ou `fix/issue-XX-description`
- ✅ **Base** : Toujours créer depuis `main` à jour
- ✅ **Target** : Ouvrir PR vers `integration` uniquement
- ✅ **Merge strategy** : **Squash merge** (condense tous les commits en un seul)

**Quand utiliser** :
- Pour chaque nouvelle feature (Issue GitHub)
- Pour chaque correction de bug
- Pour expérimenter sans impacter les autres branches

---

## 🔄 Workflow Complet

### Étape 1 : Créer une Branche Feature

```bash
# 1. Mettre à jour main
git checkout main
git pull origin main

# 2. Créer la branche feature depuis main
git checkout -b feature/issue-23-power-correlation

# 3. Pousser la branche sur GitHub
git push -u origin feature/issue-23-power-correlation
```

**Convention de nommage** :
- `feature/issue-XX-short-description` : Nouvelle fonctionnalité
- `fix/issue-XX-short-description` : Correction de bug
- `docs/update-readme` : Modification de documentation
- `refactor/domain-services` : Refactoring technique

---

### Étape 2 : Développer avec Commits Réguliers

```bash
# Faire des commits atomiques pendant le développement
git add custom_components/intelligent_heating_pilot/domain/services/power_history_tracker.py
git commit -m "feat(domain): add PowerHistoryTracker service"

git add tests/unit/domain/test_power_history_tracker.py
git commit -m "test(domain): add unit tests for PowerHistoryTracker"

git add custom_components/intelligent_heating_pilot/application/__init__.py
git commit -m "feat(app): integrate power history tracking in HeatingApplicationService"

# Pousser régulièrement
git push origin feature/issue-23-power-correlation
```

**Bonnes pratiques** :
- Commits atomiques (une modification logique = un commit)
- Messages clairs et descriptifs
- Suivre le format [Conventional Commits](https://www.conventionalcommits.org/)
- Pousser régulièrement pour ne pas perdre le travail

---

### Étape 3 : Ouvrir une Pull Request vers `integration`

#### 3.1 Sur GitHub

1. Allez sur `https://github.com/RastaChaum/Intelligent-Heating-Pilot`
2. Cliquez sur **Pull requests** → **New pull request**
3. **Base** : `integration` ← **Compare** : `feature/issue-23-power-correlation`
4. Cliquez sur **Create pull request**

#### 3.2 Remplir le Template

Utilisez le template de PR (voir `.github/pull_request_template_feature.md`) :

```markdown
## 🎯 Objectif

Implémente l'Issue #23 : Filtrage intelligent des slopes avec corrélation temporelle

## 📝 Changements

- Ajout du service `PowerHistoryTracker` (domain)
- Enrichissement de `SlopeData` avec métadonnées power
- Implémentation algorithme de corrélation temporelle
- Ajout tests unitaires (coverage >80%)

## ✅ Checklist

- [x] Tests unitaires ajoutés et passent
- [x] Architecture DDD respectée
- [x] Documentation mise à jour
- [x] Pas de régression

## 🔗 Issues Liées

Closes #23
```

#### 3.3 Attendre la Review

- L'administrateur ou un contributeur review la PR
- Corrections éventuelles demandées
- Discussion et itérations

---

### Étape 4 : Squash Merge vers `integration`

#### 4.1 Approuver et Merger

1. Quand la PR est approuvée, cliquez sur **Squash and merge** 🎯
2. **Éditez le message du commit squashé** pour résumer tous les changements :

```
feat: implement power correlation for slope filtering (#23)

- Add PowerHistoryTracker domain service for temporal correlation
- Enrich SlopeData with power_percent_avg, power_percent_max, lookback_duration
- Implement retrospective correlation algorithm (looks back in time)
- Add configuration options: lookback_minutes, min_power_threshold
- Add comprehensive unit tests (>80% coverage)
- Update documentation

This implementation solves Issue #23 by filtering slopes based on
historical power_percent data, accounting for thermal inertia.

Closes #23
```

3. Confirmez le merge
4. La branche `feature/issue-23-power-correlation` est **automatiquement supprimée**

#### 4.2 Résultat

Dans `integration`, vous aurez **un seul commit** qui résume toute la feature, au lieu de 10-15 commits de développement. Cela garde l'historique propre et lisible.

---

### Étape 5 : Créer une Pré-Release (Optionnel)

Avant de merger vers `main`, testez `integration` avec une pré-release :

```bash
# 1. Se positionner sur integration
git checkout integration
git pull origin integration

# 2. Tagger la pré-release
git tag v0.4.0-beta.1 -m "Pre-release v0.4.0-beta.1: Power correlation feature"

# 3. Pousser le tag
git push origin v0.4.0-beta.1
```

Le workflow GitHub (`.github/workflows/create-release.yml`) créera automatiquement la pré-release.

---

### Étape 6 : Release vers `main`

Quand `integration` est stable et testée :

#### 6.1 Ouvrir une PR Release

1. **Pull requests** → **New pull request**
2. **Base** : `main` ← **Compare** : `integration`
3. Remplir le template de PR Release (voir `.github/pull_request_template_release.md`)

```markdown
## 🚀 Release v0.4.0

## 📝 Changements Principaux

### Nouvelles Fonctionnalités
- Filtrage intelligent des slopes avec corrélation temporelle (#23)
- Configuration utilisateur des seuils power (#23)

### Corrections de Bugs
- Aucune dans cette release

### Améliorations Techniques
- Architecture DDD enrichie avec services domaine
- Tests unitaires renforcés (>85% coverage)

## ✅ Checklist Release

- [x] CHANGELOG.md mis à jour
- [x] README.md mis à jour
- [x] Version dans manifest.json incrémentée
- [x] Pré-release testée (v0.4.0-beta.1)
- [x] Documentation complète
- [x] Tous les tests passent

## 📊 Statistiques

- Issues fermées : #23
- Commits intégrés : 12
- Fichiers modifiés : 15
- Lignes ajoutées : +850 / Lignes supprimées : -120

See CHANGELOG.md for full details.
```

#### 6.2 Merge avec Merge Commit

1. Après approbation admin, cliquez sur **Create a merge commit** 🎯
2. **Message du merge commit** :

```
release: v0.4.0 - Power Correlation & Slope Filtering

Merge integration branch with all features and fixes from v0.3.0 to v0.4.0

See CHANGELOG.md for complete release notes.
```

3. Confirmez le merge

#### 6.3 Tagger la Release

```bash
# 1. Mettre à jour main local
git checkout main
git pull origin main

# 2. Créer le tag de release
git tag v0.4.0 -m "Release v0.4.0: Power Correlation & Slope Filtering"

# 3. Pousser le tag
git push origin v0.4.0
```

Le workflow GitHub créera automatiquement la **release finale**.

---

## 🔍 Résumé des Merge Strategies

| Source | Target | Strategy | Historique | Pourquoi |
|--------|--------|----------|------------|----------|
| `feature/*` | `integration` | **Squash merge** | 1 commit par feature | Historique condensé, facile à lire |
| `integration` | `main` | **Merge commit** | Garde tout | Traçabilité complète des releases |

### Exemple Visuel

**Avant Squash Merge (`feature/issue-23` → `integration`)** :
```
feature/issue-23:
  - feat: add PowerHistoryTracker
  - test: add unit tests
  - fix: typo in docstring
  - feat: integrate in application
  - docs: update README
  - refactor: improve naming
  - test: add edge cases
```

**Après Squash Merge dans `integration`** :
```
integration:
  - feat: implement power correlation for slope filtering (#23)
```

**Merge Commit (`integration` → `main`)** :
```
main:
  - release: v0.4.0 - Power Correlation & Slope Filtering
    ↳ Merge integration (garde tous les commits d'integration)
```

---

## 🚨 Règles Importantes

### ✅ À FAIRE

- **Toujours créer feature branches depuis `main`**
- **Ouvrir PR vers `integration` uniquement**
- **Utiliser squash merge pour feature → integration**
- **Utiliser merge commit pour integration → main**
- **Supprimer les branches après merge** (automatique)
- **Tagger les releases et pré-releases**
- **Mettre à jour CHANGELOG.md avant release**

### 🚫 À NE PAS FAIRE

- ❌ Développer directement sur `main`
- ❌ Développer directement sur `integration` (sauf corrections mineures)
- ❌ Créer des branches depuis `integration`
- ❌ Faire des merge commits de feature vers integration
- ❌ Faire des squash merge de integration vers main
- ❌ Forcer des push sur `main` ou `integration`
- ❌ Oublier de mettre à jour `main` avant de créer une branche

---

## 🎓 Exemples Concrets

### Exemple 1 : Implémenter une Feature

```bash
# 1. Créer la branche
git checkout main && git pull origin main
git checkout -b feature/issue-45-humidity-compensation

# 2. Développer (plusieurs commits)
git commit -m "feat: add HumidityCompensationService"
git commit -m "test: add unit tests"
git commit -m "feat: integrate in prediction service"
git push origin feature/issue-45-humidity-compensation

# 3. Ouvrir PR sur GitHub (feature → integration avec squash merge)

# 4. Après merge, supprimer la branche locale
git checkout integration
git pull origin integration
git branch -d feature/issue-45-humidity-compensation
```

### Exemple 2 : Corriger un Bug

```bash
# 1. Créer la branche
git checkout main && git pull origin main
git checkout -b fix/issue-50-sensor-crash

# 2. Corriger (commits atomiques)
git commit -m "fix: prevent crash when sensor unavailable"
git commit -m "test: add test for edge case"
git push origin fix/issue-50-sensor-crash

# 3. Ouvrir PR (fix → integration avec squash merge)
```

### Exemple 3 : Préparer une Release

```bash
# 1. S'assurer que integration est à jour et testée
git checkout integration
git pull origin integration

# 2. Mettre à jour la documentation
# Éditer CHANGELOG.md, README.md, manifest.json

git add CHANGELOG.md README.md custom_components/intelligent_heating_pilot/manifest.json
git commit -m "docs: prepare release v0.5.0"
git push origin integration

# 3. Créer pré-release pour tests
git tag v0.5.0-beta.1 -m "Pre-release v0.5.0-beta.1"
git push origin v0.5.0-beta.1

# 4. Tester la pré-release

# 5. Ouvrir PR (integration → main avec merge commit)

# 6. Après merge, tagger la release finale
git checkout main && git pull origin main
git tag v0.5.0 -m "Release v0.5.0"
git push origin v0.5.0
```

---

## 🔧 Maintenance et Hotfixes

### Hotfix sur `main` (Urgent)

Si un bug critique doit être corrigé en production :

```bash
# 1. Créer hotfix depuis main
git checkout main && git pull origin main
git checkout -b hotfix/critical-sensor-bug

# 2. Corriger
git commit -m "fix: critical sensor crash in production"
git push origin hotfix/critical-sensor-bug

# 3. PR vers main (squash merge acceptable pour hotfix)

# 4. Après merge sur main, backporter vers integration
git checkout integration
git pull origin integration
git merge main  # Merge commit pour garder la trace
git push origin integration
```

---

## 📚 Ressources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Squash Merging](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges#squash-and-merge-your-commits)

---

## 🎯 Philosophie

> "Le code sur `main` doit toujours être déployable. La branche `integration` permet de tester l'intégration avant la release. Les branches `feature/*` permettent d'expérimenter en toute sécurité."

**Objectifs** :
- 🎯 **Qualité** : Code stable et testé sur `main`
- 🎯 **Traçabilité** : Historique clair et compréhensible
- 🎯 **Collaboration** : Workflow simple pour les contributeurs
- 🎯 **Rapidité** : Itérations rapides sur `feature/*`, releases contrôlées

---

**Prochaines étapes** : Consultez [CONTRIBUTING.md](../CONTRIBUTING.md) pour les conventions de code et le workflow TDD/DDD.
