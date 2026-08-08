# Checklist — Web Application Hunting

Passage systématique. Voir détail technique : [`03-Web-Application-Hunting`](../03-Web-Application-Hunting/README.md).

## Authentification & Sessions

- [ ] Rate limiting absent/faible sur login, reset password, OTP/2FA
- [ ] Enumération d'utilisateurs via message d'erreur ou timing différentiel
- [ ] Token de reset password prévisible (entropie, séquentialité)
- [ ] Sessions actives non invalidées après reset password/changement d'email
- [ ] Session ID non régénéré après login (fixation)
- [ ] JWT : `alg=none`, confusion RS256/HS256, `kid`/`jku`/`x5u` injection, clé faible

## Contrôle d'accès (IDOR / BOLA / BFLA)

- [ ] Chaque endpoint référençant un ID testé cross-compte (lecture ET écriture)
- [ ] IDs secondaires (invoice_id, session_id imbriqués) testés, pas seulement l'URL principale
- [ ] Endpoints admin testés avec un rôle standard (force browsing)
- [ ] Mass assignment testé sur tous les endpoints de mise à jour (champs non documentés)
- [ ] Export/notifications/webhooks vérifiés pour fuite d'IDs d'autres utilisateurs

## Injection

- [ ] SQLi testé sur tous les paramètres (GET/POST/headers/cookies/JSON imbriqué)
- [ ] NoSQL injection testée via query string ET body JSON (`$ne`, `$gt`, `$where`)
- [ ] SSTI testé sur tout champ pouvant alimenter un template (`{{7*7}}` et variantes)
- [ ] Command injection testée sur tout champ déclenchant un traitement serveur externe

## XSS & Client-Side

- [ ] Reflected/Stored testés avec canari contextuel sur tous les points d'entrée
- [ ] DOM XSS analysé via DOM Invader / audit des sinks (`innerHTML`, `eval`, etc.)
- [ ] CSP analysée (CSP Evaluator) pour whitelist dangereuse / directives manquantes
- [ ] postMessage listeners vérifiés pour absence de validation d'origine

## SSRF

- [ ] Tous les champs acceptant une URL testés (avatar, webhook, PDF gen, import)
- [ ] Bypass de filtre testés (représentations IP alternatives, DNS rebinding, redirection)
- [ ] Cloud metadata testé si SSRF confirmé (169.254.169.254, GCP/Azure équivalents)
- [ ] Blind SSRF confirmé via Collaborator/serveur DNS-HTTP contrôlé si pas de réponse visible

## Business Logic

- [ ] Race conditions testées sur coupon/paiement/inscription à quota limité (single-packet attack)
- [ ] Workflow multi-étapes testé pour saut d'étape / retour arrière après action irréversible
- [ ] Manipulation de prix/quantité côté client testée (négatif, virgule flottante, devise)
- [ ] Idempotency sur webhooks de paiement testée (rejouabilité)

## File Upload & Deserialization

- [ ] Bypass d'extension/MIME testé (double extension, polyglot, magic bytes)
- [ ] SVG upload testé pour XXE/XSS stockée si affiché inline
- [ ] Signature de sérialisation recherchée dans cookies/params (Java/PHP/.NET/Python/Node)
- [ ] Accès en lecture au fichier uploadé vérifié après upload (même si exécution bloquée)

## Configuration & Divers

- [ ] CORS testé pour réflexion d'origine arbitraire avec credentials
- [ ] Headers de sécurité vérifiés (CSP, X-Frame-Options, HSTS)
- [ ] Clickjacking testé si X-Frame-Options/CSP frame-ancestors absent
- [ ] Open redirect testé et évalué pour escalade (OAuth, SSRF bypass)
- [ ] Méthodes HTTP alternatives testées (verb tampering, override headers)

## Avant de conclure

- [ ] Chaque signal faible trouvé reconsidéré pour un chaînage possible (voir [`08-Advanced-Techniques`](../08-Advanced-Techniques/README.md))
- [ ] Impact business explicite formulé pour chaque vulnérabilité candidate à un rapport
