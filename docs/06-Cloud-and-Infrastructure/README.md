# 06 — Cloud & Infrastructure Hunting

## Contexte

Le cloud misconfig est l'une des catégories à plus fort impact (accès direct à des données de production, voire compromission complète d'un compte cloud) et à volume croissant avec l'adoption massive de l'IaC (Infrastructure as Code) souvent mal auditée.

## AWS

### S3 Buckets

```bash
# Énumération de noms probables
cloud_enum -k target -k target-prod -k target-dev -k target-staging -k target-backup -k target-assets

# Vérification manuelle de permissions
aws s3 ls s3://bucket-name --no-sign-request           # lecture anonyme ?
aws s3 cp test.txt s3://bucket-name/ --no-sign-request  # écriture anonyme ?
aws s3api get-bucket-acl --bucket bucket-name --no-sign-request
```

| Misconfiguration | Impact |
|---|---|
| Lecture publique (`ListBucket`/`GetObject` ouverts) | Exfiltration de données (backups, logs, PII, code source) |
| Écriture publique (`PutObject` ouvert) | Upload malveillant, potentiel stored XSS si le bucket sert du contenu web, ou pollution de pipeline CI/CD si le bucket est une source de build |
| Bucket policy trop permissive sur des rôles cross-account | Accès non prévu par un compte AWS tiers |
| Bucket takeover (référence DNS/CNAME vers un bucket supprimé) | Voir Subdomain Takeover ci-dessous |

### IAM Misconfigurations

- Policies avec `"Action": "*", "Resource": "*"` attachées à des rôles à faible privilège attendu.
- Trust policies de rôle assumable trop larges (`"Principal": "*"` ou un compte AWS externe non prévu).
- Clés d'accès IAM long-terme fuitées dans du code public, des configs, des variables d'environnement exposées (`.env` accessible, panneau debug Django/Flask ouvert).

### Lambda / Serverless

- Variables d'environnement contenant des secrets, accessibles via une fonction vulnérable (SSRF/RCE dans le code de la fonction elle-même).
- IAM role de la fonction Lambda trop permissif — confirmer via SSRF (voir 03/03) si applicable au contexte serverless.

## GCP

- **Firebase mal configuré** — Realtime Database / Firestore avec règles de sécurité par défaut (`".read": true, ".write": true`) → accès total sans authentification.
  ```
  https://<project-id>.firebaseio.com/.json   → test direct de lecture publique
  ```
- **GCS buckets publics** — équivalent S3, mêmes techniques d'énumération (`cloud_enum`, `gcpbucketbrute`).
- **Service accounts avec rôles trop larges** — `roles/owner` attaché à un service account utilisé par une fonction exposée.
- **Cloud Functions non authentifiées** (`allUsers` avec rôle `Cloud Functions Invoker`).

## Azure

- **Blob Storage public** — équivalent S3/GCS (`az storage blob list` en anonyme, ou `microburst`/`cloud_enum`).
- **Azure AD misconfigurations** — applications enregistrées avec des permissions excessives, redirect URIs OAuth trop permissifs (voir 03/04 OAuth).
- **Storage Account keys leakées** — souvent via repos GitHub publics ou configs CI/CD exposées.

## Subdomain Takeover

### Contexte

Un enregistrement DNS (CNAME généralement) pointe vers un service cloud/tiers désactivé/non réclamé (bucket S3 supprimé, app Heroku supprimée, page GitHub Pages désactivée) — l'attaquant peut alors réclamer ce service et servir du contenu sous le domaine légitime de la cible.

### Comment tester

```bash
# Outils dédiés
subjack -w subdomains.txt -t 100 -o results.txt -ssl
nuclei -l subdomains.txt -t takeovers/

# Vérification manuelle : CNAME pointant vers un service tiers avec message d'erreur caractéristique
dig CNAME sub.target.com
curl -I https://sub.target.com   # chercher "NoSuchBucket", "There isn't a GitHub Pages site here", etc.
```

**Services fréquemment vulnérables (liste vivante — vérifier can-i-take-over-xyz) :** S3, GitHub Pages, Heroku, Azure (cloudapp.net, trafficmanager.net), Fastly, Unbounce, Shopify, Netlify, Zendesk, WPEngine, Cargo, Tumblr, Surge.sh, Bitbucket.

> 💡 **Pro tip :** Un takeover confirmé peut être escaladé en volant des cookies (si le domaine/sous-domaine parent partage un scope de cookie via `Domain=.target.com`), en contournant une CSP qui whitelist ce sous-domaine, ou en interceptant des redirections OAuth mal validées pointant vers ce sous-domaine.

## Kubernetes

| Vecteur | Test |
|---|---|
| Dashboard Kubernetes exposé sans auth | `https://<ip>:8443/` accessible publiquement |
| API server exposé (`:6443`) sans authentification forte | `kubectl --server=https://target:6443 --insecure-skip-tls-verify get pods` |
| Kubelet API exposé (`:10250`) | Exécution de commandes dans des pods via l'API kubelet non authentifiée |
| ConfigMaps/Secrets exposés via une app vulnérable (SSRF, path traversal) | Pivot vers les credentials internes du cluster |
| RBAC trop permissif | Service account de pod avec des permissions cluster-admin alors qu'il ne devrait accéder qu'à son namespace |
| etcd exposé sans authentification (`:2379`) | Lecture directe de tous les secrets du cluster |

## IaC (Infrastructure as Code) Misconfig — recon statique

Si le code Terraform/CloudFormation/Pulumi de la cible est accessible (repo public, fuite) :
```bash
# Scan automatisé de misconfigurations IaC
checkov -d ./terraform-repo/
tfsec ./terraform-repo/
```
Cherche : buckets sans chiffrement/versioning, security groups avec `0.0.0.0/0` sur des ports sensibles, IAM policies trop larges définies en dur.

## Comment confirmer l'impact

- Bucket/storage public : lister le contenu, télécharger UN fichier de preuve non sensible (nom de fichier suffit souvent), jamais un dump massif.
- Subdomain takeover : héberger une page de preuve minimale (pas de contenu trompeur/phishing) confirmant le contrôle du sous-domaine.
- Kubernetes/etcd exposé : lister les namespaces/secrets accessibles SANS les extraire ni les utiliser.

> ⚠️ **Attention légale :** L'accès à des credentials cloud (clés IAM, service account tokens) via ces vecteurs doit être **documenté, pas exploité activement** (pas de `aws s3 ls` sur l'ensemble du compte, pas de pivot supplémentaire) sauf autorisation explicite du programme.

## Références

- `cloud_enum`, `S3Scanner`, `gcpbucketbrute`, `microburst` (outils cloud recon)
- `can-i-take-over-xyz` (liste vivante de services vulnérables au takeover)
- `checkov`, `tfsec` (scan IaC)
- HackTricks — AWS/GCP/Azure Pentesting, Kubernetes Pentesting
