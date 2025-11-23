# 🔧 Guide de Réalignement des Branches Git

## 🎯 Objectif

Réaligner l'historique de `integration` avec `main` après avoir fait des squash merges par le passé.

---

## 📊 Situation Actuelle

**Problème** : Vous avez fait un squash merge de `integration` vers `main`, créant une divergence d'historique.

```
main:        ... → v0.3.0 → 598a29f (squash de integration)
integration: ... → v0.3.0 → ab200aa → ... → b201fb5 (historique complet)
```

Git ne reconnaît pas que le commit squashé `598a29f` dans `main` correspond aux commits `ab200aa...b201fb5` dans `integration`.

---

## ✅ Solution Recommandée : Rebaser integration sur main

Cette solution :
- ✅ Préserve les nouveaux commits dans `integration`
- ✅ Aligne les historiques
- ✅ Ne perd aucun travail
- ✅ Prépare pour le workflow correct (merge commits)

---

## 🛠️ Procédure Détaillée

### Étape 0 : Backup (✅ DÉJÀ FAIT)

```bash
# Créer un backup de integration
git branch integration-backup integration
```

**Vérifier** : `git branch` doit montrer `integration-backup`

---

### Étape 1 : Identifier les Nouveaux Commits

Identifier les commits dans `integration` qui sont **après** v0.3.0 et qui ne sont **pas encore** dans `main` :

```bash
# Lister les commits après v0.3.0 dans integration
git log v0.3.0..integration --oneline
```

**Résultat attendu** :
```
b201fb5 feat: add PR models et update branch strategy
9da40c8 feat: supprimer les instructions de l'agent...
62d2d56 Add specialized agents for TDD workflow...
dbf774e feat: add documentation for realease...
```

Ces commits doivent être **préservés** après le rebase.

---

### Étape 2 : Mettre à Jour `main` Localement

```bash
# S'assurer que main est à jour
git checkout main
git pull origin main
```

**Vérifier** : Vous devez être sur le commit `598a29f` (Release 0.3.0)

---

### Étape 3 : Rebaser `integration` sur `main`

⚠️ **ATTENTION** : Cette opération réécrit l'historique de `integration`.

```bash
# Retourner sur integration
git checkout integration

# Rebaser sur main (résolution interactive)
git rebase main
```

#### Que Va-t-il Se Passer ?

Git va essayer de **rejouer** tous les commits de `integration` qui ne sont pas dans `main` **par-dessus** le commit `598a29f` de `main`.

**Deux scénarios possibles** :

#### **Scénario A : Rebase Réussit (Pas de Conflits)**

Si les commits après v0.3.0 dans `integration` ne modifient pas les mêmes fichiers que le squash dans `main`, le rebase réussira automatiquement.

```bash
Successfully rebased and updated refs/heads/integration.
```

**Passez à l'Étape 4.**

#### **Scénario B : Conflits de Rebase**

Si Git détecte des conflits (modifications des mêmes lignes), vous devrez les résoudre manuellement.

**Messages typiques** :
```
CONFLICT (content): Merge conflict in <file>
```

**Résoudre les conflits** :

1. **Ouvrir les fichiers en conflit** dans VS Code
2. **Choisir les bonnes modifications** (généralement garder les modifications de `integration`)
3. **Marquer comme résolu** :
   ```bash
   git add <fichier-résolu>
   ```
4. **Continuer le rebase** :
   ```bash
   git rebase --continue
   ```
5. **Répéter** si d'autres conflits apparaissent

**En cas de problème grave** :
```bash
# Annuler le rebase et revenir à l'état initial
git rebase --abort
```

Vous pouvez alors revenir à `integration-backup` :
```bash
git checkout integration-backup
git branch -D integration
git checkout -b integration integration-backup
```

---

### Étape 4 : Vérifier le Résultat

Après un rebase réussi, vérifier l'historique :

```bash
# Voir l'historique rebased
git log --oneline --graph --all -20
```

**Résultat attendu** :
```
* <nouveau-hash> (HEAD -> integration) feat: add PR models et update branch strategy
* <nouveau-hash> feat: supprimer les instructions de l'agent...
* <nouveau-hash> Add specialized agents for TDD workflow...
* <nouveau-hash> feat: add documentation for realease...
* 598a29f (origin/main, main) Release 0.3.0 (#26)  ← BASE COMMUNE
* ...
```

**Points importants** :
- ✅ Les commits de `integration` ont de **nouveaux hashes** (normal après rebase)
- ✅ Ils sont **au-dessus** du commit `598a29f` de `main`
- ✅ Il n'y a **plus de divergence** entre `main` et `integration`

---

### Étape 5 : Forcer le Push sur `integration`

