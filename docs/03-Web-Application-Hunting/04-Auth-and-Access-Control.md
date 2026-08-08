# Auth & Access Control — IDOR, Broken Auth, JWT, OAuth

## Contexte

C'est la catégorie **la plus rentable en volume** pour un hunter avancé : IDOR (Insecure Direct Object Reference) et Broken Access Control représentent la majorité des rapports critiques payés sur les programmes matures, car ils demandent une compréhension fonctionnelle plutôt qu'un payload générique — les scanners automatiques les ratent presque toujours.

## IDOR — Insecure Direct Object Reference

### Comment tester

```
1. Cartographier CHAQUE endpoint qui référence un objet par ID (numérique, UUID, slug).
2. Créer DEUX comptes de test (A et B) avec des rôles/tenants différents si possible.
3. Pour chaque endpoint, remplacer l'ID de A par un ID appartenant à B, en utilisant le token/session de A.
4. Tester dans les DEUX sens (lecture ET écriture/suppression).
5. Tester aussi les endpoints indirects : exports, notifications, webhooks, IDs dans des réponses imbriquées (ex: commande contient un ID de facture référençable séparément).
```

**Matrice de test systématique :**

| Méthode | Scénario | Résultat attendu (sécurisé) |
|---|---|---|
| GET | Token A → ressource de B | 403/404 |
| PUT/PATCH | Token A → modifier ressource de B | 403 |
| DELETE | Token A → supprimer ressource de B | 403 |
| POST (création liée) | Token A → créer une ressource liée au tenant de B | 403 |
| Requête batch/bulk | IDs mixtes A+B dans un même appel | Filtrage correct par ownership |

> 💡 **Pro tip d'élite :** Ne teste pas uniquement les IDs "voisins" (id+1/id-1). Beaucoup d'IDOR se cachent dans des **IDs secondaires peu évidents** : `invoice_id` référencé dans une réponse d'API `order`, `session_id` dans un export CSV, `family_member_id` dans une app santé/finance familiale. Cartographie tous les identifiants qui apparaissent dans TOUTE réponse JSON, pas seulement l'URL.

### IDOR sur identifiants non-devinables (UUID) — toujours tester quand même

