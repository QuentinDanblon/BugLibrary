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

## Nuclei templates fournis

Ces 6 templates ne sont pas écrits de mémoire : 5 sont copiés **verbatim** du dépôt officiel [`projectdiscovery/nuclei-templates`](https://github.com/projectdiscovery/nuclei-templates) (maintenu et testé par la communauté sécurité, licence MIT) — donc déjà éprouvés en conditions réelles par des milliers de scans. Le 6e (introspection GraphQL) n'a pas d'équivalent officiel ; il a été écrit ici puis **validé en sandbox** avec `nuclei -validate` et confirmé fonctionnel contre une vraie API GraphQL publique (`countries.trevorblades.com/graphql`), pas seulement contre un mock.

| Template | Sévérité | Détecte | Source |
|---|---|---|---|
| [`nuclei-templates/git-config.yaml`](nuclei-templates/git-config.yaml) | Medium | `.git/config` exposé (credentials embarqués) | officiel — `http/exposures/configs/git-config.yaml` |
| [`nuclei-templates/git-exposure.yaml`](nuclei-templates/git-exposure.yaml) | Medium | Dossier `.git/` exposé (reconstruction du repo via GitTools) | officiel — `http/exposures/logs/git-exposure.yaml` |
| [`nuclei-templates/laravel-env-and-generic-dotenv.yaml`](nuclei-templates/laravel-env-and-generic-dotenv.yaml) | High | Fichiers `.env` exposés (22 variantes de chemin, dont générique `/api/.env`) | officiel — `http/exposures/configs/laravel-env.yaml` |
| [`nuclei-templates/openapi-detect.yaml`](nuclei-templates/openapi-detect.yaml) | Info | `openapi.json` exposé | officiel — `http/exposures/apis/openapi.yaml` |
| [`nuclei-templates/swagger-api-detect.yaml`](nuclei-templates/swagger-api-detect.yaml) | Info | ~60 chemins Swagger UI/docs courants exposés | officiel — `http/exposures/apis/swagger-api.yaml` |
| [`nuclei-templates/graphiql-exposure.yaml`](nuclei-templates/graphiql-exposure.yaml) | Low | Console GraphiQL exposée publiquement | officiel — `http/misconfiguration/graphql/graphiql-exposure.yaml` |
| [`nuclei-templates/cloud-metadata-exposure.yaml`](nuclei-templates/cloud-metadata-exposure.yaml) | Low | Fuite directe de metadata cloud AWS/GCP reflétée dans la réponse | officiel — `http/misconfiguration/cloud-metadata.yaml` |
| [`nuclei-templates/graphql-introspection-enabled.yaml`](nuclei-templates/graphql-introspection-enabled.yaml) | Info | Introspection GraphQL activée (fuite de schéma complet) | BugLibrary — live-testé contre une API publique réelle |

Validation effectuée dans le sandbox de développement (pas juste une relecture) :
- `nuclei -validate -t tools/nuclei-templates/` → syntaxe des 8 templates confirmée valide par le moteur nuclei réel (v3.11.1).
- 6 des 8 templates confirmés en tir réel contre un serveur mock reproduisant les réponses exactes attendues (`.git/config`, `.git/` 403, `.env` Laravel, `openapi.json`, `swagger.json`, `/graphiql`) — tous ont matché correctement.
- Le template d'introspection GraphQL confirmé en tir réel contre une API GraphQL publique en production.

Lancer les templates :

```bash
nuclei -u https://target.com -t tools/nuclei-templates/laravel-env-and-generic-dotenv.yaml
nuclei -u https://target.com -t tools/nuclei-templates/  # tous les templates du dossier
```

## Wordlists fournies

Ces 3 wordlists ne sont pas tapées de mémoire — ce sont des extraits réels de [SecLists](https://github.com/danielmiessler/SecLists) (licence MIT), le standard de facto de l'industrie, filtrés/curés pour rester denses en signal.

| Wordlist | Contenu réel source | Usage |
|---|---|---|
| [`wordlists/common-api-endpoints.txt`](wordlists/common-api-endpoints.txt) | Copie intégrale (295 lignes) de `Discovery/Web-Content/api/api-endpoints.txt` | Content discovery ciblé API (`ffuf -w wordlists/common-api-endpoints.txt -u https://target.com/FUZZ`) |
| [`wordlists/common-idor-mass-assignment-params.txt`](wordlists/common-idor-mass-assignment-params.txt) | Filtrage par mots-clés (id/role/token/admin/scope/etc., 1100 lignes) de `Discovery/Web-Content/burp-parameter-names.txt` (6453 lignes réelles) | Fuzzing de paramètres pour IDOR/mass assignment (`arjun`, `ffuf` mode paramètre) |
| [`wordlists/common-subdomain-prefixes.txt`](wordlists/common-subdomain-prefixes.txt) | Top 150 lignes (classées par fréquence réelle d'observation) de `Discovery/DNS/subdomains-top1million-5000.txt` | Bruteforce/permutation de sous-domaines complémentaire à `subfinder`/`amass` (`subfinder -d target.com -all` puis permutation avec ce préfixe) |

Ces listes restent volontairement courtes — pour un fuzzing exhaustif, les combiner avec les listes complètes SecLists/Assetnote ci-dessous plutôt que les remplacer.

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
