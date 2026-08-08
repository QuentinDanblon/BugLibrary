# Template de Notes de Reconnaissance / Recon Notes Template

> Une instance par cible/programme. Structure pensée pour être réutilisée à chaque nouvelle session sans redécouvrir ce qui est déjà connu. Voir méthodologie : [`docs/02-Reconnaissance`](../docs/02-Reconnaissance/README.md).

---

## Cible

- **Programme :** [nom]
- **Plateforme :** [HackerOne / Bugcrowd / Intigriti / Programme privé / VDP]
- **Date de dernière mise à jour de ces notes :** [YYYY-MM-DD]
- **Scope résumé :** [domaines/apps in-scope]
- **Exclusions clés :** [self-XSS, clickjacking sans impact, etc.]

## Inventaire des assets

| Asset | Type | Statut | Techno détectée | Priorité (1-10) | Notes |
|---|---|---|---|---|---|
| `app.target.com` | Web app | Actif | React + Node/Express | 8 | Panel utilisateur, upload avatar |
| `api.target.com` | API REST | Actif | Express, Swagger exposé | 9 | `/v1/` et `/v2/` actifs simultanément |
| `staging.target.com` | Web app | Actif | Identique à prod | 9 | Moins de couverture probable |

## Sous-domaines découverts (log incrémental)

```
[Date] nouveau sous-domaine trouvé : xxx.target.com — source : subfinder
[Date] nouveau sous-domaine trouvé : yyy.target.com — source : ctfr monitoring
```

## Endpoints identifiés

| Endpoint | Méthode | Auth requise | Description | Testé ? |
|---|---|---|---|---|
| `/api/v2/user/{id}` | GET | Oui | Profil utilisateur | ☐ |
| `/api/v2/orders/{id}/invoice` | GET | Oui | Facture de commande | ☐ |

## Secrets / fuites identifiées (JS, GitHub, sourcemaps)

*Toujours vérifier la validité avant tout usage — ne jamais utiliser une clé/token réel trouvé sans autorisation explicite du programme couvrant ce cas.*

| Type | Localisation | Valide ? | Action prise |
|---|---|---|---|
| API key Stripe test | `bundle.min.js` ligne X | Non vérifié | À signaler si sensible, ne pas utiliser |

## Hypothèses en cours (voir 01-Mindset-and-Methodology)

| Hypothèse | Statut | Résultat |
|---|---|---|
| L'endpoint `/orders/{id}/invoice` est probablement vulnérable à un IDOR (ID séquentiel observé) | En test | — |

## Historique de sessions

| Date | Durée | Focus | Résultat |
|---|---|---|---|
| [YYYY-MM-DD] | 2h | Recon passive complète | Liste initiale d'assets établie |
