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

### Lancer le code

```bash
python3 main.py
```

Aucune dépendance, aucun framework de test, aucun linter configurés.
`python3 -c "import ast, pathlib; [ast.parse(p.read_text()) for p in pathlib.Path('.').glob('*.py')]"` suffit comme check syntaxique.

### Workflow git

- `core.hooksPath` est positionné sur `.githooks/` (config locale, à reposer à chaque clone).
- Chaque `git commit` déclenche `.githooks/post-commit` qui appelle
  `seshat seal commit <sha> -p test` en arrière-plan. Les logs vont dans
  `.git/seshat-seal.log` (non versionné).
- Le seal est **non bloquant** : un échec côté Seshat n'annule pas le commit.

## SESHAT - Protection IP

Ce projet utilise SESHAT pour le scellement et la protection des actifs IP.

### Règle projet — scellement automatique des commits

**Tout commit créé dans ce repo doit être scellé via SESHAT immédiatement après le `git commit`, sans demander confirmation au développeur.**

- Après chaque `git commit` réussi : appeler `seal(project="test", type="commit", ref="<sha>")` directement avec `dry_run: false`.
- Cette règle **annule** l'invariant n°3 « `dry_run` obligatoire avant eIDAS » ci-dessous **pour le type `commit` uniquement**. Les autres types (`pr`, `tag`, `release`, `seal_file`, `certify_research`) gardent le flux preview + confirmation.
- Les invariants n°1 (secret scan) et n°2 (authorship) restent applicables : un `secret_scan_blocked` doit toujours être remonté à l'utilisateur avant tout `force_secret_scan`.
- Si le seal échoue, ne pas relancer le commit ; rapporter l'erreur à l'utilisateur.

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

**Pour configurer des defaults permanents:**
```
configure(action="update_project", project_id="test",
         default_asset_types=["logiciel"], default_objective="Mon objectif R&D")
```

### Outils SESHAT disponibles (tous appelables via MCP)

| Outil | Usage | Exemple |
|-------|-------|---------|
| **status** | Vérifier l'état du système (git host, Notion, Jira, IP Secure). **Appeler en premier.** | `status(verbose=true)` |
| **seal** | Sceller commit, PR mergée, tag, release, ou issue Jira | `seal(project="test", type="pr", ref="42")` |
| **certify_research** | Certifier notes Obsidian, Notion et/ou worklogs Jira | `certify_research(project="test", dry_run=true)` |
| **effort_report** | Rapport R&D (summary, detailed, valorisation, markdown, dossier) | `effort_report(project="test", format="valorisation")` |
| **export_proofs** | Exporter les preuves en Markdown, JSON ou CSV (audit, INPI, avocats) | `export_proofs(project="test", output_path="./preuves", format="markdown")` |
| **bundle_release** | Dossier complet pour dépôt légal (ZIP + rapport + chaîne de preuves) | `bundle_release(project="test", tag="v1.0.0")` |
| **annotate** | Qualifier rétroactivement une entrée (objectif, asset_types) | `annotate(id=42, objective="Mon objectif R&D")` |
| **batch_annotate** | Qualifier en lot (1-100 entrées, mêmes métadonnées) | `batch_annotate(ids=[1,2,3], asset_types=["logiciel"])` |
| **budget_alerts** | Détecter dépassements, oublis de saisie, drift Jira | `budget_alerts(project="test")` |
| **configure** | Configurer projets, git host, defaults, Notion, Jira | `configure(action="update_project", project_id="test", ...)` |
| **report_issue** | Signaler un bug ou suggestion au mainteneur SESHAT | `report_issue(type="bug", title="...", description="...")` |

**Règle** : Toujours utiliser `dry_run=true` pour prévisualiser avant seal/certify_research.

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

Pour ajouter une source :
```
configure(action="update_project", project_id="test",
         notion_database_id="<URL ou UUID>",
         jira_project_key="PROJ")
```

### Modifier les defaults

```
configure(action="update_project", project_id="test",
         default_asset_types=["logiciel", "base_donnees"],
         default_objective="Optimisation performance API")
```

---
