# 00 — Introduction

## Objectif de cette bibliothèque

BugLibrary n'est pas un cours. C'est un **système de référence opérationnel** : tu l'ouvres quand tu es sur une cible réelle, tu cherches la section pertinente, tu appliques, tu reviens si besoin. Chaque document est écrit pour être consommé en 2-5 minutes et donner une action immédiate.

## Pour qui

- Hunters bug bounty avancés à experts (déjà familiers avec HTTP, les bases OWASP, Burp Suite).
- Pentesters professionnels cherchant une référence dense.
- **Agents IA** orchestrés pour automatiser tout ou partie de la chasse (recon, triage d'hypothèses, génération de payloads, rédaction de rapports).

## Comment lire ce dépôt efficacement

1. **Ne lis jamais un doc de A à Z avant d'agir.** Va directement à la checklist ou à la technique dont tu as besoin (`Ctrl+F` est ton ami).
2. **Chaque technique suit le même squelette** : Contexte → Comment tester → Comment confirmer l'impact → Remédiation (pour comprendre la vraie sévérité) → Références.
3. **Les pro-tips (💡) sont les vrais alpha.** Ce sont les détails qui séparent un rapport dupliqué d'un rapport unique et payé.
4. **Les avertissements (⚠️) sont non négociables.** Scope, légalité, destruction de données — ignore-les et tu risques une interdiction de programme ou pire.

## Philosophie de cette bibliothèque

### 1. Impact avant technique
Une XSS reflétée sur un endpoint sans session n'a aucune valeur. Le hunting d'élite ne collectionne pas les vulnérabilités, il **collectionne l'impact** : prise de compte, exfiltration de données, exécution de code, contournement de contrôle financier. Chaque technique documentée ici est reliée à un scénario d'impact concret.

### 2. Hypothèses avant scanners
Les scanners automatiques trouvent ce que tout le monde trouve. L'élite formule des **hypothèses** sur la base de l'architecture observée ("cette API utilise probablement un JWT signé HS256 avec une clé faible parce que le stack est Node/Express et la doc Swagger fuite le middleware"), puis teste précisément cette hypothèse. Voir [`01-Mindset-and-Methodology`](../01-Mindset-and-Methodology/README.md).

### 3. La reconnaissance est 70% du travail
Sur un programme mature (Google, Meta, grosses fintechs), la vulnérabilité triviale n'existe presque plus en surface évidente. Elle se trouve dans l'asset oublié, le sous-domaine de dev exposé, l'API interne mal documentée. Voir [`02-Reconnaissance`](../02-Reconnaissance/README.md).

### 4. Le chaînage fait le payout
Une IDOR seule = P4/low. Une IDOR + une fuite d'ID prévisible + une absence de rate limiting = prise de compte de masse = critique. Voir [`08-Advanced-Techniques`](../08-Advanced-Techniques/README.md).

### 5. Le rapport est un livrable, pas une formalité
Un rapport mal écrit fait baisser la sévérité perçue même pour un bug critique réel. Voir [`10-Reporting-and-Communication`](../10-Reporting-and-Communication/README.md) et [`templates/bug-report-template.md`](../../templates/bug-report-template.md).

## Prérequis techniques supposés

- HTTP/HTTPS en profondeur (headers, méthodes, codes de statut, cookies, CORS, CSP).
- Burp Suite (Repeater, Intruder, Extender) ou équivalent (Caido).
- Bases de scripting (Python et/ou Bash) pour automatiser.
- Lecture de code source (au moins JS côté client, idéalement backend courant : Node, Python, PHP, Java, Go).
- Notions réseau (DNS, TLS, reverse proxy, CDN).

## Ce que cette bibliothèque n'est PAS

- Pas un cours OWASP Top 10 pour débutants.
- Pas une liste de payloads copiés-collés sans compréhension du contexte.
- Pas un outil légal — ne remplace pas l'avis d'un juriste sur la portée d'un programme.

## Navigation rapide

| Je veux... | Va à... |
|---|---|
| Structurer mon approche mentale sur une nouvelle cible | [`01-Mindset-and-Methodology`](../01-Mindset-and-Methodology/README.md) |
| Cartographier la surface d'attaque | [`02-Reconnaissance`](../02-Reconnaissance/README.md) |
| Trouver des vulns web classiques et modernes | [`03-Web-Application-Hunting`](../03-Web-Application-Hunting/README.md) |
| Cibler une API REST/GraphQL | [`04-API-GraphQL-Hunting`](../04-API-GraphQL-Hunting/README.md) |
| Chasser sur mobile | [`05-Mobile-Hunting`](../05-Mobile-Hunting/README.md) |
| Chasser sur du cloud/infra | [`06-Cloud-and-Infrastructure`](../06-Cloud-and-Infrastructure/README.md) |
| Reverser un binaire | [`07-Binary-and-Reverse-Engineering`](../07-Binary-and-Reverse-Engineering/README.md) |
| Techniques avancées et chaînage | [`08-Advanced-Techniques`](../08-Advanced-Techniques/README.md) |
| Automatiser / utiliser des agents IA | [`09-Automation-and-Tooling`](../09-Automation-and-Tooling/README.md) |
| Rédiger un rapport qui paie | [`10-Reporting-and-Communication`](../10-Reporting-and-Communication/README.md) |
| Rester dans les clous légalement | [`11-Legal-Ethics-and-OPSEC`](../11-Legal-Ethics-and-OPSEC/README.md) |
| Checklist rapide avant de soumettre | [`12-Checklists-and-CheatSheets`](../12-Checklists-and-CheatSheets/README.md) |
| Étudier des cas réels | [`13-Case-Studies`](../13-Case-Studies/README.md) |
| Rester à jour | [`14-Resources-and-Continuous-Learning`](../14-Resources-and-Continuous-Learning/README.md) |
