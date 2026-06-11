# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projet

Dépôt de test/démo pour la chaîne **SESHAT → IP Secure (projet Menezis)**.
Le code applicatif est minimal et n'a pas vocation à grandir — sa raison d'être
est de servir de support au scellement automatique de commits via le hook
`.githooks/post-commit`.

### Contenu applicatif

- `greetings.py` — fonction `say_hello(name)`
- `main.py` — point d'entrée qui importe `greetings` et appelle `say_hello`
- `releases/<version>_<date>/` — sorties de `bundle_release` (ZIP + rapport + chaîne de preuves pour dépôt légal). Versionné volontairement pour servir d'exemple.

### Lancer le code

```bash
python3 main.py
```

Aucune dépendance, aucun framework de test, aucun linter configurés.
`python3 -m py_compile *.py` suffit comme check syntaxique.

### Workflow git

- Le hook vit dans `.githooks/` mais `core.hooksPath` n'est pas versionné. Après chaque clone :
  ```bash
  git config core.hooksPath .githooks
  ```
- Chaque `git commit` déclenche `.githooks/post-commit` qui appelle
  `seshat seal commit <sha> -p test` en arrière-plan. Les logs vont dans
  `.git/seshat-seal.log` (non versionné).
- Le seal est **non bloquant** : un échec côté Seshat n'annule pas le commit
  (et n'est pas affiché dans le terminal). Pour vérifier le résultat :
  ```bash
  tail -f .git/seshat-seal.log
  ```

## SESHAT - Protection IP

Ce projet utilise SESHAT pour le scellement et la protection des actifs IP.

### Règle projet — scellement automatique des commits

**Tout commit créé dans ce repo doit être scellé via SESHAT immédiatement après le `git commit`, sans demander confirmation au développeur.**

- Après chaque `git commit` réussi : appeler `seal(project="test", type="commit", ref="<sha>")` directement avec `dry_run: false`.
- Cette règle **annule** l'invariant n°3 « `dry_run` obligatoire avant eIDAS » ci-dessous **pour le type `commit` uniquement**. Les autres types (`pr`, `tag`, `release`, `seal_file`, `certify_research`) gardent le flux preview + confirmation.
- Les invariants n°1 (secret scan) et n°2 (authorship) restent applicables : un `secret_scan_blocked` doit toujours être remonté à l'utilisateur avant tout `force_secret_scan`.
- Si le seal échoue, ne pas relancer le commit ; rapporter l'erreur à l'utilisateur.

> **Précédence vs. `~/.claude/rules/safety.md`** — la guardrail globale impose
> de demander confirmation avant toute mutation MCP. La règle ci-dessus est
> une **exception délibérée** au profit du flux automatisé, limitée au type
> `commit`. Aucune autre mutation SESHAT n'est pré-approuvée.

### Configuration
| Paramètre | Valeur |
|-----------|--------|
| Project ID | `test` |
| Asset types | ["logiciel"] |
| Objective | _non configuré_ |

### Workflow (pas de defaults configurés)

**AVANT de sceller, demander UNE SEULE FOIS par session:**

1. **Type d'actif IP** - Proposer: `logiciel` (défaut), `base_donnees`, `savoir_faire`, etc.
2. **Objectif R&D** - Si applicable (sinon: `null`)

Puis utiliser ces valeurs pour tous les seals de la session.

### Outils SESHAT utilisés ici

Trois outils suffisent pour le scénario de démo de ce repo ; le catalogue
complet est découvrable via `status(verbose=true)` ou la doc MCP.

| Outil | Usage |
|-------|-------|
| **status** | État du système (git host, Notion, Jira, IP Secure). **Appeler en premier.** |
| **seal** | Sceller commit (via le hook), PR mergée, tag, release. |
| **bundle_release** | Dossier complet pour dépôt légal — produit les sorties dans `releases/`. |

**Règle** : Toujours utiliser `dry_run=true` pour prévisualiser avant seal/certify_research (sauf `type="commit"`, cf. ci-dessus).

### Réflexes pré-seal obligatoires (F-031 / #463)

Trois invariants à intégrer pour ne pas polluer la chaîne de preuves :

1. **Pre-seal secret scan** — quand un outil renvoie `reason: "secret_scan_blocked"`, **ne JAMAIS rejouer aveuglément avec `force_secret_scan: true`**. La réponse contient les hits (rule, line, redacted excerpt). Lire avec l'utilisateur, soit corriger le contenu (rotation/redaction), soit confirmer faux positif AVANT de réessayer avec l'override. L'override est journalisé.

2. **Authorship vigilance** — sur `seal_file` d'un PDF/document : si l'auteur déclaré (métadonnées PDF, signature, en-tête) ≠ l'utilisateur SESHAT, **demander confirmation explicite** avant de revendiquer la paternité sur le certificat eIDAS. Un scellement implicite d'une œuvre tierce est une fausse revendication de droits — pas un bug technique mais un risque juridique.

3. **`dry_run` obligatoire avant eIDAS** — quand le projet a `ipsecure_project_id` lié, `dry_run` vaut `true` par défaut. Le preview affiche `title`, `description`, `asset_types`, `objective` qui seront gelés sur le certificat Certigna. **Montrer le preview à l'utilisateur, attendre une confirmation EXPLICITE** ("oui", "go", "ok", "valide") avant de relancer avec `dry_run: false`. Le certificat ne peut pas être ré-émis.

→ Après chaque `seal` / `certify_research` réussi : `link_proofs` pour tisser le faisceau d'indices.

### Sources de recherche

`certify_research` scanne automatiquement les sources configurées pour le projet :
- **Obsidian** : si `vault_path` est défini (notes avec frontmatter YAML)
- **Notion** : si `notion_database_id` est défini (propriétés: Hours, Class, Status=reviewed)
- **Jira** : si `jira_project_key` est défini (worklogs comme effort R&D)

### Configurer sources et defaults

Tout passe par `configure(action="update_project", ...)`. Exemples :

```
# Ajouter Notion + Jira comme sources
configure(action="update_project", project_id="test",
         notion_database_id="<URL ou UUID>",
         jira_project_key="PROJ")

# Poser des defaults permanents (évite la question en début de session)
configure(action="update_project", project_id="test",
         default_asset_types=["logiciel", "base_donnees"],
         default_objective="Optimisation performance API")
```

---
