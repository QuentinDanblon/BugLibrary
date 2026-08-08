# Contributing to BugLibrary / Contribuer à BugLibrary

Thank you for helping build the elite bug-hunting reference library.  
Merci de contribuer à la bible du bug hunting.

---

## English

### What we accept

| Type | Welcome? | Notes |
|------|----------|--------|
| Methodology, checklists, report templates | ✅ | High priority |
| Modern techniques (2024–2026), with legal framing | ✅ | Authorized testing only |
| Case studies (anonymized, educational) | ✅ | No live 0-days / private disclosures |
| AI agent prompts & workflows | ✅ | OPSEC-aware |
| Runnable exploit PoCs / malware / weaponized payloads | ❌ | Hard reject |
| Out-of-scope attack guides | ❌ | Hard reject |
| Credential dumps / PII | ❌ | Hard reject |

### Quality bar

Content must be:

1. **Actionable** — a hunter can apply it the same day
2. **Accurate** — techniques validated or clearly marked as experimental
3. **Scoped** — always assume authorized programs (HackerOne, Bugcrowd, Intigriti, VDP, pentest RoE)
4. **Structured** — headings, tables, checklists, pro tips
5. **Bilingual when user-facing** — French + English for major prose (or dual sections)
6. **Safe** — describe *classes* of issues and testing approaches; do not ship attack engines

### How to contribute

1. Fork the repository
2. Create a branch: `docs/<section>-<short-topic>`
3. Add or improve Markdown under the correct `docs/NN-*/` folder
4. Update section `README.md` indexes if you add files
5. Run a self-review against the checklist below
6. Open a Pull Request with a clear summary (what / why / risk)

### Self-review checklist

- [ ] No weaponized payloads or live malware
- [ ] Explicit “authorized testing only” where offensive techniques appear
- [ ] Links to related sections (Legal, Reporting, OPSEC) when relevant
- [ ] Tables / checklists used instead of walls of text
- [ ] Pro tips labeled and concrete
- [ ] French + English for major new guides (or note if EN-only temporary)
- [ ] No secrets, tokens, real target data, or private program details
- [ ] Living Document note updated if process changed (`docs/14-...`)

### Style guide

- Prefer short paragraphs and bullet lists
- Use fenced code only for **safe** examples (headers, query shapes, report structure)
- Mark severity language carefully (CVSS as guidance, not gospel)
- Name tools generically when possible; link official docs
- Date-stamp major technique notes when tied to a year (`<!-- updated: 2026-03 -->`)

### Commit messages

```
docs(web): add IDOR prioritization matrix
docs(ai): expand multi-agent recon orchestration
fix(templates): clarify impact section in bug-report template
chore: update living-document maintenance cadence
```

### Reporting security issues in *this* repo

If you find a vulnerability in BugLibrary infrastructure or accidental secret exposure, contact the maintainer privately — do not open a public issue with secrets.

---

## Français

### Ce que nous acceptons

| Type | Accepté ? | Notes |
|------|-----------|--------|
| Méthodologie, checklists, templates de rapports | ✅ | Priorité haute |
| Techniques modernes (2024–2026), cadre légal | ✅ | Tests autorisés uniquement |
| Études de cas (anonymisées, pédagogiques) | ✅ | Pas de 0-day privés |
| Prompts & workflows agents IA | ✅ | OPSEC conscient |
| PoC d'exploits exécutables / malware | ❌ | Rejet |
| Guides d'attaque hors scope | ❌ | Rejet |
| Dumps de credentials / PII | ❌ | Rejet |

### Barre de qualité

1. **Actionnable** — applicable le jour même  
2. **Précis** — validé ou marqué expérimental  
3. **Scopé** — programmes autorisés uniquement  
4. **Structuré** — titres, tableaux, checklists, pro tips  
5. **Bilingue** pour le contenu majeur FR + EN  
6. **Sûr** — classes de bugs et approches de test, pas d'armes clés en main  

### Processus

1. Fork  
2. Branche `docs/<section>-<sujet>`  
3. Markdown dans le bon dossier `docs/NN-*/`  
4. Mettre à jour l'index de section  
5. Auto-revue (checklist ci-dessus)  
6. Pull Request claire  

### Messages de commit

Préfixer par `docs(scope):`, `fix(templates):`, `chore:`.

---

## Code of Conduct

By participating, you agree to our [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
