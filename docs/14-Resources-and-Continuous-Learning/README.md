# 14 — Resources & Continuous Learning

## Ce dépôt est un "Living Document"

### Pourquoi la mise à jour continue est non négociable

- Les frameworks changent leurs défauts de sécurité (React/Angular patchent des sinks XSS, Express change ses middlewares par défaut).
- Les WAF évoluent — un bypass documenté aujourd'hui peut être patché dans 3 mois.
- De nouvelles classes de vulnérabilités émergent (ex: les attaques sur les LLM/RAG deviennent une surface propre depuis 2023-2024 — prompt injection, data poisoning dans des pipelines d'agents).
- Les techniques de chaînage se raffinent constamment (recherche PortSwigger, DEF CON, Black Hat chaque année).

### Protocole de mise à jour recommandé

| Fréquence | Action |
|---|---|
| Hebdomadaire | Parcourir la Hacktivity HackerOne publique (nouveaux rapports divulgués) pour repérer des patterns émergents |
| Mensuelle | Vérifier les nouvelles publications PortSwigger Research, Project Zero, Trail of Bits blog |
| Trimestrielle | Revue complète d'une section du dépôt — vérifier que les payloads/outils cités sont toujours d'actualité |
| Après chaque grosse conférence (DEF CON, Black Hat, OWASP AppSec) | Intégrer les nouvelles techniques présentées pertinentes pour le bug bounty |
| Après chaque CVE majeure dans un framework populaire | Ajouter une entrée si la technique est généralisable (pas juste un CVE ponctuel patché) |

### Signaux qu'une section a besoin d'une mise à jour

- Un outil cité n'est plus maintenu (dernier commit > 2 ans, remplacé par un successeur communément adopté).
- Un payload/bypass documenté ne fonctionne plus contre les versions actuelles des frameworks/WAF mentionnés.
- Une nouvelle classe de vulnérabilité représente désormais une part significative des rapports payés observés en Hacktivity.
- Un contributeur signale via une issue/PR qu'une technique est obsolète.

## Sources de veille recommandées

### Recherche et publications techniques
- PortSwigger Research (blog + Web Security Academy — mises à jour très régulières)
- Project Zero (Google) — analyses techniques de très haut niveau, surtout binaire/navigateur
- Trail of Bits blog
- Orange Tsai (blog.orange.tw) — recherche SSRF/désérialisation avancée
- HackTricks (livre en ligne exhaustif, mis à jour en continu par la communauté)
- PayloadsAllTheThings (dépôt GitHub de référence pour payloads par catégorie)

### Plateformes et communautés
- HackerOne Hacktivity (rapports publiquement divulgués — la meilleure source de patterns réels payés)
- Bugcrowd University (contenu pédagogique gratuit, niveau intermédiaire à avancé)
- Twitter/X communauté bug bounty (comptes de chercheurs reconnus — vérifier la fiabilité avant application)
- Discord/Slack communautaires de bug bounty (échanges informels, souvent des alertes rapides sur des bypass frais)

### Conférences
- DEF CON, Black Hat (USA/Europe/Asia) — talks orientés recherche offensive
- OWASP AppSec (Global + régionaux)
- Nullcon, Troopers, OffensiveCon — recherche binaire/exploitation avancée

### Formation continue structurée
- PortSwigger Web Security Academy (gratuit, exercices pratiques par catégorie, référence absolue)
- PentesterLab (labs pratiques payants, niveau intermédiaire à avancé)
- HackTheBox / TryHackMe (pratique généraliste, utile pour les fondamentaux réseau/binaire)

## Journal des évolutions majeures (à maintenir)

> Section à compléter par les contributeurs à chaque mise à jour significative — format : Date, Section modifiée, Raison du changement.

| Date | Section | Changement |
|---|---|---|
| 2026-08 | Création initiale | Version initiale complète du dépôt (00-14 + templates + tools) |

## Comment proposer une mise à jour

Voir [`CONTRIBUTING.md`](../../CONTRIBUTING.md). Toute PR touchant une technique existante doit préciser explicitement ce qui a changé et pourquoi (version de framework, date de test, référence à la source de la découverte de l'obsolescence).
