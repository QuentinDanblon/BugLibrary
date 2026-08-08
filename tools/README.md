# tools/

Stack d'outils recommandée pour BugLibrary — voir le détail complet et le rôle de chaque outil dans [`docs/09-Automation-and-Tooling/README.md`](../docs/09-Automation-and-Tooling/README.md).

## Organisation de ce dossier

```
tools/
├── README.md              → ce fichier, index de la stack
├── wordlists/              → wordlists custom BugLibrary (curées, petites, versionnées ici)
├── nuclei-templates/       → templates nuclei custom écrits par la communauté BugLibrary
└── burp-configs/           → configurations Burp Suite exportées (scope presets, extensions recommandées)
```

## Nuclei templates custom fournis

| Template | Sévérité | Détecte |
|---|---|---|
| [`nuclei-templates/exposed-env-file.yaml`](nuclei-templates/exposed-env-file.yaml) | High | Fichiers `.env` exposés publiquement (credentials DB, clés API) |
| [`nuclei-templates/graphql-introspection-enabled.yaml`](nuclei-templates/graphql-introspection-enabled.yaml) | Info | Introspection GraphQL activée (fuite de schéma complet) |
| [`nuclei-templates/exposed-swagger-openapi-docs.yaml`](nuclei-templates/exposed-swagger-openapi-docs.yaml) | Info | Documentation Swagger/OpenAPI exposée publiquement |
| [`nuclei-templates/exposed-git-config.yaml`](nuclei-templates/exposed-git-config.yaml) | Medium | Dossier `.git` exposé (reconstruction du code source possible) |
| [`nuclei-templates/cloud-metadata-ssrf-probe.yaml`](nuclei-templates/cloud-metadata-ssrf-probe.yaml) | Info (référence manuelle) | Payloads de référence pour confirmer un SSRF vers les endpoints metadata cloud (AWS/GCP/Azure/Alibaba) — usage manuel, pas un scan automatisé |

Lancer les templates automatisés :

```bash
nuclei -u https://target.com -t tools/nuclei-templates/exposed-env-file.yaml
nuclei -u https://target.com -t tools/nuclei-templates/  # tous les templates du dossier (sauf le probe SSRF, à usage manuel)
```

## Wordlists custom fournies

| Wordlist | Usage |
|---|---|
| [`wordlists/common-api-endpoints.txt`](wordlists/common-api-endpoints.txt) | Content discovery ciblé API (`ffuf -w wordlists/common-api-endpoints.txt -u https://target.com/FUZZ`) |
| [`wordlists/common-idor-mass-assignment-params.txt`](wordlists/common-idor-mass-assignment-params.txt) | Fuzzing de paramètres pour IDOR/mass assignment (`arjun`, `ffuf` mode paramètre) |
| [`wordlists/common-subdomain-prefixes.txt`](wordlists/common-subdomain-prefixes.txt) | Bruteforce/permutation de sous-domaines complémentaire à `subfinder`/`amass` |

Ces listes sont volontairement courtes et curées (signal dense) — pour un fuzzing exhaustif, les combiner avec SecLists/Assetnote ci-dessous plutôt que les remplacer.

## Installation rapide de la stack recon de base

```bash
# Go-based tools (via go install)
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/ffuf/ffuf/v2@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/tomnomnom/waybackurls@latest

# Python-based tools
pip install arjun
pip install paramspider

# sqlmap
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git

# jwt_tool
git clone https://github.com/ticarpi/jwt_tool.git
```

## Extensions Burp Suite recommandées (BApp Store)

Autorize, Param Miner, Turbo Intruder, HTTP Request Smuggler, JS Link Finder, Logger++, InQL, Active Scan++, Backslash Powered Scanner, JSON Web Tokens.

## Wordlists recommandées (à jour, pas SecLists 2018)

- [SecLists](https://github.com/danielmiessler/SecLists) (référence générale, vérifier la mise à jour régulière)
- [Assetnote Wordlists](https://wordlists.assetnote.io/) (générées et mises à jour automatiquement depuis du contenu réel observé — excellente qualité)
- Wordlists custom générées par cible via extraction de JS/contenu observé (`cewl`, extraction manuelle de termes métier spécifiques).

> ⚠️ Les wordlists volumineuses ne sont pas versionnées dans ce dépôt (voir `.gitignore`) — chaque contributeur les récupère localement depuis les sources ci-dessus.