⚠️ **ATTENTION** : Vous allez réécrire l'historique de `origin/integration`.

**Important** : Assurez-vous que **personne d'autre ne travaille** sur `integration` en ce moment.

```bash
# Forcer le push (réécrit l'historique distant)
git push origin integration --force-with-lease
```

**`--force-with-lease`** est plus sûr que `--force` : il vérifie que personne n'a pushé entre-temps.

---

### Étape 6 : Vérifier sur GitHub

1. Allez sur `https://github.com/RastaChaum/Intelligent-Heating-Pilot`
2. Regardez l'historique de `integration`
3. **Vérifier** :
   - Les nouveaux commits sont présents
   - L'historique est aligné avec `main`
   - Pas de divergence

---

### Étape 7 : Nettoyer le Backup

Une fois que tout fonctionne correctement :

```bash
# Supprimer la branche de backup locale
git branch -D integration-backup

# Si vous l'aviez pushée (optionnel)
git push origin --delete integration-backup
```

---

## 🎯 Résultat Final

Après cette procédure :

```
main:        ... → 598a29f (Release 0.3.0)
                       ↓
integration: ... → 598a29f → b201fb5' → 9da40c8' → ... (nouveaux commits)
```

**Avantages** :
- ✅ Historiques alignés
- ✅ Plus de divergence
- ✅ Prêt pour le workflow correct (merge commits)
- ✅ Tous les commits préservés

---

## 🚨 Troubleshooting

### Problème : "Cannot rebase: You have unstaged changes"

**Solution** :
```bash
# Sauvegarder les modifications en cours
git stash

# Faire le rebase
git rebase main

# Récupérer les modifications
git stash pop
```

---

### Problème : Trop de conflits pendant le rebase

**Option 1 : Annuler et utiliser la méthode alternative**
```bash
git rebase --abort
```

**Option 2 : Recréer integration depuis main (voir section alternative ci-dessous)**

---

### Problème : "force-with-lease" échoue

**Solution** :
```bash
# Si vous êtes certain qu'il n'y a pas de travail distant à perdre
git push origin integration --force
```

⚠️ Utilisez `--force` seulement si vous êtes **absolument certain**.

---

## 🔄 Méthode Alternative : Recréer `integration`

Si le rebase est trop complexe ou échoue, vous pouvez **recréer** `integration` :

### Procédure

```bash
# 1. Identifier les commits à préserver
git log v0.3.0..integration --oneline > commits-to-preserve.txt

# 2. Sauvegarder les fichiers modifiés
git checkout integration
git diff main > integration-changes.patch

# 3. Supprimer integration locale
git checkout main
git branch -D integration

# 4. Recréer integration depuis main
git checkout -b integration main

# 5. Appliquer les modifications
git apply integration-changes.patch

# 6. Créer un nouveau commit (ou plusieurs si nécessaire)
git add .
git commit -m "feat: reapply integration changes after realignment

Includes:
- PR templates and branching strategy
- Specialized agents for TDD workflow
- Documentation updates

Original commits: b201fb5, 9da40c8, 62d2d56, dbf774e"

# 7. Forcer le push
git push origin integration --force
```

**Inconvénient** : Perd l'historique granulaire (mais le contenu est préservé).

---

## 📋 Checklist de Vérification

Après réalignement, vérifiez :

- [ ] `git log main..integration` montre les nouveaux commits uniquement
- [ ] `git log integration..main` ne montre rien (pas de divergence)
- [ ] `git diff main integration` montre les différences attendues
- [ ] Les tags (v0.3.0) sont présents dans les deux branches
- [ ] L'historique sur GitHub est cohérent
- [ ] Vous pouvez créer une PR de `integration` vers `main` sans conflit

---

## 🎓 Prévention Future

Pour éviter ce problème à l'avenir :

✅ **Toujours utiliser merge commit** pour `integration` → `main`  
✅ **Toujours utiliser squash merge** pour `feature/*` → `integration`  
✅ **Ne jamais rebase** `integration` après merge vers `main`  
✅ **Synchroniser** `integration` avec `main` après chaque release :

```bash
git checkout integration
git merge main --ff-only  # Fast-forward uniquement
git push origin integration
```

---

## 🚀 Prochaines Étapes

Après réalignement réussi :

1. **Créer une branche de test** : `git checkout -b test/workflow-verification`
2. **Tester le workflow** : Ouvrir une PR test vers `integration`
3. **Valider** : Vérifier que tout fonctionne
4. **Continuer** : Reprendre le développement normalement

---

**Besoin d'aide ?** Consultez les logs détaillés avec `git log --graph --all --oneline --decorate` pour comprendre l'état actuel.
