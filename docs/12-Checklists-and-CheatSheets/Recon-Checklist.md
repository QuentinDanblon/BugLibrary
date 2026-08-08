# Checklist — Reconnaissance & Attack Surface Mapping

Cocher au fur et à mesure. Voir méthodologie complète : [`02-Reconnaissance`](../02-Reconnaissance/README.md).

## Phase 1 — Passive Recon

- [ ] Certificats TLS historiques (`crt.sh`, Censys, SecurityTrails) → liste de sous-domaines
- [ ] Shodan/FOFA/ZoomEye pour bannières de service et historique d'IP
- [ ] Wayback Machine / `waybackurls` pour URLs historiques
- [ ] Recherche de secrets/endpoints fuités sur GitHub/GitLab (org + forks + gists liés)
- [ ] DNS historique (DNSDumpster, SecurityTrails) pour sous-domaines désactivés
- [ ] Job postings / LinkedIn pour stack technique annoncée
- [ ] Reverse whois / ASN mapping pour ranges IP appartenant à l'organisation

## Phase 2 — Subdomain Enumeration

- [ ] `subfinder`, `amass -passive`, `assetfinder` combinés puis dédupliqués
- [ ] Résolution DNS (`dnsx`) + probing HTTP (`httpx -status-code -title -tech-detect`)
- [ ] Permutation/mutation (`altdns`, `gotator`, `dnsgen`) sur les sous-domaines connus
- [ ] Monitoring continu de Certificate Transparency (nouveaux sous-domaines en temps réel)
- [ ] Vérification de subdomain takeover (`subjack`, `nuclei -t takeovers/`)

## Phase 3 — Active Recon (⚠️ vérifier les règles du programme avant)

- [ ] Port scanning ciblé (`naabu` + `nmap -sV`) si autorisé par le scope
- [ ] Fingerprint techno précis (`httpx -tech-detect`, Wappalyzer)
- [ ] Screenshots de masse pour triage visuel (`gowitness`/`aquatone`)

## Phase 4 — Content Discovery

- [ ] Fuzzing de répertoires/fichiers avec wordlist à jour (`ffuf`)
- [ ] Extraction d'endpoints depuis JS non minifié (`katana -js-crawl`)
- [ ] Recherche de sourcemaps (`.js.map`) exposées accidentellement
- [ ] Découverte de paramètres cachés (`arjun`, `paramspider`)
- [ ] Diff du JS entre deux dates pour repérer les changements récents

## Phase 5 — API & GraphQL Discovery

- [ ] Recherche de doc exposée (`/swagger.json`, `/openapi.json`, `/api-docs`)
- [ ] Test d'introspection GraphQL (`/graphql`, `/graphiql`, `/playground`)
- [ ] Recherche de versions d'API multiples actives (`/v1/`, `/v2/`, `/v3/`)
- [ ] Recherche de collections Postman exposées publiquement

## Phase 6 — Cloud Asset Discovery

- [ ] Énumération de buckets S3/GCS/Azure Blob avec noms probables (`cloud_enum`)
- [ ] Vérification de lecture/écriture publique sur les buckets trouvés
- [ ] Recherche de Firebase Realtime Database/Firestore mal configuré

## Phase 7 — Historical & Leak-Based

- [ ] Vérification d'exposition d'identifiants via services légaux (HaveIBeenPwned)
- [ ] Monitoring de paste sites pour fuite de config/tokens
- [ ] Vérification de dependency confusion sur packages internes potentiellement mal nommés

## Phase 8 — Organisation & Priorisation

- [ ] Toutes les données classées dans une structure `recon/<target>/` cohérente
- [ ] Grille de priorisation appliquée (fonctionnalité sensible, nouveauté, stack à risque, faible couverture)
- [ ] Liste finale d'assets triés par priorité de test transmise à la phase de hunting actif
