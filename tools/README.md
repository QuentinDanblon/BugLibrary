# tools/

Stack d'outils recommandée pour BugLibrary — voir le détail complet et le rôle de chaque outil dans [`docs/09-Automation-and-Tooling/README.md`](../docs/09-Automation-and-Tooling/README.md).

## Organisation de ce dossier

```
tools/
├── README.md              → ce fichier, index de la stack
├── wordlists/              → wordlists custom recommandées (non versionnées si volumineuses — voir .gitignore)
├── nuclei-templates/       → templates nuclei custom écrits par la communauté BugLibrary
└── burp-configs/           → configurations Burp Suite exportées (scope presets, extensions recommandées)
```

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
