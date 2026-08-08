# 04 — API, GraphQL & gRPC Hunting

## Contexte

Les APIs (REST, GraphQL, gRPC, WebSocket) sont la surface d'attaque dominante des applications modernes (mobile-first, SPA, microservices). L'OWASP API Security Top 10 (2023) reflète cette réalité : **BOLA (Broken Object Level Authorization) est la vulnérabilité API #1** — c'est l'IDOR appliqué aux APIs.

## REST API Hunting

### Découverte et cartographie

```
1. Récupérer toute doc exposée : /swagger.json, /openapi.yaml, /api-docs, /v3/api-docs
2. Importer dans Postman/Insomnia pour générer une collection testable automatiquement
3. Comparer les versions d'API actives (/v1/, /v2/, /v3/) — les anciennes versions
   sont souvent moins maintenues en sécurité mais toujours actives en production
4. Extraire les endpoints depuis le trafic mobile (voir 05-Mobile-Hunting)
```

### OWASP API Security Top 10 (2023) — grille de test

| # | Catégorie | Test rapide |
|---|---|---|
| API1 | Broken Object Level Authorization (BOLA/IDOR) | Cross-account object ID substitution — voir 03/04-Auth-and-Access-Control |
| API2 | Broken Authentication | Tokens faibles, absence de rotation, endpoints d'auth sans rate limit |
| API3 | Broken Object Property Level Authorization | Mass assignment, exposition de champs sensibles non filtrés dans la réponse (over-fetching) |
| API4 | Unrestricted Resource Consumption | Absence de pagination/limite → DoS applicatif, requêtes coûteuses répétées sans rate limit |
| API5 | Broken Function Level Authorization | Endpoints admin accessibles avec un rôle standard (force browsing sur verbes/routes) |
| API6 | Unrestricted Access to Sensitive Business Flows | Abus d'achat en masse, de création de compte en masse, absence de CAPTCHA/anti-bot sur flow sensible |
| API7 | Server Side Request Forgery | Voir 03/03-SSRF — webhooks, imports d'URL côté API |
| API8 | Security Misconfiguration | CORS trop permissif, verbose error, headers de sécurité manquants, méthodes HTTP non désactivées (`TRACE`, `PUT` sur des endpoints non prévus) |
| API9 | Improper Inventory Management | Versions d'API oubliées, environnements de staging/dev exposés, endpoints "internes" documentés mais publics |
| API10 | Unsafe Consumption of APIs | L'app fait confiance aveuglément à une API tierce (données non validées après ingestion) |

### CORS Misconfiguration — check rapide

```
# Tester la réflexion d'origine arbitraire
curl -H "Origin: https://evil.com" -I https://api.target.com/user/me

# Vulnérable si :
Access-Control-Allow-Origin: https://evil.com
Access-Control-Allow-Credentials: true
# → un site tiers peut lire les données authentifiées de la victime via fetch() avec credentials
```

> 💡 **Pro tip :** Teste aussi la réflexion de sous-domaines (`https://evil.target.com` si l'app fait un `.endsWith('.target.com')` sans validation stricte) et le bypass via `null` origin (sandboxed iframe, certains contextes `file://`).

### HTTP Method Override / Verb Tampering

```
X-HTTP-Method-Override: DELETE
X-Method-Override: DELETE
_method=DELETE (paramètre de formulaire)
```
Teste si un endpoint bloqué en `DELETE` direct devient accessible via override, contournant potentiellement des règles de firewall/proxy filtrant par méthode.

## GraphQL Hunting (spécifique)

### Introspection

```graphql
query IntrospectionQuery {
  __schema {
    types { name fields { name type { name } } }
    queryType { name }
    mutationType { name }
  }
}
```
Si activée en production → cartographie complète du schéma, y compris mutations/queries "cachées" non utilisées par le frontend officiel.

> 💡 **Pro tip :** Même quand l'introspection est désactivée, teste le **field suggestion** (erreurs qui révèlent des noms de champs proches — `Did you mean "userById"?`) et utilise des outils de **brute-force de schéma** (`clairvoyance`, `graphql-cop`) pour reconstruire le schéma sans introspection.

### Vulnérabilités spécifiques GraphQL

| Vulnérabilité | Description / Test |
|---|---|
| **Batching Attack** | Envoyer un tableau de multiples queries dans une seule requête pour contourner le rate limiting (limite comptée par requête HTTP, pas par opération) — utile pour brute-force OTP/login |
| **Query Depth / Complexity Abuse (DoS)** | Requêtes imbriquées profondément (`user{friends{friends{friends{...}}}}`) sans limite de profondeur/complexité → épuisement de ressources serveur |
| **Alias-based Rate Limit Bypass** | Utiliser des alias GraphQL pour répéter le même champ N fois dans une seule requête (`a1: login(...) a2: login(...) ...`) |
| **Field-level Authorization Bypass** | Une query autorisée peut exposer un champ imbriqué non censé être accessible à ce rôle (le contrôle d'accès n'est fait qu'au niveau query top-level, pas field-level) |
| **Injection via arguments** | Arguments de mutation/query passés bruts à une requête SQL/NoSQL backend — voir 03/02-SQLi |
| **CSRF sur mutations** (si GET autorisé ou Content-Type flexible) | Endpoint GraphQL acceptant `GET /graphql?query=...` ou un `Content-Type: text/plain` permissif → CSRF classique possible |

**Exemple de batching pour bypass rate limit login :**
```json
[
  {"query": "mutation{login(user:\"admin\",pass:\"pass1\"){token}}"},
  {"query": "mutation{login(user:\"admin\",pass:\"pass2\"){token}}"},
  ...
]
```

## gRPC & Protobuf Hunting

- Récupérer les fichiers `.proto` (souvent exposés par erreur dans des repos publics ou via réflexion gRPC activée : `grpcurl -plaintext target:port list`).
- Tester la réflexion gRPC active en production (`grpc.reflection.v1alpha.ServerReflection`) — fuite de la structure complète de l'API interne.
- Fuzzing de champs protobuf avec des types inattendus (types numériques hors bornes, chaînes malformées) via `ghz`, `grpcurl` scripté.

## WebSocket Hunting

- Vérifier l'absence de validation d'origine à l'établissement de la connexion (`Origin` header non vérifié) → Cross-Site WebSocket Hijacking (CSWSH).
- Injecter des payloads dans les messages échangés (mêmes classes de vuln que HTTP : injection, XSS si les messages sont rendus côté client sans échappement).
- Tester l'absence de ré-authentification sur connexion longue durée après révocation de session/token.

## Comment confirmer l'impact

- BOLA/BFLA : capture montrant l'accès cross-tenant/cross-role à une ressource ou fonction.
- CORS : PoC HTML hébergé démontrant l'exfiltration de données authentifiées cross-origin.
- GraphQL DoS : mesure du temps de réponse/charge serveur induite par une query complexe (sans la maintenir en charge soutenue au-delà du strict nécessaire à la preuve).

## Références

- OWASP API Security Top 10 (2023)
- PortSwigger Web Security Academy — GraphQL vulnerabilities, CORS
- `graphql-cop`, `InQL`, `clairvoyance` (outils GraphQL)
- PayloadsAllTheThings — GraphQL Injection
