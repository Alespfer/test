---
title: Note de recherche fictive — Méthodologie de scellement itératif
author: Alberto Esperón
date: 2026-06-18
status: draft
asset_type: savoir_faire
context: Document jetable créé pour la vague de tests SESHAT 1.4.x sur projet `test`. Aucune valeur de recherche réelle.
---

# Méthodologie de scellement itératif — note de travail

## 1. Hypothèse

Dans le cadre d'un cycle de développement court, le scellement d'un livrable
peut être réalisé soit en bout de chaîne (single seal du repo final), soit
en pas-à-pas (un seal par commit significatif).

L'hypothèse testée ici est que le **pas-à-pas** offre une meilleure
auditabilité fiscale (chaque effort R&D est attaché à un certificat eIDAS
daté individuellement) au prix d'une charge cognitive de validation accrue
pour l'utilisateur (chaque seal requiert un dry_run + une validation).

## 2. Variables observées

- **t_seal** : temps moyen entre la complétion d'un commit et son scellement.
- **n_orphelins** : nombre de sceaux dont `ipsecure_contribution_id` est
  resté `null` après l'opération (cf. F-NEW-4 sur la déconnexion silencieuse).
- **ratio_pending** : `pending_attestations / total_records` au moment de la
  consultation du dashboard.

## 3. Protocole

Pour chaque itération de développement :
1. Préparer un script Python isolé (pas de dépendance hors stdlib).
2. Le commiter avec un message conforme à la convention `<type>(<scope>): <desc>`.
3. Pousser sur le remote `origin/main` avant le sceau (réflexe #5).
4. Sceller le commit avec `category: CODE` et `asset_types: ["logiciel"]`.
5. Noter le `ledger_id` et le `ipsecure_contribution_id` retournés.

À la fin des N itérations, un `seal type:repo` figera l'état global.

## 4. Limites assumées

- Ce document est lui-même un mock — sa description eIDAS ne doit pas être
  considérée comme une revendication d'antériorité scientifique.
- Le projet `test` est volontairement isolé du projet `wisenomy` pour ne pas
  contaminer le ledger productif avec des entrées de validation.
