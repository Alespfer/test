---
title: Note de recherche fictive — Évaluation des correctifs SESHAT 1.5.4
author: Alberto Esperón
date: 2026-06-19
status: draft
asset_type: savoir_faire
context: Document jetable créé pour la vague 2 de tests SESHAT sur projet `test`. Évalue les correctifs apportés par 1.5.4 suite aux rapports #48–#53 du 2026-06-18. Aucune valeur de recherche réelle.
---

# Évaluation des correctifs 1.5.4 — note de travail

## 1. Objet

Reprise du protocole de test SESHAT du 2026-06-18 sur la nouvelle version 1.5.4
publiée par le mainteneur après nos rapports #48–#53. L'objectif est de mesurer,
à protocole identique, la part des frictions corrigées et celles qui persistent.

## 2. Frictions à observer en priorité

- **F-NEW-11 (rapport #48, critique)** — la confusion soumission vs certification
  eIDAS est-elle levée dans `seal_file` (`ipsecure_status`), `fetch_certificate`,
  `sync`, et le dashboard ?
- **F-NEW-8 (rapport #49, haute)** — déjà confirmée corrigée en lecture schéma
  (colonne `sealed_path` présente).
- **F-NEW-9 (rapport #50, moyenne)** — `commit_sha` est-il correctement populé
  même après retry ?
- **F-NEW-10 (rapport #51, moyenne)** — le hook post-commit propage-t-il son
  échec ? La paire (`file:` + `commit:`) est-elle systématique ?
- **F-NEW-12 (rapport #52, mineure)** — le warning « plaintext secrets » est-il
  dédupliqué ?
- **F-NEW-13 (rapport #53, mineure)** — `seshat configure <action>` est-il
  désormais exposé en CLI ?

## 3. Protocole

Identique à celui du 2026-06-18 : 3 mocks scellés, 3 itérations de code, 1 repo
seal final. Les mocks sont volontairement nommés avec le suffixe `_20260619`
pour ne pas écraser ceux de la vague précédente et préserver la traçabilité.

## 4. Limites

Ce document est lui-même un mock. Sa description eIDAS ne doit pas être
considérée comme une revendication d'antériorité scientifique. Le périmètre
de la vague est strictement la chaine SESHAT — les frictions Jinnove (côté
serveur eIDAS) restent hors-périmètre tant qu'on n'a pas la confirmation de
leur résolution côté support.
