# Contributing to BugLibrary

**FR ci-dessous / French version below.**

## EN — How to Contribute

BugLibrary is a living document. It stays valuable only if it keeps absorbing new techniques, retiring dead ones, and getting more precise over time.

### What we want

- **New, actionable techniques** — 2024-2026 relevant, with a working PoC/example, not theory copy-pasted from a 2015 blog post.
- **Checklist improvements** — a missing test case, a sharper hypothesis, a faster triage heuristic.
- **Corrections** — outdated payloads, dead tools, WAF bypasses that no longer work.
- **Case studies** — anonymized/generalized write-ups of real findings (scrub target identity unless it's already public disclosure).
- **Templates** — better report structures, better recon note formats.

### What we reject

- Anything violating `CODE_OF_CONDUCT.md` (illegal use, undisclosed exploits, malware).
- Unverified claims ("I heard this works") without a reproducible example.
- Duplicate content — check existing docs first.
- Pure theory with zero actionability.

### How to submit

1. Fork the repo.
2. Create a branch: `git checkout -b add/<short-topic>` or `fix/<short-topic>`.
3. Add/edit content under `docs/<relevant-section>/`. Follow the existing Markdown style (tables, checklists, mermaid diagrams where useful, pro-tips in blockquotes).
4. If adding a technique, include: **context**, **how to test**, **how to confirm impact**, **remediation note**, **references**.
5. Run a spell/link check if you can (`markdown-link-check` recommended).
6. Open a Pull Request with a clear description of what changed and why.
7. One reviewer approval minimum before merge.

### Style guide (quick reference)

- Headers: `##` for major subsection, `###` for detail blocks.
- Use tables for comparisons (severity, tool matrices, payload lists).
- Use fenced code blocks with language hints (` ```http `, ` ```bash `, ` ```graphql `, ...).
- Pro tips: `> 💡 **Pro tip:** ...`
- Warnings: `> ⚠️ **Attention scope/legal:** ...`
- Keep sentences dense — no filler. Every line should teach something or point somewhere.

### Commit messages

Conventional style: `docs(section): short description`, e.g. `docs(web): add HTTP request smuggling desync chain example`.

---

## FR — Comment contribuer

BugLibrary est un document vivant. Il ne garde sa valeur que s'il continue d'absorber de nouvelles techniques, d'en retirer les obsolètes, et de gagner en précision.

### Ce qu'on veut

- **Techniques actionnables et récentes** (2024-2026), avec un exemple/PoC fonctionnel — pas de la théorie recopiée d'un article de 2015.
- **Améliorations de checklists** — un cas de test manquant, une hypothèse plus fine, une heuristique de triage plus rapide.
- **Corrections** — payloads obsolètes, outils morts, bypass WAF qui ne fonctionnent plus.
- **Études de cas** — retours d'expérience anonymisés/généralisés sur des découvertes réelles (masquer l'identité de la cible sauf si déjà en disclosure publique).
- **Templates** — meilleures structures de rapport, meilleurs formats de notes de recon.

### Ce qu'on refuse

- Tout ce qui viole `CODE_OF_CONDUCT.md` (usage illégal, exploits non divulgués, malware).
- Affirmations non vérifiées ("j'ai entendu dire que ça marche") sans exemple reproductible.
- Contenu dupliqué — vérifier l'existant avant de proposer.
- Théorie pure sans aucune actionnabilité.

### Comment soumettre

1. Forker le dépôt.
2. Créer une branche : `git checkout -b add/<sujet-court>` ou `fix/<sujet-court>`.
3. Ajouter/modifier le contenu sous `docs/<section-concernée>/`. Respecter le style Markdown existant (tables, checklists, diagrammes mermaid si utile, pro-tips en citation).
4. Pour une nouvelle technique, inclure : **contexte**, **comment tester**, **comment confirmer l'impact**, **remédiation**, **références**.
5. Vérifier l'orthographe et les liens si possible.
6. Ouvrir une Pull Request avec une description claire du changement et de sa raison.
7. Une approbation minimum avant fusion.

### Guide de style (référence rapide)

Voir la section anglaise ci-dessus — les conventions sont identiques (tables, blocs de code avec langage, pro-tips en blockquote, avertissements légaux explicites, phrases denses sans remplissage).

### Messages de commit

Style conventionnel : `docs(section): description courte`, ex. `docs(web): ajout chaîne de desync HTTP request smuggling`.
