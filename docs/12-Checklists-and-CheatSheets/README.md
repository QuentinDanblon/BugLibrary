# 12 — Checklists & CheatSheets

Index des checklists actionnables de ce dépôt. Chaque checklist est conçue pour être suivie en conditions réelles, pas lue une fois puis oubliée.

## Checklists disponibles

| Fichier | Usage |
|---|---|
| [`Recon-Checklist.md`](Recon-Checklist.md) | Cartographie de surface d'attaque complète avant de commencer les tests actifs |
| [`Web-Checklist.md`](Web-Checklist.md) | Passage systématique sur une application web (toutes catégories OWASP + business logic) |
| [`API-Checklist.md`](API-Checklist.md) | Passage systématique sur une API REST/GraphQL |

## Checklist "avant de soumettre un rapport" (universelle)

- [ ] La vulnérabilité est-elle strictement dans le scope écrit du programme ?
- [ ] Ai-je testé avec des comptes de test, jamais des comptes/données réels de tiers ?
- [ ] Ai-je démontré un impact concret, pas juste une exécution de payload isolée (`alert(1)` seul ne suffit jamais) ?
- [ ] Ai-je vérifié qu'il ne s'agit pas d'un comportement documenté comme accepté/exclu par le programme ?
- [ ] Mes étapes de reproduction sont-elles exécutables telles qu'écrites, sans étape implicite manquante ?
- [ ] Ai-je inclus les requêtes/réponses HTTP brutes en preuve, pas seulement des captures d'écran ?
- [ ] Ma sévérité est-elle justifiée par un score CVSS calculé, pas juste affirmée ?
- [ ] Ai-je nettoyé tout artefact de test laissé sur la cible (fichiers uploadés, comptes créés, données injectées) ?
- [ ] Ai-je vérifié qu'un rapport similaire n'existe pas déjà dans mon propre historique sur ce programme ?
- [ ] Le titre décrit-il précisément la classe de vuln, la localisation, et l'impact principal ?

## Checklist "premier jour sur un nouveau programme"

- [ ] Lire le scope complet (in/out) + toutes les exclusions listées.
- [ ] Consulter la Hacktivity/historique de rapports publics pour calibrer le niveau accepté.
- [ ] Identifier l'âge du programme et la fréquence de mise à jour du scope.
- [ ] Repérer les technologies annoncées (job postings, changelog, headers serveur).
- [ ] Vérifier les règles spécifiques de rate limiting / types de test autorisés.
- [ ] Identifier les canaux de contact en cas d'ambiguïté (email sécurité, formulaire dédié).
- [ ] Démarrer la reconnaissance passive avant toute action active (voir [`Recon-Checklist.md`](Recon-Checklist.md)).
