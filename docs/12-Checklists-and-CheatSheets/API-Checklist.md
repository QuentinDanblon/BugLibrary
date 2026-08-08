# Checklist — API & GraphQL Hunting

Passage systématique. Voir détail technique : [`04-API-GraphQL-Hunting`](../04-API-GraphQL-Hunting/README.md).

## Découverte & Inventaire

- [ ] Documentation exposée récupérée (`swagger.json`, `openapi.yaml`, `/api-docs`)
- [ ] Toutes les versions actives identifiées (`/v1/`, `/v2/`, `/v3/`) — anciennes versions testées aussi
- [ ] Endpoints extraits du trafic mobile croisés avec ceux documentés (endpoints "cachés")
- [ ] Collections Postman/Insomnia exposées publiquement recherchées

## OWASP API Top 10 — passage systématique

- [ ] API1 — BOLA/IDOR testé sur chaque endpoint avec objet référencé par ID
- [ ] API2 — Authentification testée (tokens faibles, absence de rotation, rate limit)
- [ ] API3 — Mass assignment / over-fetching testé (champs non documentés acceptés/exposés)
- [ ] API4 — Absence de pagination/limite testée (requêtes coûteuses répétables sans limite)
- [ ] API5 — Endpoints admin testés avec un rôle standard (function level auth)
- [ ] API6 — Flows métier sensibles testés pour abus en masse (achat, création de compte)
- [ ] API7 — SSRF testé sur tout champ acceptant une URL côté API
- [ ] API8 — CORS, headers de sécurité, méthodes HTTP non désactivées vérifiés
- [ ] API9 — Environnements de staging/dev/versions oubliées recherchés
- [ ] API10 — Validation des données consommées depuis des APIs tierces vérifiée

## GraphQL spécifique

- [ ] Introspection testée (`__schema`) — si désactivée, field suggestion/brute-force testés
- [ ] Batching attack testé pour bypass de rate limiting (login/OTP)
- [ ] Query depth/complexity abuse testé (requêtes imbriquées profondes)
- [ ] Alias-based rate limit bypass testé
- [ ] Field-level authorization testé (champ imbriqué accessible malgré query top-level restreinte)
- [ ] CSRF sur mutations testé si GET ou Content-Type flexible accepté

## gRPC / WebSocket (si applicable)

- [ ] Réflexion gRPC testée (`grpcurl list`) pour fuite de structure interne
- [ ] Fichiers `.proto` recherchés dans repos publics/fuites
- [ ] Validation d'origine WebSocket testée (CSWSH)
- [ ] Ré-authentification testée sur connexion WebSocket longue durée après révocation

## Avant de conclure

- [ ] Chaque vulnérabilité candidate testée dans les deux sens (lecture ET écriture/suppression)
- [ ] Impact chaîné évalué (ex: BOLA + absence de rate limit = account takeover de masse)