Même avec un UUID v4 (non énumérable), l'IDOR reste exploitable si :
- L'UUID d'un autre utilisateur **fuite** ailleurs (réponse API d'un endpoint public, notification, export partagé, historique de commande visible par un tiers via un autre bug).
- L'application permet l'énumération via un canal annexe (recherche, autocomplete qui retourne des UUID).

> 💡 Automatise la collecte de tous les identifiants observés durant une session de navigation normale (proxy Burp + extension custom ou script) — tu construis ainsi une base d'IDs "appartenant à d'autres utilisateurs" sans même les avoir devinés.

### Mass Assignment (proche cousin de l'IDOR)

```json
// Requête légitime de mise à jour de profil
{"name": "John", "email": "john@test.com"}

// Test mass assignment — ajouter des champs non documentés
{"name": "John", "email": "john@test.com", "role": "admin", "isVerified": true, "balance": 999999}
```
> 💡 Récupère la liste complète des champs possibles via le schéma GraphQL (introspection), la doc Swagger, ou en observant les réponses GET du même objet (qui exposent souvent plus de champs que le formulaire PUT n'en attend).

## Broken Authentication

| Vecteur | Test |
|---|---|
| Absence de rate limiting sur login | Brute-force avec Turbo Intruder — mesurer le nombre de tentatives avant lockout/captcha |
| Absence de rate limiting sur OTP/2FA | Brute-force du code OTP (souvent 4-6 chiffres = 10⁴-10⁶ possibilités) |
| Reset de mot de passe — token prévisible | Analyser l'entropie du token (timestamp-based ? séquentiel ?) |
| Reset de mot de passe — pas d'invalidation de session existante | Vérifier si les sessions actives restent valides après un reset (devrait toutes être invalidées) |
| "Remember me" avec token faible | Décoder/analyser le cookie persistant |
| Enumération d'utilisateurs | Différence de message/timing entre "email inexistant" et "mauvais mot de passe" |
| Session fixation | Vérifier si le session ID est régénéré après login (sinon, fixation possible) |

## JWT — JSON Web Token Attacks (2024-2026)

```
1. Décoder le JWT (jwt.io ou manuellement) — examiner header, payload, algorithme.

2. Algorithm confusion (alg=none) :
   - Modifier le header en {"alg":"none"}, supprimer la signature, tester si accepté.

3. Algorithm confusion (RS256 → HS256) :
   - Si l'app utilise RS256 (clé publique/privée) mais accepte aussi HS256,
     re-signer le token avec HS256 en utilisant la CLÉ PUBLIQUE comme secret HMAC.
   - Outil : jwt_tool (`python3 jwt_tool.py <token> -X k -pk public_key.pem`)

4. Clé faible / brute-forçable (HS256) :
   - jwt_tool ou hashcat avec une wordlist contre le secret HMAC.

5. kid (Key ID) injection :
   - Si le header contient "kid", tester l'injection SQL/path traversal dans ce champ
     si l'app va chercher la clé depuis un fichier/DB en utilisant "kid" tel quel.

6. jku/x5u header injection :
   - Si le header contient "jku" (JWK Set URL) ou "x5u", héberger sa propre clé
     publique sur un serveur contrôlé et pointer le header vers cette URL.

7. Absence de vérification d'expiration (exp) ou de "nbf".

8. Confusion de type ("typ" manipulation, JWT utilisé comme JWE, etc.)
```

> 💡 **Pro tip d'élite :** Beaucoup d'implémentations 2024-2026 utilisent des librairies modernes déjà résistantes à `alg=none`, mais restent vulnérables à la confusion RS256/HS256 si le développeur n'a pas explicitement restreint les algorithmes acceptés (`jwt.verify(token, key, {algorithms: ['RS256']})` — l'oubli de cette restriction est très fréquent).

## OAuth / SSO Misconfigurations

| Vecteur | Test |
|---|---|
| `redirect_uri` mal validé | Tester des variantes : sous-domaine contrôlé, path traversal (`https://trusted.com/../evil.com`), wildcard ouvert |
| État CSRF manquant sur le flow OAuth | Vérifier la présence et la validation du paramètre `state` |
| Confusion d'audience de token | Un token émis pour l'App A est-il accepté par l'App B (même émetteur) ? |
| Account linking sans vérification d'email | Lier un compte OAuth tiers à un compte existant sans re-vérifier la propriété de l'email |
| Authorization Code interception | Flow implicite (deprecated) encore utilisé — le code/token apparaît dans l'URL/historique navigateur |
| PKCE absent sur client public (mobile/SPA) | Permet l'interception du code d'autorisation par une app malveillante sur le même device |

## Privilege Escalation (verticale/horizontale)

- **Verticale** : utilisateur standard → admin (endpoints admin non protégés côté serveur, juste cachés côté front).
- **Horizontale** : utilisateur A → données/actions de l'utilisateur B (recoupe l'IDOR).
- **Force browsing** d'endpoints admin non liés dans l'UI mais actifs côté serveur (`/admin/api/...`, `/internal/...`) — souvent découverts via le JS bundle ou la doc API exposée.

## Comment confirmer l'impact

- Démonstration bout-en-bout avec deux comptes de test distincts (jamais des comptes réels tiers).
- Capture d'écran/vidéo montrant : login en tant que A → accès à une ressource strictement liée à B → preuve de lecture ou modification.
- Pour JWT/OAuth : preuve de forge d'un token valide, utilisé pour accéder à une ressource protégée.

## Références

- PortSwigger Web Security Academy — Access control, JWT attacks, OAuth
- OWASP API Security Top 10 (BOLA/IDOR = #1 récurrent)
- `jwt_tool` (ticarpi) documentation
- HackTricks — JWT, OAuth vulnerabilities
